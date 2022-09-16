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
from helper.wallet import WalletHelper
from lib import BadRequest
from schemas.user import AuthSchema
from schemas.wallet import AddressParam, WalletForm


class WalletResource(Resource):
    @security.http(
        params=AddressParam()
    )
    def get(self, params):
        _msg, _nonce = WalletHelper.get_sign_msg(address=get(params, 'address'))
        return {
            'message': _msg,
            'nonce': _nonce
        }

    @security.http(
        form_data=WalletForm(),
        response=AuthSchema()
    )
    def post(self, form_data):
        _device_id = request.headers.get('did', default='')
        _xrip = request.headers.get('xrip', default='')
        _geoip = request.headers.get('geoip', default='')
        _user = WalletHelper.verify(
            address=get(form_data, 'address'),
            signature=get(form_data, 'signature'),
            nonce=get(form_data, 'nonce')
        )
        if not _user:
            raise BadRequest(msg="Invalid", errors=[{
                'signature': 'Invalid'
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
