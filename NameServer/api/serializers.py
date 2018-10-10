from .models import *
from rest_framework import serializers

class InstitutionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Institution
        fields = ('name', 'namespace', 'creation_date')

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
    allowed_to = InstitutionSerializer(read_only=True, many=True)

    def get_identifier(self, obj):
        return '{}.{}'.format(obj.namespace_id, obj.name)

    class Meta:
        model = Dataset
        fields = ('identifier', 'name', 'namespace', 'author', 'description', 'pub_date', 'locations', 'allowed_to')

class AuthenticationSerializer(serializers.HyperlinkedModelSerializer):

    identifier = serializers.SerializerMethodField()

    def get_identifier(self, obj):
        return '{}_{}'.format(obj.client.namespace, obj.target.namespace)

    class Meta:
        model = Authentication
        fields = ('identifier', 'client', 'target', 'token', 'expiration')

