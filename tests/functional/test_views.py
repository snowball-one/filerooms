# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from webtest import Upload

from .. import factories


def get_rooms(owners=None):
    return {
        'public': factories.RoomFactory(owners=owners, is_public=True),
        'private': factories.RoomFactory(owners=owners)
    }

# Room list view

def test_super_user_can_see_all_rooms(webtest):
    user = factories.SuperUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-list'), user=user)
    assert rooms['public'].name in response
    assert rooms['private'].name in response


def test_staff_user_can_see_all_rooms(webtest):
    user = factories.StaffUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-list'), user=user)
    assert rooms['public'].name in response
    assert rooms['private'].name in response


def test_normal_user_cannot_see_unowned_rooms(webtest):
    user = factories.NormalUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-list'), user=user)
    assert rooms['public'].name in response
    assert rooms['private'].name not in response


def test_normal_user_can_see_owned_rooms(webtest):
    user = factories.NormalUserFactory()
    rooms = get_rooms([user])
    response = webtest.get(reverse('filerooms:room-list'), user=user)
    assert rooms['public'].name in response
    assert rooms['private'].name in response


def test_staff_user_can_see_add_room(webtest):
    user = factories.StaffUserFactory()
    response = webtest.get(reverse('filerooms:room-list'), user=user)
    assert reverse('filerooms:room-create') in response


def test_super_user_can_see_add_room(webtest):
    user = factories.SuperUserFactory()
    response = webtest.get(reverse('filerooms:room-list'), user=user)
    assert reverse('filerooms:room-create') in response


def test_normal_user_cannot_see_add_room(webtest):
    user = factories.NormalUserFactory()
    response = webtest.get(reverse('filerooms:room-list'), user=user)
    assert reverse('filerooms:room-create') not in response


# Room create view

def test_staff_user_can_create_room(webtest):
    user = factories.StaffUserFactory()
    response = webtest.get(reverse('filerooms:room-create'), user=user)
    form = response.form
    form['name'] = 'a test room'
    form['is_public'] = True
    response = form.submit().follow()
    assert 'a test room' in response

def test_super_user_can_create_room(webtest):
    user = factories.SuperUserFactory()
    response = webtest.get(reverse('filerooms:room-create'), user=user)
    form = response.form
    form['name'] = 'a test room'
    form['is_public'] = True
    response = form.submit().follow()
    assert 'a test room' in response

def test_normal_user_cannot_create_room(webtest):
    user = factories.NormalUserFactory()
    response = webtest.get(reverse('filerooms:room-create'), user=user)
    assert response.status_int == 302


# Download list view

def test_staff_user_can_view_private_room(webtest):
    user = factories.StaffUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-detail', kwargs={
        'slug': rooms['private'].slug}), user=user)
    response.status_int = 200

def test_super_user_can_view_private_room(webtest):
    user = factories.SuperUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-detail', kwargs={
        'slug': rooms['private'].slug}), user=user)
    response.status_int = 200

def test_normal_user_can_view_private_room(webtest):
    user = factories.NormalUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-detail', kwargs={
        'slug': rooms['private'].slug}), user=user, status=404)
    response.status_int = 404


# Room delete view

def test_staff_user_can_delete_room(webtest):
    user = factories.StaffUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-delete', kwargs={
        "slug": rooms['public'].slug}), user=user)
    response = response.form.submit()
    assert response.status_int == 302
    assert response.follow().status_int == 200


def test_super_user_can_delete_room(webtest):
    user = factories.SuperUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-delete', kwargs={
        "slug": rooms['public'].slug}), user=user)
    response = response.form.submit()
    assert response.status_int == 302
    assert response.follow().status_int == 200


def test_normal_user_cannot_delete_room(webtest):
    user = factories.NormalUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:room-delete', kwargs={
        "slug": rooms['public'].slug}), user=user)
    assert response.status_int == 302


# Create download view

def test_staff_user_can_create_download(webtest):
    user = factories.StaffUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:download-create', kwargs={
        'slug': rooms['public'].slug,
    }), user=user)
    form = response.form
    form['name'] = 'a download'
    form['description'] = 'a description'
    form['attachment'] = Upload('file.txt', 'content')
    response = form.submit().follow()
    assert  'a download' in response

def test_super_user_can_create_download(webtest):
    user = factories.SuperUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:download-create', kwargs={
        'slug': rooms['public'].slug,
    }), user=user)
    form = response.form
    form['name'] = 'a download'
    form['description'] = 'a description'
    form['attachment'] = Upload('file.txt', 'content')
    response = form.submit().follow()
    assert  'a download' in response

def test_normal_user_cannot_create_download(webtest):
    user = factories.NormalUserFactory()
    rooms = get_rooms()
    response = webtest.get(reverse('filerooms:download-create', kwargs={
        'slug': rooms['public'].slug,
    }), user=user)
    assert response.status_int == 302


# Download delete view

def test_staff_user_can_delete_a_download(webtest):
    user = factories.StaffUserFactory()
    rooms = get_rooms()
    download = factories.DownloadFactory(room=rooms['public'])
    response = webtest.get(reverse('filerooms:download-delete', kwargs={
        'room_slug': rooms['public'].slug,
        'pk': download.pk
    }), user=user)
    response = response.form.submit()
    assert response.status_int == 302
    assert response.follow().status_int == 200


def test_super_user_can_delete_a_download(webtest):
    user = factories.SuperUserFactory()
    rooms = get_rooms()
    download = factories.DownloadFactory(room=rooms['public'])
    response = webtest.get(reverse('filerooms:download-delete', kwargs={
        'room_slug': rooms['public'].slug,
        'pk': download.pk
    }), user=user)
    response = response.form.submit()
    assert response.status_int == 302
    assert response.follow().status_int == 200


def test_normal_user_cannot_delete_a_download(webtest):
    user = factories.NormalUserFactory()
    rooms = get_rooms()
    download = factories.DownloadFactory(room=rooms['public'])
    response = webtest.get(reverse('filerooms:download-delete', kwargs={
        'room_slug': rooms['public'].slug,
        'pk': download.pk
    }), user=user)
    assert response.status_int == 302
