# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from . import views


room_patterns = [
    url(r'^$', views.RoomListView.as_view(), name='room-list'),
    url(r'^create/$', views.RoomCreateView.as_view(), name='room-create'),
    url(r'^(?P<slug>[\w-]+)/$', views.RoomDetailView.as_view(),
        name='room-detail'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.RoomDeleteView.as_view(),
        name='room-delete'),
    url(r'^(?P<slug>[\w-]+)/upload/$', views.DownloadCreateView.as_view(),
        name='download-create'),
    url(r'^(?P<room_slug>[\w-]+)/(?P<pk>\d+)/$',
        views.DownloadFileView.as_view(), name='download'),
    url(r'^(?P<room_slug>[\w-]+)/(?P<pk>\d+)/delete/$',
        views.DownloadDeleteView.as_view(), name='download-delete'),
]

# Enforce namespace here so url reverse work correctly
urlpatterns = (
    url(r'', include(room_patterns, namespace='filerooms')),
)
