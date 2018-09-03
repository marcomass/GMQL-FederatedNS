# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat
from django.db.models import  Value as V
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from api.permissions import IsAllowedToSeeThis
from serializers import *


class InstitutionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Institutions to be viewed or edited.
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = (permissions.IsAuthenticated,)

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Locations to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

class DatasetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Datasets to be viewed or edited.
    """
    queryset = Dataset.objects.order_by('-pub_date')
    serializer_class = DatasetSerializer
    lookup_value_regex = '[\w.@+-]+'


    # List only those datasets allowed to the current user
    def list(self, request):

        # TODO: Write it in a proper way
        other_institutions = Institution.objects.exclude(namespace=request.user.namespace)
        queryset = Dataset.objects.all().exclude(allowed_to__in=other_institutions)

        serializer = DatasetSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        # identifier: namespace + "." + name

        queryset = Dataset.objects.all().annotate(identifier=Concat('namespace', V('.'), 'name'))

        dataset = get_object_or_404(queryset, identifier = pk )
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    permission_classes = ([permissions.IsAuthenticated])