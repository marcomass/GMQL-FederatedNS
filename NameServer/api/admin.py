# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin

from .models import *

admin.site.register(Instance)
admin.site.register(Authentication)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    readonly_fields = ('owner',)
    fieldsets = [
        (None, {'fields': [('name', 'instances', 'owner')]}),
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()



@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    #list_display = ('name', 'owner')
    readonly_fields = ('namespace',)
    #fieldsets = [
     #   (None, {'fields': [('name', 'instances', 'owner')]}),
    #]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'namespace', None) is None:
            obj.namespace = request.user
        obj.save()

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    #list_display = ('name', 'owner')
    readonly_fields = ('namespace',)
    #fieldsets = [
     #   (None, {'fields': [('name', 'instances', 'owner')]}),
    #]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'namespace', None) is None:
            obj.namespace = request.user
        obj.save()