from rest_framework.relations import PrimaryKeyRelatedField

from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

class InstanceSerializer( serializers.ModelSerializer):

    password = serializers.CharField(max_length=255, write_only=True,style={'input_type': 'password'})
    creation_date = serializers.CharField(read_only=True)
    instancename=serializers.CharField(source='username')

    location  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Instance
        fields = ( 'instancename', 'description', 'email', 'password', 'creation_date', 'location')

    def create(self, validated_data):

        user = get_user_model().objects.create_user(validated_data['description'],
                                  validated_data['username'],
                                  validated_data['email'],
                                  validated_data['password'])

        return user

    def get_location(self, obj):
        try:
         return '{}'.format(obj.username)
        except:
         return None

class CurrentInstanceSerializer( InstanceSerializer):

    token = serializers.SerializerMethodField()
    instancename = serializers.CharField(source='username')

    class Meta:
        model = Instance
        fields = ( 'instancename', 'description', 'email', 'password', 'creation_date', 'location', 'token')


    def get_token(self, obj):

        token = Token.objects.get(user=obj)
        return  token.key


class GroupSerializer(serializers.ModelSerializer):

    identifier = serializers.SerializerMethodField()

    instances = serializers.SlugRelatedField(
        many=True,
        queryset=Instance.objects.all(),
        #read_only=True,
        slug_field='username'
    )

    def get_identifier(self, obj):
        return obj.name

    class Meta:
        model = Group
        fields = ('identifier', 'name', 'owner', 'instances')


class LocationSerializer(serializers.ModelSerializer):

    #identifier = serializers.SerializerMethodField()

    #def get_identifier(self, obj):
        #return '{}.{}'.format(obj.instance.username, obj.name)
        #return '{}'.format(obj.instance.username)

    class Meta:
        model = Location
        fields = ('instance', 'name', 'details', 'URI')
        read_only_fields = ('instance',)


class DatasetSerializer(serializers.ModelSerializer):

    identifier = serializers.SerializerMethodField()

    copies = serializers.SlugRelatedField(
        many=True,
        queryset=Instance.objects.all(),
        #read_only=True,
        slug_field='username'
    )
    allowed_to = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        #read_only=True,
        slug_field='name'
    )
    pub_date = serializers.CharField(read_only=True)

    def get_identifier(self, obj):
        return '{}.{}'.format(obj.owner_id, obj.name)

    class Meta:
        model = Dataset
        fields = ('identifier', 'name', 'owner', 'author', 'description', 'pub_date', 'copies', 'allowed_to')

class AuthenticationSerializer(serializers.ModelSerializer):

    identifier = serializers.SerializerMethodField()

    def get_identifier(self, obj):
        return '{}_{}'.format(obj.client.username, obj.target.username)

    class Meta:
        model = Authentication
        fields = ('identifier', 'client', 'target', 'token', 'expiration')