# core/views.py

from http import HTTPStatus
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator


PAGE_SIZE = 20


def index(request):
    return redirect("tasks/")


def _create_todo(request):
    title = request.POST.get("title")
    if not title:
        raise ValueError("Title is required")

    todo = Todo.objects.create(title=title, user=request.user)
    return render(
        request,
        "tasks.html#todo-items-partial",
        {"todos": [todo]},
        status=HTTPStatus.CREATED,
    )


@require_http_methods(["GET", "POST"])
@login_required
def tasks(request):
    if request.method == "POST":
        return _create_todo(request)

    page_number = int(request.GET.get("page", 1))

    all_todos = request.user.todos.all().order_by("-created_at")
    paginator = Paginator(all_todos, PAGE_SIZE)
    curr_page = paginator.get_page(page_number)

    context = {
        "todos": curr_page.object_list,
        "fullname": request.user.get_full_name() or request.user.username,
        "next_page_number": page_number + 1 if curr_page.has_next() else None,
    }

    template_name = "tasks.html"

    if "HX-Request" in request.headers:
        template_name += "#todo-items-partial"

    return render(request, template_name, context)


@login_required
@require_http_methods(["PUT"])
def toggle_todo(request, task_id):
    todo = request.user.todos.get(id=task_id)
    todo.is_completed = not todo.is_completed
    todo.save()

    return render(
        request,
        "tasks.html#todo-items-partial",
        {
            "todos": [todo],
        },
    )


@login_required
@require_http_methods(["DELETE", "POST", "GET"])
def task_details(request, task_id):
    todo = request.user.todos.get(id=task_id)

    if request.method == "DELETE":
        todo.delete()
        response = HttpResponse(status=HTTPStatus.NO_CONTENT)
        response["HX-Trigger"] = "todo-deleted"
        return response

    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            raise ValueError("Title is required")

        todo.title = title
        todo.is_completed = bool(request.POST.get("is_completed"))
        todo.save()

    # GET will just return the todo details
    return render(
        request,
        "tasks.html#todo-items-partial",
        {"todos": [todo]},
    )


@login_required
@require_http_methods(["GET"])
def edit_task(request, task_id):
    todo = request.user.todos.get(id=task_id)
    return render(
        request,
        "tasks.html#todo-item-edit",
        {"todo": todo},
    )


@login_required
@require_http_methods(["POST"])
def search(request):
    query = request.POST.get("query")

    if not query:
        return redirect("tasks")

    results = request.user.todos.filter(title__icontains=query).order_by("-created_at")

    return render(
        request,
        "tasks.html#todo-items-partial",
        {"todos": results},
        status=HTTPStatus.OK,
    )
