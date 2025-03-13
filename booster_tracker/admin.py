from django.contrib import admin
from django.db.models import Q
from django.templatetags.static import static
from datetime import datetime
import pytz
from booster_tracker.models import (
    StageAndRecovery,
    Stage,
    LandingZone,
    TugOnLaunch,
    Boat,
    SupportOnLaunch,
    Spacecraft,
    SpacecraftFamily,
    SpacecraftOnLaunch,
    PadUsed,
    Pad,
    Launch,
    FairingRecovery,
    Rocket,
    Orbit,
    Operator,
    RocketFamily,
    LaunchStat,
)

## test

# Register your models here.
# pylint: disable=consider-using-set-comprehension


class LaunchStatInLine(admin.TabularInline):
    model = LaunchStat
    extra = 0


class StageRecoveryInLine(admin.TabularInline):
    model = StageAndRecovery
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            launch_instance = self.parent_model.objects.get(pk=request.resolver_match.kwargs["object_id"])
        except (AttributeError, KeyError, self.parent_model.DoesNotExist):
            launch_instance = None
        if not launch_instance or launch_instance.time > datetime.now(pytz.UTC):
            if db_field.name == "stage":
                kwargs["queryset"] = Stage.objects.filter(status="ACTIVE")
            if db_field.name == "landing_zone":
                kwargs["queryset"] = LandingZone.objects.filter(status="ACTIVE")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FairingRecoveryInLine(admin.TabularInline):
    model = FairingRecovery
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            launch_instance = self.parent_model.objects.get(pk=request.resolver_match.kwargs["object_id"])
        except (AttributeError, KeyError, self.parent_model.DoesNotExist):
            launch_instance = None
        if not launch_instance or launch_instance.time > datetime.now(pytz.UTC):
            if db_field.name == "boat":
                kwargs["queryset"] = Boat.objects.filter(status="ACTIVE", type="FAIRING_RECOVERY")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TugInLine(admin.TabularInline):
    model = TugOnLaunch
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            launch_instance = self.parent_model.objects.get(pk=request.resolver_match.kwargs["object_id"])
        except (AttributeError, KeyError, self.parent_model.DoesNotExist):
            launch_instance = None
        if not launch_instance or launch_instance.time > datetime.now(pytz.UTC):
            if db_field.name == "boat":
                kwargs["queryset"] = Boat.objects.filter(status="ACTIVE", type="TUG")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SupportInLine(admin.TabularInline):
    model = SupportOnLaunch
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            launch_instance = self.parent_model.objects.get(pk=request.resolver_match.kwargs["object_id"])
        except (AttributeError, KeyError, self.parent_model.DoesNotExist):
            launch_instance = None
        if not launch_instance or launch_instance.time > datetime.now(pytz.UTC):
            if db_field.name == "boat":
                kwargs["queryset"] = Boat.objects.filter(status="ACTIVE", type="SUPPORT")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DragonInLine(admin.TabularInline):
    model = SpacecraftOnLaunch
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            launch_instance = self.parent_model.objects.get(pk=request.resolver_match.kwargs["object_id"])
        except (AttributeError, KeyError, self.parent_model.DoesNotExist):
            launch_instance = None
        if not launch_instance or launch_instance.time > datetime.now(pytz.UTC):
            if db_field.name == "spacecraft":
                kwargs["queryset"] = Spacecraft.objects.filter(status="ACTIVE")
            if db_field.name == "recovery_boat":
                kwargs["queryset"] = Boat.objects.filter(status="ACTIVE", type="SPACECRAFT_RECOVERY")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PadInLine(admin.TabularInline):
    model = PadUsed
    extra = 0


class RocketFilter(admin.SimpleListFilter):
    title = "Rocket"
    parameter_name = "rocket"

    def lookups(self, request, model_admin):
        rockets = set([launch.rocket for launch in Launch.objects.all()])
        return [(rocket, rocket) for rocket in rockets]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rocket__name=self.value())
        return queryset


class StageNameFilter(admin.SimpleListFilter):
    title = "Stage Name"
    parameter_name = "stage_name"

    def lookups(self, request, model_admin):
        stage_names = set([stage.stage for stage in StageAndRecovery.objects.all()])
        return [(stage_name, stage_name) for stage_name in stage_names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stageandrecovery__stage__name=self.value())
        return queryset


