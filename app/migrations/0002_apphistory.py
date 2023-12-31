# Generated by Django 4.2.4 on 2023-09-03 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("FINISHED", "Finished"), ("RUNNING", "Running")],
                        default="RUNNING",
                        max_length=100,
                    ),
                ),
                ("running_time", models.DateTimeField(auto_now_add=True)),
                ("image", models.CharField(max_length=100)),
                ("envs", models.CharField(max_length=100)),
                ("command", models.CharField(max_length=100)),
                (
                    "app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="history",
                        to="app.app",
                    ),
                ),
            ],
            options={
                "db_table": "app_history",
            },
        ),
    ]
