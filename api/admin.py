# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Institution, Location, Dataset

admin.site.register(Institution)
admin.site.register(Location)
admin.site.register(Dataset)
