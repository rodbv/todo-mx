# core/tests/conftest.py

import pytest
from model_bakery import baker


@pytest.fixture
def make_user(django_user_model):
    def _make_user(**kwargs):
        return baker.make("core.UserProfile", **kwargs)

    return _make_user


@pytest.fixture
def make_todo(make_user):
    def _make_todo(user=None, **kwargs):
        return baker.make("core.Todo", user=user or make_user(), **kwargs)

    return _make_todo
