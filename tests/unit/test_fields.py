# -*- coding: utf-8 -*-
from filerooms import fields


def test_protected_file_field_omits_storage_for_deconstruct():
    field = fields.ProtectedStorageFileField(("a_field"))
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs
