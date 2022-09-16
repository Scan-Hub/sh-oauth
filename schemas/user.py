# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate

from contains import Regexps
from lib import ObjectIdField, DatetimeField


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    display_name = fields.Str(missing='')

    avatar = fields.Str(missing='')
    # username = fields.Str(missing='')
    # user_address = fields.Str(missing='')
    phone = fields.Str(validate=validate.Regexp(regex=Regexps.phone), missing='')
    birthday = DatetimeField(default=None)
    gender = fields.Str(validate=validate.OneOf([
        'male',
        'female',
        'other'
    ]))


class ViewUserSchema(UserSchema):
    class Meta:
        unknown = EXCLUDE

    _id = ObjectIdField(required=True)
    address = fields.Str(missing='')
    email = fields.Email(missing='')


class AuthSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    access_token = fields.Str(required=True)
    user = fields.Nested(UserSchema)
