from django.urls import include, path
from rest_framework import routers

from missions import views

app_name = "missions"

router = routers.DefaultRouter()

router.register("missions", views.MissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]