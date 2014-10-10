# -*- coding: utf-8- -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse_lazy

from . import querysets
from .utils import protected_storage


class AbstractRoom(models.Model):
    name = models.CharField(_('name'), max_length=128)
    slug = models.SlugField(_('slug'), blank=True, unique=True)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                    related_name='rooms',
                                    verbose_name=_('owners'))
    is_public = models.BooleanField(_('public room'), default=False,
                                    help_text=_("If this room is made public, "
                                    "then anyone can see the files in it"))

    objects = querysets.RoomQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AbstractRoom, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.is_public:
            return _("{0} - public").format(self.name)
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('filerooms:room-detail',
                            kwargs={'slug': self.slug})


class AbstractDownload(models.Model):

    name = models.CharField(_("file name"), max_length=128)
    room = models.ForeignKey('filerooms.Room', related_name='downloads',
                             verbose_name=_("file room"))
    description = models.TextField(_("description"))
    attachment = models.FileField(_("attachment"), storage=protected_storage,
                                  upload_to='files/%Y%m')
    created = models.DateTimeField(_("created date"), null=True, blank=True)

    objects = querysets.DownloadQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()
        return super(AbstractDownload, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        path = self.attachment.path
        super(AbstractDownload, self).delete(*args, **kwargs)
        protected_storage.delete(path)

    def __unicode__(self):
        return "{0} uploaded at {1}".format(self.name, self.created)

    # Helpers functions for easy usage in templates

    @property
    def attachment_name(self):
        if self.attachment:
            return self.attachment.name.split('/')[-1]
        return None

    @property
    def extension(self):
        if self.attachment:
            return self.attachment.name.split('/')[-1].split(".")[-1]
        return None

    @property
    def size(self):
        if self.attachment:
            return self.attachment.size
        return None

    def get_absolute_url(self):
        return reverse_lazy('filerooms:download', kwargs={
            'room_slug': self.room.slug, 'pk': self.pk})
