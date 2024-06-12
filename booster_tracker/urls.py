from django.urls import path, include
from booster_tracker import views

app_name = "booster_tracker"
urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health, name="health"),
    path("launches/<str:encoded_launch_name>/", views.launch_details, name="launch"),
    path("launches/", views.launches_list, name="launches"),
    path("dragons/<str:dragon_name>/", views.dragon_info, name="dragon"),
    path("dragons/", views.dragon_list, name="dragons"),
    path("starship/", views.starship_home, name="starship"),
    path(
        "<str:rocket_family>/<str:stage_type>/<str:stage_name>/",
        views.stage_info,
        name="stage",
    ),
    path("<str:rocket_family_name>/<str:stage_type>/", views.stage_list, name="stages"),
]