class PadFilter(admin.SimpleListFilter):
    title = "Pad"
    parameter_name = "pad"

    def lookups(self, request, model_admin):
        pads = set([launch.pad for launch in Launch.objects.all()])
        return [(pad, pad) for pad in pads]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(pad__nickname=self.value())
        return queryset


class LandingLocationFilter(admin.SimpleListFilter):
    title = "Landing Location"
    parameter_name = "landing_zone"

    def lookups(self, request, model_admin):
        landing_zones = set([landing_zone.landing_zone for landing_zone in StageAndRecovery.objects.all()])
        return [(landing_zone, landing_zone) for landing_zone in landing_zones]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stageandrecovery__landing_zone__name=self.value())
        return queryset


class LaunchOutcomeFilter(admin.SimpleListFilter):
    title = "Launch Outcome"
    parameter_name = "launch_outcome"

    def lookups(self, request, model_admin):
        launch_outcomes = set([launch.launch_outcome for launch in Launch.objects.all()])
        return [(launch_outcome, launch_outcome) for launch_outcome in launch_outcomes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(launch_outcome=self.value())
        return queryset


class OrbitFilter(admin.SimpleListFilter):
    title = "Orbit"
    parameter_name = "orbit"

    def lookups(self, request, model_admin):
        orbits = set([launch.orbit for launch in Launch.objects.all()])
        return [(orbit, orbit) for orbit in orbits]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(orbit__name=self.value())
        return queryset


class LandingMethodFilter(admin.SimpleListFilter):
    title = "Landing Method"
    parameter_name = "method"

    def lookups(self, request, model_admin):
        landing_methods = set([method.method for method in StageAndRecovery.objects.all()])
        return [(method, method) for method in landing_methods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stageandrecovery__method=self.value())
        return queryset


class LandingOutcomeFilter(admin.SimpleListFilter):
    title = "Booster Recovery Outcome"
    parameter_name = "recovery_success"

    def lookups(self, request, model_admin):
        # Get distinct recovery outcomes
        recovery_outcomes = (
            StageAndRecovery.objects.values_list("recovery_success", flat=True).order_by("recovery_success").distinct()
        )
        # Convert boolean values to human-readable strings
        return [(str(outcome), "Success" if outcome else "Failure") for outcome in recovery_outcomes]

    def queryset(self, request, queryset):
        if self.value() is not None:
            # Filter based on selected recovery outcome
            return queryset.filter(stageandrecovery__recovery_success=self.value())
        return queryset


class MethodSuccessFilter(admin.SimpleListFilter):
    title = "Booster Method Outcome"
    parameter_name = "method_success"

    def lookups(self, request, model_admin):
        # Get distinct method success values
        method_success_values = (
            StageAndRecovery.objects.values_list("method_success", flat=True).order_by("method_success").distinct()
        )
        # Convert boolean values to human-readable strings
        return [
            (
                str(value),
                ("Success" if value == "SUCCESS" else "Precluded" if value == "PRECLUDED" else "Failure"),
            )
            for value in method_success_values
        ]

    def queryset(self, request, queryset):
        if self.value() is not None and not self.value() == "None":
            # Filter based on selected method success
            return queryset.filter(stageandrecovery__method_success=self.value())
        return queryset


class FairingMethodFilter(admin.SimpleListFilter):
    title = "Fairing Catch"
    parameter_name = "catch"

    def lookups(self, request, model_admin):
        recovery_methods = set([method.catch for method in FairingRecovery.objects.all()])
        return [(method, method) for method in recovery_methods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(fairingrecovery__catch=self.value())
        return queryset


class FairingRecoveryOutcome(admin.SimpleListFilter):
    title = "Fairing Recovery Outcome"
    parameter_name = "recovery"

    def lookups(self, request, model_admin):
        recovery_outcomes = set([recovery.recovery for recovery in FairingRecovery.objects.all()])
        return [(recovery, recovery) for recovery in recovery_outcomes]

    def queryset(self, request, queryset):
        if self.value() is not None:
            # Filter based on selected recovery outcome
            return queryset.filter(fairingrecovery__recovery=self.value())
        return queryset


class BoosterLocationMissingFilter(admin.SimpleListFilter):
    title = "Booster Location Missing"
    parameter_name = "location_missing"

    def lookups(self, request, model_admin):
        return (
            ("true", "Yes"),
            ("false", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "true":
            # Filter for missions that have missing latitude or longitude
            return queryset.filter(stageandrecovery__latitude__isnull=True) | queryset.filter(
                stageandrecovery__longitude__isnull=True
            )
        if self.value() == "false":
            # Filter for missions that have both latitude and longitude
            return queryset.exclude(stageandrecovery__latitude__isnull=True) & queryset.exclude(
                stageandrecovery__longitude__isnull=True
            )
        return queryset


class FairingLocationMissingFilter(admin.SimpleListFilter):
    title = "Fairing Location Missing"
    parameter_name = "fairing_location_missing"

    def lookups(self, request, model_admin):
        return (
            ("true", "Yes"),
            ("false", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "true":
            # Filter for missions that have missing latitude or longitude
            return queryset.filter(fairingrecovery__latitude__isnull=True) | queryset.filter(
                fairingrecovery__longitude__isnull=True
            )

        if self.value() == "false":
            # Filter for missions that have both latitude and longitude
            return queryset.exclude(fairingrecovery__latitude__isnull=True) & queryset.exclude(
                fairingrecovery__longitude__isnull=True
            )
        return queryset


class LaunchAdmin(admin.ModelAdmin):
    inlines = [
        StageRecoveryInLine,
        FairingRecoveryInLine,
        TugInLine,
        SupportInLine,
        LaunchStatInLine,
        DragonInLine,
    ]
    readonly_fields = ("celery_task_id",)  # Make the field read-only in the edit form

    class Media:
        js = ("js/landingzones.js",)

    def custom_time_display(self, obj):
        return obj.time.strftime("%B %d, %Y %H:%M")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            launch_instance = Launch.objects.get(pk=request.resolver_match.kwargs.get("object_id"))
        except (AttributeError, KeyError, Launch.DoesNotExist):
            launch_instance = None
        if not launch_instance or launch_instance.time > datetime.now(pytz.UTC):
            if db_field.name == "rocket":
                kwargs["queryset"] = Rocket.objects.filter(status="ACTIVE")
            if db_field.name == "pad":
                kwargs["queryset"] = Pad.objects.filter(status="ACTIVE")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ["name", "custom_time_display", "pad"]
    list_filter = (
        RocketFilter,
        PadFilter,
        LandingMethodFilter,
        LandingLocationFilter,
        LandingOutcomeFilter,
        MethodSuccessFilter,
        LaunchOutcomeFilter,
        FairingMethodFilter,
        FairingRecoveryOutcome,
        OrbitFilter,
        StageNameFilter,
        BoosterLocationMissingFilter,
        FairingLocationMissingFilter,
    )
    search_fields = ["name"]


class VersionFilter(admin.SimpleListFilter):
    title = "Version"
    parameter_name = "version"

    def lookups(self, request, model_admin):
        versions = set([stage.version for stage in Stage.objects.all()])
        return [(version, version) for version in versions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(version=self.value())
        return queryset


class StageTypeFilter(admin.SimpleListFilter):
    title = "Type"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        types = set([stage.type for stage in Stage.objects.all()])
        return [(type, type) for type in types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        return queryset


class StageStatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        statuses = set([stage.status for stage in Stage.objects.all()])
        return [(status, status) for status in statuses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class StageAdmin(admin.ModelAdmin):
    list_display = ["name", "rocket", "version", "type", "status"]
    list_filter = [RocketFilter, VersionFilter, StageTypeFilter, StageStatusFilter]
    search_fields = ["name"]


class RocketAdmin(admin.ModelAdmin):
    inlines = [PadInLine]


class BoatTypeFilter(admin.SimpleListFilter):
    title = "Type"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        types = set([boat.type for boat in Boat.objects.all()])
        return [(type, type) for type in types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        return queryset


class BoatStatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        statuses = set([boat.status for boat in Boat.objects.all()])
        return [(status, status) for status in statuses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class BoatAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "status"]
    list_filter = [BoatTypeFilter, BoatStatusFilter]
    search_fields = ["name"]


admin.site.site_header = "Booster Tracker"
admin.site.site_title = "Booster Tracker Admin"
admin.site.index_title = "Welcome to the Booster Tracker Admin Panel!"
admin.site.register(Launch, LaunchAdmin)
admin.site.register(Rocket, RocketAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Boat, BoatAdmin)
admin.site.register(Orbit)
admin.site.register(LandingZone)
admin.site.register(Pad)
admin.site.register(SpacecraftFamily)
admin.site.register(Spacecraft)
admin.site.register(Operator)
admin.site.register(RocketFamily)
