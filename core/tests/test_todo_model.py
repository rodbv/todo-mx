# core/tests/test_todo_model.py

import pytest


@pytest.mark.django_db
class TestTodoModel:
    def test_todo_items_are_associated_to_users(self, make_todo, make_user):
        [user1, user2] = make_user(_quantity=2)

        for i in range(3):
            make_todo(user=user1, title=f"user1 todo {i}")

        make_todo(user=user2, title="user2 todo")

        assert {todo.title for todo in user1.todos.all()} == {
            "user1 todo 0",
            "user1 todo 1",
            "user1 todo 2",
        }

        assert {todo.title for todo in user2.todos.all()} == {"user2 todo"}
