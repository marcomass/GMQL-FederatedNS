# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.contrib.auth.base_user import BaseUserManager
import uuid

from django.utils import timezone


from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser, UserManager


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class MyUserManager(UserManager):
    def create_user(self, name, namespace, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email       = self.normalize_email(email),
            namespace   = namespace,
            name        = name
        )

        user.set_password(password)
        user.username = namespace
        user.save(using=self._db)
        return user

    def create_superuser(self, name, namespace, email,  password, **extra_fields):
        user                = self.create_user( name, namespace, email, password)
        user.is_admin       = True
        user.is_superuser   = True
        user.is_staff       = True
        user.save(using=self._db)
        return user

class Institution(AbstractUser):
    name          = models.CharField(max_length=50, unique=True)
    email         = models.EmailField(max_length=254, unique=True)
    namespace     = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True)

    USERNAME_FIELD = 'namespace'
    REQUIRED_FIELDS = ['name', 'email']

    objects = MyUserManager()

    def __str__(self):
        return self.namespace + " ( " + self.name + " )"



class Location(models.Model):
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=300)
    URI = models.CharField(max_length=100)

    namespace =  models.ForeignKey(Institution, to_field='namespace', on_delete=models.CASCADE, editable=False)

    @property
    def location_identifier(self):
        return self.namespace_id + "." + self.name

    class Meta:
        unique_together = (("name", "namespace"),)

    def __str__(self):
        return self.URI + " ( " + self.location_identifier + " )"

class Dataset(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    pub_date = models.DateTimeField(default=timezone.now)

    namespace = models.ForeignKey(Institution, to_field='namespace', on_delete=models.CASCADE, editable=False)

    locations =  models.ManyToManyField(Location, related_name='dataset_location')
    allowed_to = models.ManyToManyField(Institution, related_name='dataset_institution')


    @property
    def dataset_identifier(self):
        return self.namespace_id + "." + self.name

    class Meta:
        unique_together = (("name", "namespace"),)

    def __str__(self):
        return self.dataset_identifier

class Authentication(models.Model):

    EXPIRATION_DAYS = 14

    client = models.ForeignKey(Institution, to_field='namespace', related_name='client', on_delete=models.CASCADE, editable=False)
    target = models.ForeignKey(Institution, to_field='namespace', related_name='target', null=True, blank=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, editable=False)
    expiration = models.DateTimeField(blank=True, editable=False, default=timezone.now)

    # Generate a token and expiration date on saving
    def save(self, *args, **kwargs):
            self.token = uuid.uuid4()
            self.expiration = timezone.now() + timezone.timedelta(days=self.EXPIRATION_DAYS)
            super(Authentication, self).save()

    @property
    def authentication_identifier(self):
        return str(self.client.namespace) + "_" + self.target.namespace


    class Meta:
        unique_together = (("client", "target"),)

    def __str__(self):
        return self.authentication_identifier

