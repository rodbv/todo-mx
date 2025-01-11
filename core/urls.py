# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<int:task_id>/toggle/", views.toggle_todo, name="toggle_todo"),
    path("tasks/<int:task_id>/", views.task_details, name="task_details"),
    path("tasks/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("tasks/search/", views.search, name="search"),
]
