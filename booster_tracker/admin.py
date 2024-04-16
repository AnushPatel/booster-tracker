from typing import Any
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from functools import reduce

from django.db.models.query import QuerySet
from .models import *
# Register your models here.

class StageRecoveryInLine(admin.TabularInline):
    model = StageAndRecovery
    extra = 0

class FairingRecoveryInLine(admin.TabularInline):
    model = FairingRecovery
    extra = 0

class TugInLine(admin.TabularInline):
    model = TugOnLaunch
    extra = 0

class SupportInLine(admin.TabularInline):
    model = SupportOnLaunch
    extra = 0

class DragonInLine(admin.TabularInline):
    model = DragonOnLaunch
    extra = 0

class RocketFilter(admin.SimpleListFilter):
    title = 'Rocket'
    parameter_name = 'rocket'

    def lookups(self, request, model_admin):
        rockets = set([launch.rocket for launch in Launch.objects.all()])
        return [(rocket, rocket) for rocket in rockets]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rocket__name=self.value())
        else:
            return queryset

class StageNameFilter(admin.SimpleListFilter):
    title = 'Stage Name'
    parameter_name = 'stage_name'

    def lookups(self, request, model_admin):
        stage_names = set([stage.stage for stage in StageAndRecovery.objects.all()])
        return [(stage_name, stage_name) for stage_name in stage_names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stageandrecovery__stage__name=self.value())
        else:
            return queryset

class PadFilter(admin.SimpleListFilter):
    title = 'Pad'
    parameter_name = 'pad'

    def lookups(self, request, model_admin):
        pads = set([launch.pad for launch in Launch.objects.all()])
        return [(pad, pad) for pad in pads]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(pad__nickname=self.value())
        else:
            return queryset

class LandingLocationFilter(admin.SimpleListFilter):
    title = 'Landing Location'
    parameter_name = 'landing_zone'

    def lookups(self, request, model_admin):
        landing_zones = set([landing_zone.landing_zone for landing_zone in StageAndRecovery.objects.all()])
        return [(landing_zone, landing_zone) for landing_zone in landing_zones]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stageandrecovery__landing_zone__name=self.value())
        else:
            return queryset
        
