from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from app.serializers import AppSerializer, AppHistorySerializer, AppInstanceSerializer
from app.models import App, AppInstance, AppHistory
from utilities.docker import DockerHandler



docker = DockerHandler()


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    lookup_url_kwarg = "app_id"
    
    def list(self, request):
        # Filter apps by image and name
        image = request.query_params.get("image", None)
        name = request.query_params.get("name", None)
        if image:
            self.queryset = self.queryset.filter(image__icontains=image)
        if name:
            self.queryset = self.queryset.filter(name__icontains=name)

        serializer = AppSerializer(self.queryset, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["get"])
    def run(self, request, app_id):
        try:
            app = self.queryset.get(id=app_id)
        except App.DoesNotExist:
            return Response({"error": "App not found"}, status=404, exception=True)
        
        instance_id = docker.run_app(
            image=app.image,
            envs=app.envs,
            command=app.command
        )
        app_instance = AppInstance.objects.create(
            instance_id=instance_id,
            app=app
        )
        AppHistory.objects.create(
            app=app,
            instance=app_instance,
            image=app.image,
            envs=app.envs,
            command=app.command
        )
        return Response(
            {"instance_id": instance_id},
            status=200
        )
    
    @action(detail=True, methods=["get"])
    def history(self, request, app_id):
        status = request.query_params.get("status", None)
        if status:
            self.queryset = self.queryset.filter(status=status)
        try:
            app = self.queryset.get(id=app_id)
        except App.DoesNotExist:
            return Response({"error": "App not found"}, status=404, exception=True)
        
        history = app.history.all()
        serializer = AppHistorySerializer(history, many=True)
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=["get"])
    def instances(self, request, app_id):
        try:
            app = self.queryset.get(id=app_id)
        except App.DoesNotExist:
            return Response({"error": "App not found"}, status=404, exception=True)
        
        instances = app.instances.all()
        serializer = AppInstanceSerializer(instances, many=True)
        return Response(serializer.data, status=200)


class AppInstanceStart(generics.GenericAPIView):
    serializer_class = AppInstanceSerializer

    def get(self, request, instance_id):
        try:
            app_instance = AppInstance.objects.get(instance_id=instance_id)
        except AppInstance.DoesNotExist:
            return Response({"error": "App instance not found"}, status=404, exception=True)
        
        docker.start_app(container_id=instance_id)
        return Response(
            "App instance started successfully",
            status=200
        )

class AppInstanceStop(generics.GenericAPIView):
    serializer_class = AppInstanceSerializer

    def get(self, request, instance_id):
        try:
            app_instance = AppInstance.objects.get(instance_id=instance_id)
        except AppInstance.DoesNotExist:
            return Response({"error": "App instance not found"}, status=404, exception=True)
        
        docker.stop_app(container_id=instance_id)
        return Response(
            "App instance stopped successfully",
            status=200
        )

class AppInstanceRestart(generics.GenericAPIView):
    serializer_class = AppInstanceSerializer

    def get(self, request, instance_id):
        try:
            app_instance = AppInstance.objects.get(instance_id=instance_id)
        except AppInstance.DoesNotExist:
            return Response({"error": "App instance not found"}, status=404, exception=True)
        
        docker.restart_app(container_id=instance_id)
        return Response(
            "App instance restarted successfully",
            status=200
        )

class AppInstanceRemove(generics.GenericAPIView):
    serializer_class = AppInstanceSerializer

    def get(self, request, instance_id):
        try:
            app_instance = AppInstance.objects.get(instance_id=instance_id)
        except AppInstance.DoesNotExist:
            return Response({"error": "App instance not found"}, status=404, exception=True)
        
        docker.remove_app(container_id=instance_id)
        app_instance.delete()
        return Response(
            "App instance removed successfully",
            status=200
        )