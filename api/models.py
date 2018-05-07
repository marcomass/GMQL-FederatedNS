# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Institution(models.Model):
    name          = models.CharField(max_length=50, unique=True)
    namespace     = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField()

    def __str__(self):
        return self.namespace + " ( " + self.name + " )"

class Location(models.Model):
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=300)
    URI = models.CharField(max_length=100)

    owner =  models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.URI + " ( " + self.owner.name + " - " + self.name + " )"

class Dataset(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    pub_date = models.DateTimeField()

    namespace = models.ForeignKey(Institution, to_field='namespace', on_delete=models.CASCADE)

    locations =  models.ManyToManyField(Location, related_name='dataset_location')
    allowed_to = models.ManyToManyField(Institution, related_name='dataset_institution')

    @property
    def dataset_identifier(self):
        return self.namespace_id + "." + self.name

    class Meta:
        unique_together = (("name", "namespace"),)

    def __str__(self):
        return self.dataset_identifier
