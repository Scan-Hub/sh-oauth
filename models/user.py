# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import DaoModel


class UserDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(UserDao, self).__init__(*args, **kwargs)

    def user_of_address(self, address, upsert=False):
        _user = self.find_one({
            'address': address
        })
        print('_user', _user)
        if not _user and upsert:
            _user = self.insert_one({
                'address': address,
                'created_by': Config.PROJECT
            }, worker=True)
        return _user

    def user_of_email(self, email, info={}, upsert=False):
        _user = self.find_one({
            'email': email
        })
        if not _user and upsert:
            _user = self.insert_one({
                'email': email,
                'created_by': Config.PROJECT,
                **info
            }, worker=True)
        return _user
