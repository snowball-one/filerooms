# -*- coding: utf-8- -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from .utils import protected_storage


class ProtectedStorageFileField(models.FileField):

    def __init__(self, verbose_name=None, name=None, upload_to='', **kwargs):
        kwargs['storage'] = protected_storage
        super(ProtectedStorageFileField, self).__init__(verbose_name=None,
            name=None, upload_to='', **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ProtectedStorageFileField,
                                         self).deconstruct()
        if 'storage' in kwargs:
            del kwargs["storage"]
        return name, path, args, kwargs
