# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<int:task_id>/", views.toggle_todo, name="toggle_todo"),  # <-- NEW
]
