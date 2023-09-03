from rest_framework import generics
from rest_framework import status

from app.serializers import AppSerializer, AppCreateSerializer, AppRunSerializer
from app.models import App, AppHistory
from utilities.responses import SuccessResponse, ErrorResponse
from utilities import docker



class AppCreateView(generics.CreateAPIView):
    serializer_class = AppCreateSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        app = serializer.save()
        data = serializer.data
        data["id"] = app.id
        return SuccessResponse(
            data=data,
            status=status.HTTP_201_CREATED,
            message="App created successfully"
        ).send()

class AppRetrieveView(generics.RetrieveAPIView):
    serializer_class = AppSerializer

    def retrieve(self, request, app_id):
        try:
            app = App.objects.get(id=app_id)
            serializer = self.get_serializer(app)
            return SuccessResponse(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="App retrieved successfully"
            ).send()
        except App.DoesNotExist:
            return ErrorResponse(
                message="App does not exist",
                status=status.HTTP_404_NOT_FOUND
            ).send()

class AppListView(generics.ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer

class AppUpdateView(generics.GenericAPIView):
    serializer_class = AppSerializer

    def patch(self, request, app_id):
        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return ErrorResponse(
                message="App does not exist",
                status=status.HTTP_404_NOT_FOUND
            ).send()

        serializer = self.get_serializer(app, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(
            data=serializer.data,
            status=status.HTTP_200_OK,
            message="App updated successfully"
        ).send()

class AppDeleteView(generics.DestroyAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer

    def destroy(self, request, app_id):
        try:
            app = App.objects.get(id=app_id)
            app.delete()
            return SuccessResponse(
                status=status.HTTP_200_OK,
                message="App deleted successfully"
            ).send()
        except App.DoesNotExist:
            return ErrorResponse(
                message="App does not exist",
                status=status.HTTP_404_NOT_FOUND
            ).send()

class AppRunView(generics.GenericAPIView):
    serializer_class = AppRunSerializer

    def post(self, request, app_id):
        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return ErrorResponse(
                message="App does not exist",
                status=status.HTTP_404_NOT_FOUND
            ).send()

        serializer = AppRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_count = serializer.validated_data["instance_count"]
        try:
            container_id = docker.run_containers(
                image=app.image,
                envs=app.envs,
                command=app.command,
                instance_count=instance_count
            )
            if docker.check_status_container(container_id) == "running":
                app_status = AppHistory.Status.RUNNING
            else:
                app_status = AppHistory.Status.FINNISHED
                
            AppHistory.objects.create(
                app=app,
                instance_count=instance_count,
                image=app.image,
                envs=app.envs,
                command=app.command,
                status=app_status
            )
        except:
            return ErrorResponse(
                message="App running signal failed to send",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).send()

        return SuccessResponse(
            status=status.HTTP_200_OK,
            message="App running signal sent"
        ).send()