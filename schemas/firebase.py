# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate

from enums.provider import Providers


class ConnectProviderForm(Schema):
    class Meta:
        unknown = EXCLUDE

    token = fields.Str(required=True)
    # type = fields.Str(required=True, validate=validate.OneOf([Providers.GOOGLE]))
