# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db.models.query import QuerySet
from django.db.models import Q


class RoomQuerySet(QuerySet):

    def for_user(self, user):
        if not user.is_authenticated():
            return self.filter(is_public=True)
        if user.is_staff or user.is_superuser:
            return self
        try:
            q = Q(owners=user) | Q(is_public=True)
            return self.filter(q)
        except AttributeError:
            return self.none()


class DownloadQuerySet(QuerySet):

    def for_user(self, user):
        if not user.is_authenticated():
            return self.filter(room__is_public=True)
        if user.is_staff or user.is_superuser:
            return self
        try:
            q = Q(room__owners=user) | Q(room__is_public=True)
            return self.filter(q)
        except AttributeError:
            return self.none()

    def public(self):
        try:
            return self.filter(room__is_public=True)
        except AttributeError:
            return self.none()
