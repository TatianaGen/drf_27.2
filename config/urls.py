import django.contrib
from django.urls import path, include

urlpatterns = [
    path("admin/", django.contrib.admin.site.urls),
    path("materials/", include("materials.urls", namespace="materials")),
    path("users/", include("users.urls", namespace="users")),
]
