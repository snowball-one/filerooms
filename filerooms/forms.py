from __future__ import unicode_literals, absolute_import

from django import forms
from django.db.models import get_model
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


Room = get_model('filerooms', 'Room')
Download = get_model('filerooms', 'Download')


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('name', 'owners', 'is_public')

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Room.objects.all()
        if self.instance and self.instance.pk:
            # this is an update so we need to exclude existing
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(slug=slugify(name)).exists():
            raise forms.ValidationError(
                _('a file room of this name already exists')
            )
        return name


class UploadForm(forms.ModelForm):

    def __init__(self, room, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.instance.room = room

    class Meta:
        model = Download
        fields = ('name', 'description', 'attachment')
