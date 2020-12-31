from pymongo import MongoClient, errors


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
        self._client = MongoClient("localhost", 27017)
        self._db = self._client.coach_bot_db

    def get_data_users(self):
        return list(self._db.users_id.find())

    def get_data_chats(self):
        return list(self._db.chats_id.find())

    def save_chat(self, dto):
        try:
            self._db.chats_id.insert_one({"_id": dto})
        except errors.DuplicateKeyError:
            pass

    def save_user(self, dto):
        try:
            self._db.users_id.insert_one({"_id": dto})
        except errors.DuplicateKeyError:
            pass

    def remove_chat(self, dto):
        self._db.chats_id.delete_one({"_id": dto})

    def remove_user(self, dto):
        self._db.users_id.delete_one({"_id": dto})
