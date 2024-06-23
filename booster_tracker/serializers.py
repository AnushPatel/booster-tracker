from rest_framework import serializers
from .models import Launch, Rocket, RocketFamily, Operator


class LaunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Launch
        fields = "__all__"


class RocketSerializer(serializers.ModelSerializer):
    launches = LaunchSerializer(many=True, read_only=True, source="launch_set")

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
