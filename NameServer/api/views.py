# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat
from django.db.models import  Value as V
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from django.db.models import Q

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


from .serializers import *

class IsAuthenticatedOrPostOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated) or request.method in ['POST', 'GET']


class InstanceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    API endpoint that allows Instances to be viewed or edited.
    """
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    permission_classes = (IsAuthenticatedOrPostOnly,)

    lookup_value_regex = '[\w.@+-]+'


    def list(self, request, *args, **kwargs):
        #  RETURN AN EMPTY LIST IF THE USER IS NOT AUTHENTICATED
        # (RETURNING HTTP 403 WOULD DISABLE THE FORM FOR REGISTERING THE USER)
        if (not request.user.is_authenticated):
            return Response()
        return super(InstanceViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None):

        # RETURN 403 IF THE USER IS NOT AUTHENTICATED
        if (not request.user.is_authenticated):
            raise PermissionDenied()

        queryset = Instance.objects.get_by_natural_key(pk)

        print(pk + ": " + self.request.user.username)

        if pk==request.user.username:

            serializer = CurrentInstanceSerializer(queryset)
        else:
            serializer = InstanceSerializer(queryset)

        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save()


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    lookup_value_regex = '[\w.@+-]+'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', False)

        if pk==request.user.username or pk=='GMQL-ALL':
            return Response(status=status.HTTP_403_FORBIDDEN)

        if ( Group.objects.get(pk = pk).owner.username == request.user.username):
            return super(GroupViewSet, self).update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data="You are not the owner of this resource.")

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk', False)

        if pk==request.user.username or pk=='GMQL-ALL':
            return Response(status=status.HTTP_403_FORBIDDEN)

        if ( Group.objects.get(pk = pk).owner.username == request.user.username):
            return super(GroupViewSet, self).destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data="You are not the owner of this resource.")


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Locations to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    lookup_value_regex = '[\w.@+-]+'

    def perform_create(self, serializer):
        return serializer.save(instance=self.request.user)

    def retrieve(self, request, pk=None):

        # identifier: instancename + "." + name

        #queryset =  Location.objects.all().annotate(identifier=Concat('instance', V('.'), 'name'))
        queryset =  Location.objects.all().annotate(identifier=Concat('instance', V('.'), 'name'))

        location = get_object_or_404(queryset, instance = pk )
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', False)

        if (pk == request.user.username):
            return super(LocationViewSet, self).update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data="You are not the owner of this resource.")

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk', False)

        if (pk == request.user.username):
            return super(LocationViewSet, self).destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data="You are not the owner of this resource.")


class DatasetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Datasets to be viewed or edited.
    """
    queryset = Dataset.objects.order_by('-pub_date')
    serializer_class = DatasetSerializer
    lookup_value_regex = '[\w.@+-]+'

    permission_classes = ([permissions.IsAuthenticated])

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


    # List only those datasets allowed to the current user
    def list(self, request):

        # Retrieve current user's groups
        groups = Group.objects.filter(instances__in=[request.user.id]).values_list('name', flat=True)
        datasets  = Dataset.objects.filter(allowed_to__in=groups).annotate(identifier=Concat('owner_id', V('.'), 'name'))

        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        groups = Group.objects.filter(instances__in=[request.user.id]).values_list('name', flat=True)
        datasets = Dataset.objects.filter(allowed_to__in=groups)

        queryset = datasets.annotate(identifier=Concat('owner_id', V('.'), 'name'))

        # Notice that 404 is returned both when it does not exist or when the user is not allowed to see it
        dataset = get_object_or_404(queryset, identifier = pk )

        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Dataset.objects.all().annotate(identifier=Concat('owner_id', V('.'), 'name'))
        instance = queryset.get(identifier=pk)
        if(instance.owner==request.user):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,  data="You are not the owner of this resource.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = kwargs.pop('pk', False)
        queryset = Dataset.objects.all().annotate(identifier=Concat('owner_id', V('.'), 'name'))
        instance = queryset.get(identifier=pk)

        if (instance.owner == request.user):
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data="You are not the owner of this resource.")



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