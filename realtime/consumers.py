import json

from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings

from app.models import AppInstance
from utilities.docker import DockerHandler

docker = DockerHandler()

class InstanceConsumer(JsonWebsocketConsumer):

    def validate_content(self, content):
        if not content.get("type"):
            self.send_json({"error": "Type not provided"})
            self.close()
        if not content.get("instance_id"):
            self.send_json({"error": "Instance ID not provided"})
            self.close()
        instance = AppInstance.objects.get(instance_id=content.get("instance_id"))
        if not instance:
            self.send_json({"error": "Instance not found"})
            self.close()
        if not docker.is_running(instance.instance_id):
            self.send_json({"error": "Instance not running"})
            self.close()
        return instance
    
    def websocket_connect(self, event):
        self.accept()
        self.send_json({"message": "Connected"})
    

    def receive_json(self, content):
        instance = self.validate_content(content)

        if content.get("type") == settings.WS_INSTANCE_LOGS_TYPE:

            for e in docker.logs_app_event(instance.instance_id):
                self.send_json({"data": e.decode("utf-8")})
            else:
                self.send_json({"error": "No logs found"})
                self.close()
        
        elif content.get("type") == settings.WS_INSTANCE_USAGE_TYPE:
            instance = self.validate_content(content)

            for e in docker.stats_app_event(instance.instance_id):
                e = json.loads(e.decode("utf-8"))
                self.send_json({"data": e})
            else:
                self.send_json({"error": "No stats found"})
                self.close()

        elif content.get("type") == settings.WS_INSTANCE_USAGE_TYPE:
            instance = self.validate_content(content)

            for e in docker.stats_app_event(instance.instance_id):
                e = json.loads(e.decode("utf-8"))
                self.send_json({"data": e})
            else:
                self.send_json({"error": "No stats found"})
                self.close()
        
        elif content.get("type") == settings.WS_INSTANCE_USAGE_TYPE:
            instance = self.validate_content(content)

            for e in docker.stats_app_event(instance.instance_id):
                e = json.loads(e.decode("utf-8"))
                self.send_json({"data": e})
            else:
                self.send_json({"error": "No stats found"})
                self.close()

        elif content.get("type") == settings.WS_INSTANCE_STATUS_TYPE:
            instance = self.validate_content(content)

            while True:
                status = docker.status_app(instance.instance_id)
                self.send_json({"data": status})
                import time
                time.sleep(3)