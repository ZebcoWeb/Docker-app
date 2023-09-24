from django.urls import path

from app import views

urlpatterns = [
    path("create/", views.AppViewSet.as_view({"post": "create"})),
    path("<int:app_id>/retrieve/", views.AppViewSet.as_view({"get": "retrieve"})),
    path("list/", views.AppViewSet.as_view({"get": "list"})),
    path("<int:app_id>/update/", views.AppViewSet.as_view({"post": "update"})),
    path("<int:app_id>/delete/", views.AppViewSet.as_view({"get": "destroy"})),
    path("<int:app_id>/run/", views.AppViewSet.as_view({"get": "run"})),
    path("<int:app_id>/history/", views.AppViewSet.as_view({"get": "history"})),
    path("<int:app_id>/instances/", views.AppViewSet.as_view({"get": "instances"})),

    path("instance/<str:instance_id>/start/", views.AppInstanceStart.as_view()),
    path("instance/<str:instance_id>/stop/", views.AppInstanceStop.as_view()),
    path("instance/<str:instance_id>/restart/", views.AppInstanceRestart.as_view()),
    path("instance/<str:instance_id>/remove/", views.AppInstanceRemove.as_view()),
]
