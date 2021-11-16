from rest_framework import viewsets, status
from rest_framework.response import Response

from .CustomResponse import CustomResponse
from .models import Asteroid, Sighting
from .serializer import AsteroidSerializer, SightingSerializer


class AsteroidViewSet(viewsets.ModelViewSet):
    queryset = Asteroid.objects.all()
    serializer_class = AsteroidSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(serializer.data, status=status.HTTP_200_OK)
        pass


class SightingViewSet(viewsets.ModelViewSet):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(serializer.data)
