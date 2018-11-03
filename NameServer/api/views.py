# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat
from django.db.models import  Value as V
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from django.db.models import Q

from .serializers import *


class InstanceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    API endpoint that allows Instances to be viewed or edited.
    """
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    lookup_value_regex = '[\w.@+-]+'

    def retrieve(self, request, pk=None):
        print(pk)
        queryset = Instance.objects.get_by_natural_key(pk)


        serializer = InstanceSerializer(queryset)
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    lookup_value_regex = '[\w.@+-]+'

    def retrieve(self, request, pk=None):
        queryset = Group.objects.get_by_natural_key(pk)
        serializer = GroupSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        print("SALVO")
        return serializer.save(owner=self.request.user)

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Locations to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    lookup_value_regex = '[\w.@+-]+'

    def perform_create(self, serializer):
        return serializer.save(namespace=self.request.user)

    def retrieve(self, request, pk=None):

        # identifier: namespace + "." + name

        queryset =  Location.objects.all().annotate(identifier=Concat('namespace', V('.'), 'name'))

        location = get_object_or_404(queryset, identifier = pk )
        serializer = LocationSerializer(location)
        return Response(serializer.data)

class DatasetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Datasets to be viewed or edited.
    """
    queryset = Dataset.objects.order_by('-pub_date')
    serializer_class = DatasetSerializer
    lookup_value_regex = '[\w.@+-]+'

    def perform_create(self, serializer):
        return serializer.save(namespace=self.request.user)


    # List only those datasets allowed to the current user
    def list(self, request):

        # TODO: Write it in a more proper way
        other_instances = Instance.objects.exclude(namespace=request.user.namespace)
        queryset = Dataset.objects.all()#.exclude(allowed_to__in=other_instances)

        serializer = DatasetSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        # identifier: namespace + "." + name

        # TODO: Write it in a more proper way
        other_instances = Instance.objects.exclude(namespace=request.user.namespace)
        allowed = Dataset.objects.all()#.exclude(allowed_to__in=other_instances)

        queryset = allowed.filter().annotate(identifier=Concat('namespace', V('.'), 'name'))

        dataset = get_object_or_404(queryset, identifier = pk )
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    permission_classes = ([permissions.IsAuthenticated])

class AuthenticationViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):

    queryset = Authentication.objects.all()
    serializer_class = AuthenticationSerializer
    lookup_value_regex = '[\w.@+-]+'

    def retrieve(self, request, pk=None):

        # identifier: client + "_" + target

        queryset = Authentication.objects.filter(Q(client=request.user) | Q(target=request.user))\
            .annotate(identifier=Concat('client', V('_'), 'target'))

        auth = get_object_or_404(queryset, identifier = pk )
        print(pk)

        serializer = AuthenticationSerializer(auth)
        return Response(serializer.data)

    def list(self, request):
        queryset = Authentication.objects.filter(Q(client=request.user) | Q(target=request.user))
        serializer = AuthenticationSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):

        # DELETE IF EXISTS
        if Authentication.objects.filter(client=self.request.user, target=self.request.data["target"]).exists():
           Authentication.objects.filter(client=self.request.user, target=self.request.data["target"]).delete()

        serializer.save(client=self.request.user)

    permission_classes = ([permissions.IsAuthenticated])