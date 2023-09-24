from rest_framework import serializers

from app.models import App, AppHistory, AppInstance




class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ["id", "name", "image", "envs", "command", "created_at"]


class AppInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInstance
        fields = ["instance_id", "app","created_at"]

class AppHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppHistory
        fields = ["app", "status", "running_time", "image", "envs", "command"]