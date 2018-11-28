# -*- coding: utf-8 -*-
from __future__ import unicode_literals



from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Instance

@admin.register(Instance)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Instance
    list_display = ['username', 'description','email']


#admin.site.register(Instance)
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
    readonly_fields = ('owner',)
    #fieldsets = [
     #   (None, {'fields': [('name', 'instances', 'owner')]}),
    #]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'instance', None) is None:
            obj.instance = request.user
        obj.save()

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    #list_display = ('name', 'owner')
    readonly_fields = ('instance',)
    #fieldsets = [
     #   (None, {'fields': [('name', 'instances', 'owner')]}),
    #]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'instance', None) is None:
            obj.instance = request.user
        obj.save()