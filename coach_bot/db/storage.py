from pymongo import MongoClient, errors
import functools
from os import environ


MONGO_DB_PORT = int(environ['MONGO_DB_PORT'])
MONGO_DB_ADDR = environ['MONGO_DB_ADDR']


def log_action_wrapper(method_to_decorate):
    @functools.wraps(method_to_decorate)
    def fun(self, *args, **kwargs):
        self._db.logs.insert_one({"action": method_to_decorate.__name__,
                                 "args": args})
        method_to_decorate(self, *args, **kwargs)
    return fun


class MongodbService:
    _instance = None
    _client = None
    _db = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._client = MongoClient(MONGO_DB_ADDR, MONGO_DB_PORT)
        self._db = self._client.coach_bot_db

    def get_data_users(self):
        return list(self._db.users_id.find())

    def get_data_chats(self):
        return list(self._db.chats_id.find())

    @log_action_wrapper
    def save_chat(self, dto):
        try:
            self._db.chats_id.insert_one({"_id": dto})
        except errors.DuplicateKeyError:
            pass

    @log_action_wrapper
    def save_user(self, dto):
        try:
            self._db.users_id.insert_one({"_id": dto})
        except errors.DuplicateKeyError:
            pass

    @log_action_wrapper
    def remove_chat(self, dto):
        self._db.chats_id.delete_one({"_id": dto})

    @log_action_wrapper
    def remove_user(self, dto):
        self._db.users_id.delete_one({"_id": dto})
