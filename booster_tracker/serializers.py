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
        fields = ["id", "time", "name", "mass", "customer", "launch_outcome", "pad", "rocket", "orbit", "image"]


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
            "time",
            "pad",
            "rocket",
            "name",
            "launch_outcome",
            "id",
            "image",
            "recoveries",
            "boosters",
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
        fields = "__all__"


class LandingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingZone
        fields = "__all__"


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


class StageInformationSerializer(serializers.ModelSerializer):
    stage_and_recovery = StageAndRecoverySerializer(many=True, read_only=True, source="stageandrecovery_set")

    class Meta:
        model = Stage
        fields = ["id", "name", "version", "type", "image", "status", "rocket", "stage_and_recovery", "num_launches"]


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


class SpacecraftInformationSerializer(serializers.ModelSerializer):
    spacecraft_on_launch = SpacecraftOnLaunchSerializer(many=True, read_only=True, source="spacecraftonlaunch_set")

    class Meta:
        model = Spacecraft
        fields = [
            "id",
            "name",
            "nickname",
            "version",
            "type",
            "image",
            "status",
            "family",
            "spacecraft_on_launch",
        ]


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
    max_reflight_num = serializers.DictField(child=serializers.IntegerField())
    avg_reflight_num = serializers.ListField(child=serializers.FloatField())
    max_fairing_flights = serializers.ListField(child=serializers.FloatField())
    stats = serializers.DictField(child=serializers.CharField())
    children_stats = serializers.DictField(child=serializers.CharField())
    boosters_with_most_flights = serializers.ListField(child=StageInformationSerializer())
    booster_max_num_flights = serializers.IntegerField()
    stage_two_with_most_flights = serializers.ListField(child=StageInformationSerializer())
    stage_two_max_num_flights = serializers.IntegerField()
    booster_with_quickest_turnaround = StageInformationSerializer()
    booster_turnaround_time = serializers.CharField()
    stage_two_with_quickest_turnaround = StageInformationSerializer()
    stage_two_turnaround_time = serializers.CharField()
