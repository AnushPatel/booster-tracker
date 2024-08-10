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
            "boosters",
            "recoveries",
            "image",
        ]


class RocketSerializer(serializers.ModelSerializer):
    launches = LaunchOnlySerializer(many=True, read_only=True, source="launch_set")

    class Meta:
        model = Rocket
        fields = "__all__"


class RocketOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rocket
        fields = "__all__"


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


class SpacecraftOnLaunchSerializer(serializers.ModelSerializer):
    launch = LaunchOnlySerializer(read_only=True)

    class Meta:
        model = SpacecraftOnLaunch
        fields = "__all__"


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
    remaining_launches_current_year = serializers.IntegerField()
    total_launches_current_year = serializers.IntegerField()
    total_launches_next_year = serializers.IntegerField()
    total_launches_year_after_next = serializers.IntegerField()
    next_launch = LaunchSerializer()
    last_launch = LaunchSerializer()
    num_missions = serializers.IntegerField()
    num_successes = serializers.IntegerField()
    num_landings = serializers.IntegerField()
    shortest_time_between_launches = serializers.CharField()
    num_stage_reflights = serializers.CharField()


class FamilyInformationSerializer(serializers.Serializer):
    launch_years = serializers.ListField(child=serializers.IntegerField())
    series_data = serializers.DictField(child=serializers.ListField(child=serializers.IntegerField()), required=False)
    stats = serializers.DictField(child=serializers.CharField(), required=True)
    children_stats = serializers.DictField(child=serializers.CharField(), required=True)
    boosters_with_most_flights = serializers.ListField(child=StageSerializer(), required=True)
    booster_max_num_flights = serializers.IntegerField(required=True)
    stage_two_with_most_flights = serializers.ListField(child=StageSerializer(), required=True)
    stage_two_max_num_flights = serializers.IntegerField(required=True)
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
