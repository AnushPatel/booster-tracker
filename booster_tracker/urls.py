from django.urls import path
from booster_tracker import views

urlpatterns = [
    path("", views.home, name="home"),
    path("launches/<str:launch_name>/", views.launch_details, name="launch"),
    path("launches/", views.index, name="launches")
]