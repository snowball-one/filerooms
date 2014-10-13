# -*- coding: utf-8- -*-
from __future__ import unicode_literals

from django.db import models


class CustomStorageFileField(models.FileField):

    def deconstruct(self):
        name, path, args, kwargs = super(CustomStorageFileField,
                                         self).deconstruct()
        if 'storage' in kwargs:
            del kwargs["storage"]
        return name, path, args, kwargs
