# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models import get_model

from .. import factories


Room = get_model('filerooms', 'Room')
Download = get_model('filerooms', 'Download')


def get_rooms(owners=[]):
    return {
        'public': factories.RoomFactory(owners=owners, is_public=True),
        'private': factories.RoomFactory(owners=owners)
    }

def get_downloads(owners=[]):
    rooms = get_rooms(owners=owners)
    return {
        'public': factories.DownloadFactory(room=rooms['public']),
        'private': factories.DownloadFactory(room=rooms['private'])
    }


# Room Queryset

def test_room_qs_for_user_returns_all_for_staff_user(db):
    user = factories.StaffUserFactory()
    get_rooms()
    assert Room.objects.for_user(user).count() == 2


def test_room_qs_for_user_returns_all_for_super_users(db):
    user = factories.SuperUserFactory()
    get_rooms()
    assert Room.objects.for_user(user).count() == 2


def test_room_qs_for_user_returns_only_public_for_non_owner(db):
    user = factories.NormalUserFactory()
    rooms = get_rooms()
    assert Room.objects.for_user(user).count() == 1
    assert rooms['public'] == Room.objects.for_user(user).all()[0]

def test_room_qs_for_user_return_owned_rooms(db):
    user = factories.NormalUserFactory()
    get_rooms(owners=[user])
    assert Room.objects.for_user(user).count() == 2


# Download Queryset


def test_download_qs_for_user_returns_all_for_staff_user(db):
    user = factories.StaffUserFactory()
    get_downloads()
    assert Download.objects.for_user(user).count() == 2


def test_download_qs_for_user_returns_all_for_super_user(db):
    user = factories.SuperUserFactory()
    get_downloads()
    assert Download.objects.for_user(user).count() == 2


def test_download_qs_for_user_returns_only_public_for_non_owner(db):
    user = factories.NormalUserFactory()
    downloads = get_downloads()
    assert Download.objects.for_user(user).count() == 1
    assert downloads['public'] in Download.objects.for_user(user).all()
    assert downloads['private'] not in Download.objects.for_user(user).all()


def test_download_qs_for_user_returns_downloads_for_owned_rooms(db):
    user = factories.NormalUserFactory()
    get_downloads(owners=[user])
    assert Download.objects.for_user(user).count() == 2


def test_download_qs_public_returns_only_public_downloads(db):
    downloads = get_downloads()
    assert Download.objects.public().count() == 1
    assert downloads['public'] in Download.objects.public().all()
    assert downloads['private'] not in Download.objects.public().all()
