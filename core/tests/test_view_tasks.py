# core/tests/test_view_tasks.py

from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


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

    content = response.content.decode()

    assert "New Todo" in content
    assert '<li class="list-row">' in content


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

    content = response.content.decode()

    assert "New Todo" in content
    assert '<li class="list-row">' in content
