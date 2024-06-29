from rest_framework import serializers
from .models import Orbit, StageAndRecovery, Launch, Rocket, RocketFamily, Operator


class OrbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orbit
        fields = "__all__"


class StageAndRecoverySerializer(serializers.ModelSerializer):
    booster_name = serializers.SerializerMethodField()
    zone_name = serializers.SerializerMethodField()

    class Meta:
        model = StageAndRecovery
        fields = ["booster_name", "zone_name"]

    def get_booster_name(self, obj):
        if obj.stage:
            return obj.stage.name
        return None

    def get_zone_name(self, obj):
        if obj.landing_zone:
            return obj.landing_zone.name
        return None


class LaunchSerializer(serializers.ModelSerializer):
    # recoveries = StageAndRecoverySerializer(many=True, read_only=True, source="stageandrecovery_set")

    class Meta:
        model = Launch
        fields = ["time", "pad", "rocket", "name", "launch_outcome", "id", "image", "recoveries", "boosters"]


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
