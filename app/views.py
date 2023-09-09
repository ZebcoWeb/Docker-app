from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from app.serializers import AppSerializer, AppHistorySerializer
from app.models import App, AppHistory
from utilities import docker



class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    lookup_url_kwarg = "app_id"

    @action(methods=["get"], detail=True)
    def history(self, request, app_id):
        app_history = AppHistory.objects.filter(app__id=app_id)
        serializer = AppHistorySerializer(app_history, many=True)
        return Response(serializer.data)
    
    @action(methods=["get"], detail=True)
    def run(self, request, app_id):
        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return Response({"error": "App not found"}, status=404, exception=True)

        try:
            container_id = docker.run_container(
                image=app.image,
                envs=app.envs,
                command=app.command,
            )
        except:
            return Response({"error": "Error running container"}, status=500, exception=True)
        if docker.check_status_container(container_id) == "running":
            app_status = AppHistory.Status.RUNNING
        else:
            app_status = AppHistory.Status.FINNISHED
            
        app_history = AppHistory.objects.create(
            app=app,
            status=app_status,
            image=app.image,
            envs=app.envs,
            command=app.command,
        )
        serializer = AppHistorySerializer(app_history)
        return Response(serializer.data)