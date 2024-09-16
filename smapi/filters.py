from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import FinishingItemSerializer, FinishingSerializer
from .models import Finishing, FinishingItem
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.http import QueryDict
from rest_framework import viewsets


class FinishingViewSet(viewsets.ModelViewSet):
    # queryset = Finishing.objects.all()
    serializer_class = FinishingSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["roomUuid", "room_uuid", "uuid", "id", "containerUuid", "room_number"]

    def get_queryset(self):
        queryset = Finishing.objects.all()
        roomUuid = self.request.query_params.get('roomUuid')
        uuid = self.request.query_params.get('uuid')
        containerUuid = self.request.query_params.get('containerUuid')
        id = self.request.query_params.get("id")
        room_number = self.request.query_params.get("room_number")
        if roomUuid is not None:
            queryset = queryset.filter(room_uuid=roomUuid)
        elif uuid is not None:
            queryset = queryset.filter(uuid=uuid)
        elif containerUuid is not None:
            queryset = queryset.filter(containerUuid=containerUuid)
        elif id is not None:
            queryset = queryset.filter(id=id)
        elif room_number is not None:
            queryset = queryset.filter(room_number=room_number)
        return queryset

