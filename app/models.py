from django.db import models



class App(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=150)
    envs = models.JSONField(blank=True, null=True)
    command = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "apps"


class AppInstance(models.Model):
    instance_id = models.CharField(max_length=100, unique=True, db_index=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="instances")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "app_instances"


class AppHistory(models.Model):
    class Status(models.TextChoices):
        RUNNING = "RUNNING"
        FINNISHED = "FINNISHED"

    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="history")
    instance = models.ForeignKey(AppInstance, on_delete=models.DO_NOTHING, related_name="history")
    status = models.CharField(max_length=100, choices=Status.choices, default="RUNNING")
    running_time = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=100)
    envs = models.JSONField(blank=True, null=True)
    command = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "app_history"