# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import pytest

@pytest.fixture
def webtest_csrf_checks():
    return True


@pytest.fixture(scope='function')
def webtest(request, webtest_csrf_checks, transactional_db):
    """
    Provide the "app" object from WebTest as a fixture

    Taken and adapted from https://gist.github.com/magopian/6673250
    """
    from django_webtest import DjangoTestApp, WebTestMixin

    # Patch settings on startup
    wtm = WebTestMixin()
    wtm.csrf_checks = webtest_csrf_checks
    wtm._patch_settings()

    # Unpatch settings on teardown
    request.addfinalizer(wtm._unpatch_settings)

    return DjangoTestApp()