class LaunchOutcomeFilter(admin.SimpleListFilter):
    title = 'Launch Outcome'
    parameter_name = 'launch_outcome'

    def lookups(self, request, model_admin):
        launch_outcomes = set([launch.launch_outcome for launch in Launch.objects.all()])
        return [(launch_outcome, launch_outcome) for launch_outcome in launch_outcomes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(launch_outcome=self.value())
        else:
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
        else:
            return queryset
        
class LandingMethodFilter(admin.SimpleListFilter):
    title = 'Landing Method'
    parameter_name = 'method'

    def lookups(self, request, model_admin):
        landing_methods = set([method.method for method in StageAndRecovery.objects.all()])
        return [(method, method) for method in landing_methods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stageandrecovery__method=self.value())
        else:
            return queryset
    
class LandingOutcomeFilter(admin.SimpleListFilter):
    title = 'Booster Recovery Outcome'
    parameter_name = 'recovery_success'

    def lookups(self, request, model_admin):
        # Get distinct recovery outcomes
        recovery_outcomes = StageAndRecovery.objects.values_list('recovery_success', flat=True).distinct()
        # Convert boolean values to human-readable strings
        return [(str(outcome), "Success" if outcome else "Failure") for outcome in recovery_outcomes]

    def queryset(self, request, queryset):
        if self.value() is not None:
            # Filter based on selected recovery outcome
            return queryset.filter(stageandrecovery__recovery_success=self.value())
        else:
            return queryset

class MethodSuccessFilter(admin.SimpleListFilter):
    title = 'Booster Method Outcome'
    parameter_name = 'method_success'

    def lookups(self, request, model_admin):
        # Get distinct method success values
        method_success_values = StageAndRecovery.objects.values_list('method_success', flat=True).distinct()
        # Convert boolean values to human-readable strings
        return [(str(value), "Success" if value else "Failure") for value in method_success_values]

    def queryset(self, request, queryset):
        if self.value() is not None and not self.value() == "None":
            # Filter based on selected method success
            return queryset.filter(stageandrecovery__method_success=self.value())
        else:
            return queryset

class FairingMethodFilter(admin.SimpleListFilter):
    title = 'Fairing Catch'
    parameter_name = 'catch'

    def lookups(self, request, model_admin):
        recovery_methods = set([method.catch for method in FairingRecovery.objects.all()])
        return [(method, method) for method in recovery_methods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(fairingrecovery__catch=self.value())
        else:
            return queryset

class FairingRecoveryOutcome(admin.SimpleListFilter):
    title = 'Fairing Recovery Outcome'
    parameter_name = 'recovery'

    def lookups(self, request, model_admin):
        recovery_outcomes = set([recovery.recovery for recovery in FairingRecovery.objects.all()])
        return [(recovery, recovery) for recovery in recovery_outcomes]

    def queryset(self, request, queryset):
        if self.value() is not None:
            # Filter based on selected recovery outcome
            return queryset.filter(fairingrecovery__recovery=self.value())
        else:
            return queryset
        
class BoosterLocationMissingFilter(admin.SimpleListFilter):
    title = 'Booster Location Missing'
    parameter_name = 'location_missing'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Yes'),
            ('false', 'No'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'true':
            # Filter for missions that have missing latitude or longitude
            return queryset.filter(stageandrecovery__latitude__isnull=True) | queryset.filter(stageandrecovery__longitude__isnull=True)
        elif self.value() == 'false':
            # Filter for missions that have both latitude and longitude
            return queryset.exclude(stageandrecovery__latitude__isnull=True) & queryset.exclude(stageandrecovery__longitude__isnull=True)
        else:
            return queryset

class FairingLocationMissingFilter(admin.SimpleListFilter):
    title = 'Fairing Location Missing'
    parameter_name = 'location_missing'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Yes'),
            ('false', 'No'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'true':
            # Filter for missions that have missing latitude or longitude
            return queryset.filter(fairingrecovery__latitude__isnull=True) | queryset.filter(fairingrecovery__longitude__isnull=True)
        elif self.value() == 'false':
            # Filter for missions that have both latitude and longitude
            return queryset.exclude(fairingrecovery__latitude__isnull=True) & queryset.exclude(fairingrecovery__longitude__isnull=True)
        else:
            return queryset

class LaunchAdmin(admin.ModelAdmin):
    inlines = [StageRecoveryInLine, FairingRecoveryInLine, TugInLine, SupportInLine, DragonInLine]

    def custom_time_display(self, obj):
        return obj.time.strftime("%B %d, %Y %H:%M")
    
    list_display = ["name", "custom_time_display", "pad"]
    list_filter = (RocketFilter, PadFilter, LandingMethodFilter, LandingLocationFilter, LandingOutcomeFilter, MethodSuccessFilter, LaunchOutcomeFilter,
                   FairingMethodFilter, FairingRecoveryOutcome, OrbitFilter, StageNameFilter, BoosterLocationMissingFilter, FairingLocationMissingFilter)
    search_fields = ["name"]


class VersionFilter(admin.SimpleListFilter):
    title = 'Version'
    parameter_name = 'version'

    def lookups(self, request, model_admin):
        versions = set([stage.version for stage in Stage.objects.all()])
        return [(version, version) for version in versions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(version=self.value())
        else:
            return queryset

class StageTypeFilter(admin.SimpleListFilter):
    title = 'Type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        types = set([stage.type for stage in Stage.objects.all()])
        return [(type, type) for type in types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        else:
            return queryset

class StageAdmin(admin.ModelAdmin):
    list_display = ["name", "rocket", "version", "type"]
    list_filter = [RocketFilter, VersionFilter, StageTypeFilter]
    search_fields = ["name"]

class BoatTypeFilter(admin.SimpleListFilter):
    title = 'Type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        types = set([boat.type for boat in Boat.objects.all()])
        return [(type, type) for type in types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        else:
            return queryset

class BoatAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]
    list_filter = [BoatTypeFilter]
    search_fields = ["name"]

admin.site.register(Launch, LaunchAdmin)
admin.site.register(Rocket)
admin.site.register(Stage, StageAdmin)
admin.site.register(Boat, BoatAdmin)
admin.site.register(Orbit)
admin.site.register(LandingZone)
admin.site.register(Pad)
admin.site.register(Dragon)