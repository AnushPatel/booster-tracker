from rest_framework import serializers
from .models import Orbit, StageAndRecovery, Launch, Rocket, RocketFamily, Operator, Pad, LandingZone


class OrbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orbit
        fields = "__all__"


class StageAndRecoverySerializer(serializers.ModelSerializer):
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


class LaunchOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Launch
        fields = "__all__"


class RocketSerializer(serializers.ModelSerializer):
    launches = LaunchOnlySerializer(many=True, read_only=True, source="launch_set")

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
