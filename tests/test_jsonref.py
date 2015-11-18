# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define unit tests to test core functionality."""

from __future__ import absolute_import

from jsonref import JsonRef, JsonRefError
import pytest

from jsonresolver import JSONResolver
from jsonresolver.contrib.jsonref import json_loader_factory


def test_key_resolver():
    """Test JSONSchema validation with custom reference resolver."""
    example_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            'authors': {'$ref': 'http://localhost:4000/schema/authors.json#'}
        },
        'additionalProperties': False,
    }

    json_resolver = JSONResolver(plugins=['demo.schema'])
    loader_cls = json_loader_factory(json_resolver)
    loader = loader_cls()
    data = JsonRef.replace_refs(example_schema, loader=loader)
    assert data['properties']['authors'] == {'type': 'array'}


def test_missing_route():
    """Test orignal resolver."""
    example_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            'authors': {'$ref': 'file:///missing.json#'}
        },
        'additionalProperties': False,
    }

    json_resolver = JSONResolver(plugins=['demo.schema'])
    loader_cls = json_loader_factory(json_resolver)
    loader = loader_cls()
    data = JsonRef.replace_refs(example_schema, loader=loader)
    with pytest.raises(JsonRefError):
        data['properties']['authors']['type']