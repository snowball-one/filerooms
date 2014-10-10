# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models import get_model
from django.contrib import admin


class RoomAdmin(admin.ModelAdmin):
    fields = ('name', 'owners', 'is_public')
    list_display = ('name', 'is_public')


class DownloadAdmin(admin.ModelAdmin):
    fields = ('room', 'name', 'description', 'attachment')
    list_display = ('room', 'name', 'description', 'created')


admin.site.register(get_model('filerooms', 'Room'), RoomAdmin)
admin.site.register(get_model('filerooms', 'Download'), DownloadAdmin)
