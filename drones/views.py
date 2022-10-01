from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, GenericAPIView
)
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import ScopedRateThrottle

from .permissions import IsCurrentUserOwnerOrReadOnly
from .models import Drone, DroneCategory, Pilot, Competition
from . import serializers


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class DroneCategoryList(ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = serializers.DroneCategorySerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('name',)
    search_fields = ('^name',) # ^, =, $
    ordering_fields = ('name',)


class DroneCategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = serializers.DroneCategorySerializer


class DroneList(ListCreateAPIView):
    throttle_scope = 'drones'
    throttle_classes = (ScopedRateThrottle,)#Ограничевает скорость запросов
    queryset = Drone.objects.all()
    serializer_class = serializers.DroneSerializer
    permission_classes = (
        IsCurrentUserOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_fields = (
        'name',
        'drone_category',
        'manufacturing_date',
        'has_it_competed',
    )
    search_fields = (
        '^name',
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetail(RetrieveUpdateDestroyAPIView):
    throttle_scope = 'drones'
    throttle_classes = (ScopedRateThrottle,) #Ограничевает скорость запросов
    queryset = Drone.objects.all()
    serializer_class = serializers.DroneSerializer
    permission_classes = (
        IsCurrentUserOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )


class PilotList(ListCreateAPIView):
    throttle_scope = 'pilots'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = serializers.PilotSerializer
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated
    )
    filter_fields = (
        'name',
        'gender',
        'races_count',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
        'races_count'
    )


class PilotDetail(RetrieveUpdateDestroyAPIView):
    throttle_scope = 'pilots'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = serializers.PilotSerializer
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated
    )


class CompetitionList(ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionSerializer


class CompetitionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = serializers.CompetitionSerializer


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'dronecategory-list': reverse('dronecategory-list', request=request),
            'drone-list': reverse('drone-list', request=request),
            'pilot-list': reverse('pilot-list', request=request),
            'competition-list': reverse('competition-list', request=request)
            })