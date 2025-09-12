from django.urls import path
from . import views   # ✅ This is required to use views.home

urlpatterns = [
    path("", views.home, name="home"),
]
