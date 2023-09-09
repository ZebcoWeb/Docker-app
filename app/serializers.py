from rest_framework import serializers

from app.models import App, AppHistory




class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ["id", "name", "image", "envs", "command", "created_at"]

class AppHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppHistory
        fields = ["app", "status", "running_time", "image", "envs", "command"]