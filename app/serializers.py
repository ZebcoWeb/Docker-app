from rest_framework import serializers

from app.models import App



class AppCreateSerializer(serializers.ModelSerializer):
    envs = serializers.JSONField(required=False)
    command = serializers.CharField(required=False)
    class Meta:
        model = App
        fields = ["name", "image", "envs", "command"]

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ["id", "name", "image", "envs", "command", "created_at"]


class AppRunSerializer(serializers.Serializer):
    instance_count = serializers.IntegerField(min_value=1)