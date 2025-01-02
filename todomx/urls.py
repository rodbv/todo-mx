# todomx/urls.py

from django.contrib import admin
from django.urls import include, path  # <-- NEW

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),  # <-- NEW
]
