from .models import *
from rest_framework import serializers

class InstanceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Instance
        fields = ('name', 'namespace', 'creation_date')

class GroupSerializer(serializers.HyperlinkedModelSerializer):

    identifier = serializers.SerializerMethodField()
    instances = InstanceSerializer(read_only=True, many=True)

    def get_identifier(self, obj):
        return obj.name

    class Meta:
        model = Group
        fields = ('identifier', 'name', 'owner', 'instances')

class LocationSerializer(serializers.HyperlinkedModelSerializer):

    identifier = serializers.SerializerMethodField()

    def get_identifier(self, obj):
        return '{}.{}'.format(obj.namespace_id, obj.name)

    class Meta:
        model = Location
        fields = ('identifier', 'name', 'details', 'URI', 'namespace')


class DatasetSerializer(serializers.HyperlinkedModelSerializer):

    identifier = serializers.SerializerMethodField()

    locations = LocationSerializer(read_only=True, many=True)
    allowed_to_single = InstanceSerializer(read_only=True, many=True)
    allowed_to_group = GroupSerializer(read_only=True, many=True)

    def get_identifier(self, obj):
        return '{}.{}'.format(obj.namespace_id, obj.name)

    class Meta:
        model = Dataset
        fields = ('identifier', 'name', 'namespace', 'author', 'description', 'pub_date', 'locations', 'allowed_to_single', 'allowed_to_group')

class AuthenticationSerializer(serializers.HyperlinkedModelSerializer):

    identifier = serializers.SerializerMethodField()

    def get_identifier(self, obj):
        return '{}_{}'.format(obj.client.namespace, obj.target.namespace)

    class Meta:
        model = Authentication
        fields = ('identifier', 'client', 'target', 'token', 'expiration')

