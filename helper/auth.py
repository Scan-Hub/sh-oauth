# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import base64
from datetime import timedelta

from bson import json_util
from eth_account.messages import encode_defunct
from pydash import get
from web3 import Web3

from config import Config
from enums import UserTypes
from lib import dt_utcnow
from models import SessionModel

_web3 = Web3()


class AuthHelper:

    @staticmethod
    def sign_token(user, session) -> str:
        """
            Gen token for authentication http
        :param session:
        :param user:
        :return:
        """
        _exp_time = dt_utcnow() + timedelta(seconds=Config.TOKEN_EXP)

        _msg = json_util.dumps({
            'exp': _exp_time,
            'iat': dt_utcnow(),
            'payload': {
                '_id': get(user, '_id'),
                'roles': get(user, 'roles', []),
                'address': get(user, 'address', ''),
                'type': UserTypes.NON_BLOCKCHAIN if not get(user, 'address', '') else UserTypes.BLOCKCHAIN
            }
        })
        _message = encode_defunct(text=_msg)
        _signature = _web3.eth.account.sign_message(_message, Config.SIGN_PRIVATE).signature
        _token = json_util.dumps({
            'signature': _signature.hex(),
            'payload': _msg
        })
        _token = base64.b64encode(_token.encode()).decode()
        SessionModel.record(
            user=get(user, '_id'),
            session={
                **session,
                'access_token': _token,
                'created_by': str(user)
            }
        )
        return _token
