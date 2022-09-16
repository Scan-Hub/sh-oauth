# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from lib import DaoModel


class SessionDao(DaoModel):

    def __init__(self, *args, **kwargs):
        super(SessionDao, self).__init__(*args, **kwargs)

    def record(self, user, session):
        self.redis.set(f'tokens:{user}:{get(session, "access_token")}', 1)
        self.insert_one({
            'user_id': user,
            **session
        }, worker=True)
