from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from cats.models import Cat
from cats.serializers import CatSerializer, CatUpdateSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ("update", "partial_update"):
            serializer = CatUpdateSerializer

        return serializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            self.perform_update(serializer)
            instance = self.get_object()
            response_serializer = CatSerializer(instance)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
