# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Todo, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ["email", "username"]


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    model = Todo
    list_display = ["title", "is_completed", "user"]
    list_filter = ["is_completed"]
    search_fields = ["title"]
    list_per_page = 10
    ordering = ["title"]
