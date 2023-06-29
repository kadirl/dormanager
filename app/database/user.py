from __future__ import annotations

from pymongo.database import Database, Collection
from pydantic import BaseModel
from pydantic.types import Optional
from bson.objectid import ObjectId
from typing import List

from datetime import datetime, timedelta, date

from app.utils import AppModel
from app.database import database


class UserNotifications(AppModel):
    events: bool = True
    offers: bool = True
    regular: bool = True


class User(AppModel):
    tg_id: str
    chat_id: str
    name: str
    room: int
    notification_settings: UserNotifications = UserNotifications()
    registered_at: datetime | None = datetime.now()


class UserCollection:
    col: Collection = database['user']

    @classmethod
    def create_user(cls, u: User):

        result = cls.col.insert_one(u.dict())

        if result.acknowledged:
            return result.inserted_id
        else:
            return False

    @classmethod
    def get_user_by_id(cls, id: str):
        if not isinstance(id, ObjectId):
            id = ObjectId(id)

        result = cls.col.find_one({'_id': id})

        return User(**result)

    @classmethod
    def get_user_by_tg_id(cls, id: int | str):
        if isinstance(id, int):
            id = str(id)

        result = cls.col.find_one({'tg_id': id})

        if result:
            return User(**result)

    @classmethod
    def get_all_users(cls):
        result = cls.col.find()

        return [User(**data) for data in result]

    @classmethod
    def get_regular_notification_allowed_users(cls):
        result = cls.col.find({'notification_settings.regular': True})

        return [User(**data) for data in result]

    @classmethod
    def get_events_notification_allowed_users(cls):
        result = cls.col.find({'notification_settings.events': True})

        return [User(**data) for data in result]

    @classmethod
    def get_offers_notification_allowed_users(cls):
        result = cls.col.find({'notification_settings.offers': True})

        return [User(**data) for data in result]