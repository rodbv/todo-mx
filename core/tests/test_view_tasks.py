# core/tests/test_view_tasks.py

from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from core.views import PAGE_SIZE


@pytest.mark.django_db
def test_get_tasks_returns_tasks_template_and_todo_items_of_the_user(
    client, make_user, make_todo
):
    user = make_user()
    client.force_login(user)

    make_todo(_quantity=3, user=user)

    response = client.get(reverse("tasks"))

    assertTemplateUsed(response, "tasks.html")

    assert response.status_code == HTTPStatus.OK
    assert len(response.context["todos"]) == 3
    assert all(todo.user == user for todo in response.context["todos"])


@pytest.mark.django_db
def test_create_todo_view_stores_todo_and_returns_todo_on_partial(client, make_user):
    user = make_user()
    client.force_login(user)

    response = client.post(reverse("tasks"), {"title": "New Todo"})

    assert user.todos.filter(title="New Todo").exists()
    assert response.status_code == HTTPStatus.CREATED

    content = response.content.decode().strip()

    assert "New Todo" in content
    assert content.startswith("<li")
    assert content.endswith("</li>")


@pytest.mark.parametrize("is_completed", [True, False])
@pytest.mark.django_db
def test_put_todo_toggles_todo_status_and_returns_todo_on_partial(
    client, make_todo, make_user, is_completed
):
    user = make_user()
    client.force_login(user)

    todo = make_todo(title="New Todo", user=user, is_completed=is_completed)

    response = client.put(reverse("toggle_todo", args=[todo.id]))

    todo.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert todo.is_completed is not is_completed

    content = response.content.decode().strip()

    assert "New Todo" in content
    assert content.startswith("<li")
    assert content.endswith("</li>")


@pytest.mark.django_db
def test_delete_task(client, make_todo, make_user):
    user = make_user()
    client.force_login(user)

    todo = make_todo(title="New Todo", user=user)

    response = client.delete(reverse("task_details", args=[todo.id]))

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response["HX-Trigger"] == "todo-deleted"
    assert not user.todos.filter(title="New Todo").exists()


@pytest.mark.django_db
def test_tasks_pagination(client, make_todo, make_user):
    user = make_user()
    client.force_login(user)

    # create 2 pages of data
    for i in range(PAGE_SIZE + 3):
        make_todo(title=f"Todo #{i}", user=user)

    response = client.get(reverse("tasks"))

    context = response.context
    assert context["next_page_number"] == 2
    assert len(context["todos"]) == PAGE_SIZE

    # add header to ensure this is processed as an HTMX request
    response = client.get(reverse("tasks") + "?page=2", HTTP_HX_Request="true")

    content = response.content.decode().strip()
    assert content.startswith("<li")
    assert content.endswith("</li>")

    assert ">Todo #22<" not in content
    assert ">Todo #1<" in content


# This is the ideal type of test but it doesn't work
# due to issue #54 in django-template-partials

# pytest.mark.django_db
# def test_search_filtering(client, make_todo, make_user):
#     user = make_user()
#     client.force_login(user)

#     make_todo(title="Todo 1", user=user)
#     make_todo(title="Another Todo", user=user)
#     make_todo(title="Something else", user=user)

#     response = client.post(reverse("search"), {"query": "Todo"})
#     context = response.context

#     assert len(context["todos"]) == 2
#     assert any(todo.title == "Todo 1" for todo in context["todos"])
#     assert any(todo.title == "Another Todo" for todo in context["todos"])


@pytest.mark.django_db
def test_search_filtering(client, make_todo, make_user):
    user = make_user()
    client.force_login(user)

    make_todo(title="Todo 1", user=user)
    make_todo(title="Another Todo", user=user)
    make_todo(title="Something else", user=user)

    response = client.post(reverse("search"), {"query": "Todo"})
    content = response.content.decode()

    assert "Todo 1" in content
    assert "Another Todo" in content

    assert "Something else" not in content


@pytest.mark.django_db
def test_search_empty_query_redirects_to_all_tasks(client, make_todo, make_user):
    user = make_user()
    client.force_login(user)

    make_todo(title="Todo 1", user=user)
    make_todo(title="Another Todo", user=user)
    make_todo(title="Something else", user=user)

    response = client.post(reverse("search"), {"query": ""})
    assert response.status_code == HTTPStatus.FOUND  # redirect
    assert response.url == reverse("tasks")


@pytest.mark.django_db
def test_search_zero_matches_returns_empty_list(client, make_todo, make_user):
    user = make_user()
    client.force_login(user)

    make_todo(title="Todo 1", user=user)
    make_todo(title="Another Todo", user=user)
    make_todo(title="Something else", user=user)

    response = client.post(reverse("search"), {"query": "Nonexistent"})
    content = response.content.decode()

    assert not any(
        todo in content for todo in ["Todo 1", "Another Todo", "Something else"]
    )
