from django.urls import path
from booster_tracker import views

app_name = "booster_tracker"
urlpatterns = [
    path("", views.home, name="home"),
    path("launches/<str:launch_name>/", views.launch_details, name="launch"),
    path("launches/", views.launches_list, name="launches"),
    path("boosters/falcon/<str:booster_name>/", views.booster_info, name="booster"),
    path("boosters/", views.booster_list, name="boosters"),
    path("dragons/<str:dragon_name>/", views.dragon_info, name="dragon"),
    path("dragons/", views.dragon_list, name="dragons"),
]
