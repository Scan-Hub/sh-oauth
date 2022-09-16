# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, pre_dump


class AddressParam(Schema):
    class Meta:
        unknown = EXCLUDE

    address = fields.Str(required=True)

    @pre_dump
    def to_lower(self, data, *args, **kwargs):
        data['address'] = data['address'].lower()
        return data


class WalletForm(Schema):
    class Meta:
        unknown = EXCLUDE

    address = fields.Str(required=True)
    signature = fields.Str(required=True)
    nonce = fields.Int(required=True)

    @pre_dump
    def to_lower(self, data, *args, **kwargs):
        data['address'] = data['address'].lower()
        return data
