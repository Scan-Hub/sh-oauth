# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import request
from flask_restful import Resource
from pydash import get

from connect import security
from helper.auth import AuthHelper
from helper.firebase import FirebaseHelper
from lib import BadRequest
from models import UserModel
from schemas.user import AuthSchema, ViewUserSchema
from schemas.firebase import ConnectProviderForm


class FirebaseResource(Resource):

    @security.http(
        login_required=True,
        form_data=ConnectProviderForm(),
        response=ViewUserSchema()
    )
    def put(self, form_data, user):
        _user_form_token = FirebaseHelper.get_user(get(form_data, 'token'))
        if not _user_form_token:
            raise BadRequest(msg="Invalid", errors=[{
                'token': 'Invalid'
            }])
        _exists = UserModel.user_of_email(email=get(_user_form_token, 'email'))

        if _exists:
            raise BadRequest(msg='Email already exists.')

        UserModel.update_one({
            '_id': get(user, '_id')
        }, obj={
            'email': get(_user_form_token, 'email'),
            'updated_by': str(get(user, '_id'))
        }, worker=True)

        return {
            **user,
            'email': get(_user_form_token, 'email')
        }

    @security.http(
        form_data=ConnectProviderForm(),
        response=AuthSchema()
    )
    def post(self, form_data):
        _user = FirebaseHelper.verify(get(form_data, 'token'))
        if not _user:
            raise BadRequest(msg="Invalid", errors=[{
                'token': 'Invalid'
            }])
        _access_token = AuthHelper.sign_token(user=_user,
                                              session={
                                                  'headers': dict(request.headers),
                                                  'params': request.args.to_dict(),
                                                  'form_data': form_data
                                              })
        return {
            'access_token': _access_token,
            'user': _user
        }
