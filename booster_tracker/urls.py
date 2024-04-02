from django.urls import path
from booster_tracker import views

urlpatterns = [
    path("", views.home, name="home"),
]