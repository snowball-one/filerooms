# -*- coding: utf-8- -*-
from __future__ import unicode_literals

import factory

from django.db.models import get_model
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


Room = get_model('filerooms', 'Room')
Download = get_model('filerooms', 'Download')
User = get_user_model()


class NormalUserFactory(factory.DjangoModelFactory):

    is_superuser = False
    is_staff = False
    is_active = True
    first_name = factory.Sequence(lambda n: 'first-{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'last-{0}'.format(n))
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@snowballone.com.au'.format(n))
    password = make_password('test')

    class Meta:
        model = User


class StaffUserFactory(NormalUserFactory):
    is_staff = True


class SuperUserFactory(NormalUserFactory):
    is_superuser = True


class RoomFactory(factory.DjangoModelFactory):

    is_public = False
    name = factory.Sequence(lambda n: 'room {0}'.format(n))

    class Meta:
        model = Room

    @factory.post_generation
    def owners(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.owners.add(user)


class DownloadFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'download {0}'.format(n))
    description = factory.Sequence(lambda n: 'description {0}'.format(n))
    room = factory.SubFactory(RoomFactory)

    class Meta:
        model = Download

