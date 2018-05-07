# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib import admin

from .models import Institution, Location, Dataset

admin.site.register(Institution)
admin.site.register(Location)
admin.site.register(Dataset)
