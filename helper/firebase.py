# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from firebase_admin import auth
from pydash import get

from lib.logger import debug
from models import UserModel


class FirebaseHelper:
    @staticmethod
    def get_user(token):
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            return {
                'display_name': user.display_name,
                'avatar': user.photo_url,
                'email': user.email.lower(),
                'firebase_info': user.__dict__.get('_data')
            }
        except:
            debug("Login with firebase error", str(e))
            pass
        return False

    @classmethod
    def verify(cls, token):
        try:
            user = cls.get_user(token)
            if not user:
                return False

            _user = UserModel.user_of_email(email=get(user, 'email'), info=user, upsert=True)
            return _user
        except Exception as e:
            print("Error")
            debug("Login with firebase error", str(e))

        return False
