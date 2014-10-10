# -*- coding: utf-8- -*-
from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.conf import settings


protected_storage = FileSystemStorage(location=settings.SENDFILE_ROOT)
