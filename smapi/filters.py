import django_filters.rest_framework
from rest_framework import generics
from .serializers import FinishingItemSerializer, FinishingSerializer
from .models import Finishing, FinishingItem


# class FinishingListView(generics.ListAPIView):
#     queryset = Finishing.objects.all()
#     serializer_class = FinishingSerializer
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

class FinishingListView(generics.ListAPIView):
    queryset = Finishing.objects.all()
    serializer_class = FinishingSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['roomUuid', 'uuid', "room_uuid"]
