from django.shortcuts import redirect, render
from .models import UserProfile, Todo
from django.contrib.auth.decorators import login_required


def index(request):
    return redirect("tasks/")


def get_user_todos(user: UserProfile) -> list[Todo]:
    return user.todos.all().order_by("created_at")


@login_required
def tasks(request):
    context = {
        "todos": get_user_todos(request.user),
        "fullname": request.user.get_full_name() or request.user.username,
    }

    return render(request, "tasks.html", context)
