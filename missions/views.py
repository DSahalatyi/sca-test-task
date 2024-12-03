from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from missions.models import Mission
from missions.serializers import MissionSerializer, MissionListSerializer, MissionUpdateSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("targets")
            return queryset

        return queryset

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ("list", "retrieve"):
            serializer = MissionListSerializer
            return serializer

        if self.action in ("update", "partial_update"):
            serializer = MissionUpdateSerializer
            return serializer

        return serializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()

        if mission.assignee is not None:
            raise ValidationError("A mission cannot be deleted because it is assigned to a cat.")

        self.perform_destroy(mission)
        return Response(status=status.HTTP_204_NO_CONTENT)
