from django.shortcuts import render
from rest_framework import viewsets

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
