# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import AsyncDaoModel
from connect import connect_db, redis_cluster, asyncio_mongo
from models.session import SessionDao
from models.user import UserDao

__models__ = ['UserModel', 'SessionModel']

UserModel = UserDao(connect_db.db.users, redis=redis_cluster, broker=Config.BROKER_URL, project=Config.PROJECT)
SessionModel = SessionDao(connect_db.db.sessions, redis=redis_cluster,broker=Config.BROKER_URL, project=Config.PROJECT)
