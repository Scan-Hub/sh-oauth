# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from models import UserModel
from schemas.user import UserSchema, ViewUserSchema


class UserResource(Resource):
    @security.http(
        login_required=True,
        response=ViewUserSchema()
    )
    def get(self, user):
        _user = UserModel.find_one({
            '_id': get(user, '_id')
        }, cache=True)
        return _user

    @security.http(
        login_required=True,
        response=ViewUserSchema(),
        form_data=UserSchema()
    )
    def put(self, form_data, user):
        print({'_id': get(user, '_id')})
        UserModel.update_one({
            '_id': get(user, '_id')
        }, obj={
            **form_data,
            'updated_by': str(get(user, '_id'))
        }, worker=True)

        return {
            **user,
            **form_data
        }
