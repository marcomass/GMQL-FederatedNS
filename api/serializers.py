from .models import *
from rest_framework import serializers

class InstitutionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Institution
        fields = ('name', 'namespace', 'creation_date')

class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'details', 'URI')

class DatasetSerializer(serializers.HyperlinkedModelSerializer):

    identifier = serializers.SerializerMethodField()

    locations = LocationSerializer(read_only=True, many=True)
    allowed_to = InstitutionSerializer(read_only=True, many=True)

    def get_identifier(self, obj):
        return '{}.{}'.format(obj.namespace_id, obj.name)

    class Meta:
        model = Dataset
        fields = ('identifier', 'name', 'namespace', 'author', 'description', 'pub_date', 'locations', 'allowed_to')
