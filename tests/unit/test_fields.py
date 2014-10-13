# -*- coding: utf-8 -*-
from filerooms import fields


def test_custom_file_field_omits_storage_for_deconstruct():
    field = fields.CustomStorageFileField(("a_field"), storage={})
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs
