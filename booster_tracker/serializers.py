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
        fields = [
            "launch",
            "stage_position",
            "method",
            "method_success",
            "recovery_success",
            "latitude",
            "longitude",
            "stage",
            "landing_zone",
            "get_turnaround",
        ]


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
        fields = ["id", "name", "version", "type", "image", "status", "rocket", "stage_and_recovery"]


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
        fields = ["get_turnaround", "id", "splashdown_time", "launch", "recovery_boat"]


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
    # launch_names = serializers.ListField(child=serializers.CharField())
