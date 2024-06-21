from rest_framework import serializers
from .models import RocketFamily, Operator


class RocketFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = RocketFamily
        fields = "__all__"


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = "__all__"
