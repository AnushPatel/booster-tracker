from django.urls import path
from booster_tracker import views
from booster_tracker.api_views import (
    LaunchOnlyApiView,
    LaunchApiView,
    RocketApiView,
    RocketFamilyApiView,
    OperatorApiView,
    OrbitApiView,
    PadApiView,
    PadInformationApiView,
    LandingZoneApiView,
    LandingZoneInformationApiView,
    StageAndRecoveryApiView,
    LaunchInformationApiView,
    StageApiView,
    StageInformationApiView,
    SpacecraftApiView,
    SpacecraftInformationApiView,
    BoatApiView,
    SpacecraftFamilyApiView,
    HomeDataApiView,
    FamilyInformationApiView,
    FilteredLaunchDaysApiView,
)

app_name = "booster_tracker"
urlpatterns = [
    # API Endpoints
    path("api/homedata/", HomeDataApiView.as_view(), name="home"),
    path("api/launchesonly/", LaunchOnlyApiView.as_view(), name="launches_only"),
    path("api/launches/", LaunchApiView.as_view(), name="launches"),
    path("api/stages/", StageApiView.as_view(), name="stages"),
    path("api/stageinformation/", StageInformationApiView.as_view(), name="stage_information"),
    path("api/spacecraft/", SpacecraftApiView.as_view(), name="spacecraft"),
    path("api/spacecraftfamilies/", SpacecraftFamilyApiView.as_view(), name="spacecraft_families"),
    path("api/spacecraftinformation/", SpacecraftInformationApiView.as_view(), name="spacecraft_information"),
    path("api/launchinfo/", LaunchInformationApiView.as_view(), name="launch_information"),
    path("api/rockets/", RocketApiView.as_view(), name="rockets"),
    path("api/rocketfamilies/", RocketFamilyApiView.as_view(), name="rocket_families"),
    path("api/familyinformation/", FamilyInformationApiView.as_view(), name="family_information"),
    path("api/operators/", OperatorApiView.as_view(), name="operators"),
    path("api/orbit/", OrbitApiView.as_view(), name="orbit"),
    path("api/pads/", PadApiView.as_view(), name="pads"),
    path("api/padinformation/", PadInformationApiView.as_view(), name="pad_information"),
    path("api/boats/", BoatApiView.as_view(), name="boats"),
    path("api/landingzones/", LandingZoneApiView.as_view(), name="landing_zones"),
    path("api/landingzoneinformation/", LandingZoneInformationApiView.as_view(), name="landing_zone_information"),
    path("api/stageandrecoveries/", StageAndRecoveryApiView.as_view(), name="stage_and_recoveries"),
    path("api/calendarstats/", FilteredLaunchDaysApiView.as_view(), name="filter_calendar_stats"),
    # v1 views
    path("health/", views.health, name="health"),
]
