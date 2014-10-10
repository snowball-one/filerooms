File Rooms for Django
=====================

A resuable app for django to provide public and private file rooms.

Installation
------------

    pip install git+https://github.com/snowball-one/fileroom.git


You will then need to add the following to you settings file::

    INSTALL_APP = [
        # Your other apps
        'filerooms',
    ]

    SENDFILE_ROOT = os.path.join(BASE_DIR, 'protected')
    SENDFILE_BACKEND = 'sendfile.backends.nginx'
    SENDFILE_URL = '/protected'


The ``SENDFILE_*`` settings are described in the `django-sendfile`_ package

You will also need to add the ``fileroom`` urls to your top level ``urls.py``::

    urlpatterns = [
        # your existing patterns
        url(r'^rooms/', include('filerooms.urls')),
    ]


.. _django-sendfile: https://github.com/johnsensible/django-sendfile
