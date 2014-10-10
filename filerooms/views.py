# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.views import generic
from django.views.generic.detail import BaseDetailView
from django.db.models import get_model
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.http import HttpResponseRedirect

from braces import views
from sendfile import sendfile

from .forms import UploadForm, RoomForm


Room = get_model('filerooms', 'Room')
Download = get_model('filerooms', 'Download')


class RoomListView(views.StaffuserRequiredMixin, generic.ListView):
    model = Room
    template_name = 'filerooms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10


class RoomCreateView(views.StaffuserRequiredMixin, generic.CreateView):
    model = Room
    template_name = 'filerooms/room_create.html'
    context_object_name = 'room'
    form_class = RoomForm
    success_url = reverse_lazy('filerooms:room-list')


class RoomDeleteView(views.StaffuserRequiredMixin, generic.DeleteView):
    model = Room
    template_name = 'filerooms/room_confirm_delete.html'
    context_object_name = 'room'
    success_url = reverse_lazy("filerooms:room-list")


class UserDownloadsMixin(object):

    model = Download
    context_object_name = 'downloads'

    def get_queryset(self):
        qs = super(UserDownloadsMixin, self).get_queryset()
        return qs.for_user(user=self.request.user)


class GetRoomMixin(object):

    room_slug_field = 'slug'

    @cached_property
    def room(self):
        qs = Room.objects.for_user(self.request.user)
        return get_object_or_404(
            qs,
            slug=self.kwargs.get(self.room_slug_field, None))

    def get_context_data(self, **kwargs):
        ctx = super(GetRoomMixin, self).get_context_data(**kwargs)
        ctx['room'] = self.room
        return ctx


class RoomDetailView(UserDownloadsMixin, GetRoomMixin, generic.ListView):

    template_name = 'filerooms/room_detail.html'

    def get_queryset(self):
        qs = super(RoomDetailView, self).get_queryset()
        return qs.filter(room=self.room)


class DownloadFileView(UserDownloadsMixin,
                       BaseDetailView):

    def render_to_response(self, context):
        return sendfile(self.request, self.object.attachment.path,
                        attachment=True)


class DownloadCreateView(GetRoomMixin, views.StaffuserRequiredMixin,
                         generic.CreateView):
    model = Download
    template_name = 'filerooms/download_create.html'
    form_class = UploadForm

    def get_success_url(self):
        return reverse_lazy("filerooms:room-detail",
                            kwargs={'slug': self.room.slug})

    def get_form_kwargs(self):
        kwargs = super(DownloadCreateView, self).get_form_kwargs()
        kwargs['room'] = self.room
        return kwargs


class DownloadDeleteView(GetRoomMixin, views.StaffuserRequiredMixin,
                         generic.DeleteView):
    model = Download
    template_name = 'filerooms/download_confirm_delete.html'
    context_object_name = 'download'
    room_slug_field = 'room_slug'

    def get_success_url(self):
        return reverse_lazy("filerooms:room-detail",
                            kwargs={'slug': self.room.slug})
