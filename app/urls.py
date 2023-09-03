from django.urls import path

from app import views

urlpatterns = [
    path("create/", views.AppCreateView.as_view()),
    path("<int:app_id>/retrieve/", views.AppRetrieveView.as_view()),
    path("list/", views.AppListView.as_view()),
    path("<int:app_id>/update/", views.AppUpdateView.as_view()),
    path("<int:app_id>/delete/", views.AppDeleteView.as_view()),
    path("<int:app_id>/run/", views.AppRunView.as_view()),
]
