from rest_framework import serializers
from .models import (
    Orbit,
    StageAndRecovery,
    Launch,
    Rocket,
    RocketFamily,
    Operator,
    Pad,
    LandingZone,
    Stage,
    Spacecraft,
    SpacecraftOnLaunch,
    Boat,
    SpacecraftFamily,
)
from .utils import convert_seconds
from datetime import datetime


class OrbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orbit
        fields = "__all__"


class LaunchOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Launch
        fields = [
            "id",
            "time",
            "name",
            "mass",
            "customer",
            "launch_outcome",
            "pad_turnaround",
            "company_turnaround",
            "pad",
            "rocket",
            "orbit",
            "image",
        ]


class StageAndRecoverySerializer(serializers.ModelSerializer):
    launch = LaunchOnlySerializer(read_only=True)

    class Meta:
        model = StageAndRecovery
        fields = "__all__"


class LaunchSerializer(serializers.ModelSerializer):
    recoveries = StageAndRecoverySerializer(many=True, read_only=True, source="stageandrecovery_set")

    class Meta:
        model = Launch
        fields = [
            "id",
            "time",
            "name",
            "mass",
            "customer",
            "launch_outcome",
            "pad_turnaround",
            "company_turnaround",
            "pad",
            "rocket",
            "orbit",
            "stages_string",
            "recoveries",
            "image",
        ]


class RocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rocket
        fields = ["id", "name", "status", "color", "family", "image"]


class RocketFamilySerializer(serializers.ModelSerializer):
    rockets = RocketSerializer(many=True, read_only=True, source="rocket_set")

    class Meta:
        model = RocketFamily
        fields = "__all__"


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = "__all__"


class PadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pad
        fields = [
            "id",
            "name",
            "nickname",
            "location",
            "status",
            "image",
            "num_launches",
            "fastest_turnaround",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["fastest_turnaround"] = convert_seconds(instance.fastest_turnaround)

        return representation


class PadInformationSerializer(serializers.Serializer):
    launches = serializers.ListField(child=LaunchOnlySerializer())
    display_launches = serializers.ListField(child=LaunchOnlySerializer())
    pad = PadSerializer()
    start_date = serializers.DateTimeField()


class LandingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingZone
        fields = [
            "id",
            "name",
            "nickname",
            "type",
            "serial_number",
            "status",
            "image",
            "num_landings",
            "fastest_turnaround",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["fastest_turnaround"] = convert_seconds(instance.fastest_turnaround)

        return representation


class LandingZoneInformationSerializer(serializers.Serializer):
    stage_and_recoveries = serializers.ListField(child=StageAndRecoverySerializer())
    display_stage_and_recoveries = serializers.ListField(child=StageAndRecoverySerializer())
    landing_zone = LandingZoneSerializer()
    start_date = serializers.DateTimeField()


class LaunchInformationSerializer(serializers.ModelSerializer):
    create_launch_table = serializers.SerializerMethodField()

    class Meta:
        model = Launch
        fields = ["name", "rocket", "image", "create_launch_table"]

    def get_create_launch_table(self, obj):
        return obj.create_launch_table()


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["id", "name", "version", "type", "image", "status", "rocket", "num_launches"]


class StageAndRecoveryOnlySerializer(serializers.ModelSerializer):
    stage = StageSerializer(read_only=True)
    landing_zone = LandingZoneSerializer(read_only=True)
    stage_stats = serializers.SerializerMethodField()
    landing_zone_stats = serializers.SerializerMethodField()

    class Meta:
        model = StageAndRecovery
        fields = [
            "id",
            "stage_position",
            "method",
            "method_success",
            "recovery_success",
            "latitude",
            "longitude",
            "stage",
            "num_flights",
            "stage_turnaround",
            "zone_turnaround",
            "stage_stats",
            "landing_zone",
            "landing_zone_stats",
            "num_recoveries",
        ]

    def get_stage_stats(self, obj):
        return obj.get_stage_stats()

    def get_landing_zone_stats(self, obj):
        return obj.get_landing_zone_stats()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["stage_turnaround"] = convert_seconds(instance.stage_turnaround)
        representation["zone_turnaround"] = convert_seconds(instance.zone_turnaround)

        return representation


class StageListSerializer(serializers.Serializer):
    start_filter = serializers.DictField(child=serializers.CharField(), required=True)
    stages = serializers.ListField(child=StageSerializer())


class StageInformationSerializer(serializers.Serializer):
    stage_and_recoveries = serializers.ListField(child=StageAndRecoverySerializer())
    display_stage_and_recoveries = serializers.ListField(child=StageAndRecoverySerializer())
    stage = StageSerializer()
    start_date = serializers.DateTimeField()


class SpacecraftFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpacecraftFamily
        fields = "__all__"


class SpacecraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spacecraft
        fields = ["id", "name", "nickname", "version", "type", "status", "image", "family", "num_launches"]


class SpacecraftListSerializer(serializers.Serializer):
    start_filter = serializers.DictField(child=serializers.CharField(), required=True)
    spacecraft = serializers.ListField(child=SpacecraftSerializer())


class SpacecraftOnLaunchSerializer(serializers.ModelSerializer):
    launch = LaunchOnlySerializer(read_only=True)

    class Meta:
        model = SpacecraftOnLaunch
        fields = "__all__"


class SpacecraftOnLaunchOnlySerializer(serializers.ModelSerializer):
    spacecraft_stats = serializers.SerializerMethodField()

    class Meta:
        model = SpacecraftOnLaunch
        fields = "__all__"

    def get_spacecraft_stats(self, obj: SpacecraftOnLaunch):
        return obj.get_spacecraft_stats()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["spacecraft_turnaround"] = convert_seconds(instance.spacecraft_turnaround)

        return representation


class SpacecraftInformationSerializer(serializers.Serializer):
    spacecraft = SpacecraftSerializer()
    spacecraft_on_launches = serializers.ListField(child=SpacecraftOnLaunchSerializer())
    display_spacecraft_on_launches = serializers.ListField(child=SpacecraftOnLaunchSerializer())
    start_date = serializers.DateTimeField()


class BoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boat
        fields = "__all__"


class HomePageSerializer(serializers.Serializer):
    turnaround_x_values = serializers.ListField(child=serializers.FloatField())
    turnaround_data = serializers.ListField(child=serializers.FloatField())
    best_fit_turnaround_values = serializers.ListField(child=serializers.FloatField())
    chunk_size = serializers.IntegerField()
    total_launches_current_year = serializers.IntegerField()
    total_launches_next_year = serializers.IntegerField()
    next_launch = LaunchSerializer()
    last_launch = LaunchSerializer()
    num_missions = serializers.IntegerField()
    num_successes = serializers.IntegerField()
    num_landings = serializers.IntegerField()
    shortest_time_between_launches = serializers.CharField()
    num_stage_reflights = serializers.CharField()
    years = serializers.ListField(child=serializers.IntegerField())
    launches_per_rocket_per_year = serializers.DictField(child=serializers.CharField())


class RocketFamilyInformationSerializer(serializers.Serializer):
    launch_years = serializers.ListField(child=serializers.IntegerField())
    series_data = serializers.DictField(child=serializers.ListField(child=serializers.FloatField()), required=False)
    stats = serializers.DictField(child=serializers.CharField(), required=True)
    children_stats = serializers.DictField(child=serializers.CharField(), required=True)
    boosters_with_most_flights = serializers.ListField(child=StageSerializer(), required=True)
    stage_two_with_most_flights = serializers.ListField(child=StageSerializer(), required=True)
    booster_with_quickest_turnaround = StageSerializer(required=False, allow_null=True)
    booster_turnaround_time = serializers.CharField(required=False, allow_null=True)
    stage_two_with_quickest_turnaround = StageSerializer(required=False, allow_null=True)
    stage_two_turnaround_time = serializers.CharField(required=False, allow_null=True)

    max_booster_flights = serializers.ListField(child=serializers.IntegerField(), required=False)
    max_stage_two_flights = serializers.ListField(child=serializers.IntegerField(), required=False)
    avg_booster_flights = serializers.ListField(child=serializers.FloatField(), required=False)
    avg_stage_two_flights = serializers.ListField(child=serializers.FloatField(), required=False)
    max_fairing_flights = serializers.ListField(child=serializers.FloatField(), required=False)

    start_date = serializers.DateTimeField()


class SpacecraftFamilyInformationSerializer(serializers.Serializer):
    launch_years = serializers.ListField(child=serializers.IntegerField())
    series_data = serializers.DictField(child=serializers.ListField(child=serializers.FloatField()), required=False)
    stats = serializers.DictField(child=serializers.CharField(), required=True)
    children_stats = serializers.DictField(child=serializers.CharField(), required=True)
    spacecraft_with_most_flights = serializers.ListField(child=SpacecraftSerializer(), required=True)
    spacecraft_with_quickest_turnaround = SpacecraftSerializer(required=False, allow_null=True)
    spacecraft_turnaround_time = serializers.CharField(required=False, allow_null=True)

    max_spacecraft_flights = serializers.ListField(child=serializers.IntegerField(), required=False)
    avg_spacecraft_flights = serializers.ListField(child=serializers.FloatField(), required=False)

    start_date = serializers.DateTimeField()


class CalendarStatsSerializer(serializers.Serializer):
    num_days_with_launches = serializers.IntegerField()
    percentage_days_with_launches = serializers.FloatField()
    most_launches = serializers.IntegerField()
    days_with_most_launches = serializers.CharField()
    launches = serializers.ListField(child=LaunchOnlySerializer())


class EDATableSerializer(serializers.Serializer):
    launch_table = serializers.CharField()


class AdditionalGraphSerializer(serializers.Serializer):
    mass_per_year = serializers.DictField(child=serializers.CharField())


class LaunchInformation2Serializer(serializers.ModelSerializer):
    stage_and_recoveries = StageAndRecoveryOnlySerializer(many=True, read_only=True, source="stageandrecovery_set")
    spacecraft_on_launch = SpacecraftOnLaunchOnlySerializer(many=True, read_only=True, source="spacecraftonlaunch_set")
    rocket_stats = serializers.SerializerMethodField()
    launch_provider_stats = serializers.SerializerMethodField()
    launch_pad_stats = serializers.SerializerMethodField()
    significant_stats = serializers.SerializerMethodField()


class LaunchProgressSerializer(serializers.Serializer):  # Serialzier for Launch Progress chart, do not commit to prod.
    years = serializers.ListField(child=serializers.IntegerField())
    actual_launches = serializers.ListField(child=serializers.IntegerField())
    target_launches = serializers.ListField(child=serializers.IntegerField())
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    target_goal = serializers.IntegerField()
    current_progress = serializers.IntegerField()

    class Meta:
        model = Launch
        fields = [
            "id",
            "stage_and_recoveries",
            "spacecraft_on_launch",
            "rocket_stats",
            "launch_provider_stats",
            "launch_pad_stats",
            "significant_stats",
            "time",
            "name",
            "mass",
            "customer",
            "launch_outcome",
            "pad_turnaround",
            "company_turnaround",
            "image",
            "pad",
            "rocket",
            "orbit",
        ]

    def get_rocket_stats(self, obj: Launch):
        return obj.get_rocket_stats()

    def get_launch_provider_stats(self, obj: Launch):
        return obj.get_launch_provider_stats()

    def get_launch_pad_stats(self, obj: Launch):
        return obj.get_launch_pad_stats()

    def get_significant_stats(self, obj: Launch):
        return obj.make_stats()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["pad_turnaround"] = convert_seconds(instance.pad_turnaround)
        representation["company_turnaround"] = convert_seconds(instance.company_turnaround)

        return representation
