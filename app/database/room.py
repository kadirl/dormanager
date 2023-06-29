from __future__ import annotations

from pymongo.database import Database, Collection
from pydantic import BaseModel
from pydantic.types import Optional
from bson.objectid import ObjectId
from typing import List

from datetime import datetime, timedelta, date

from app.utils import AppModel
from app.database import database


class RoomRating(AppModel):
    rating: int
    text: str
    sender_id: ObjectId


class Room(AppModel):
    number: str
    ratings: List[RoomRating | None] = []


class RoomCollection:
    col: Collection = database['room']

    @classmethod
    def create_room(cls, r: Room):

        result = cls.col.insert_one(r.dict())

        if result.acknowledged:
            return result.inserted_id
        else:
            return False

    @classmethod
    def get_room_by_number(cls, number: int):

        result = cls.col.find_one({'number': number})

        return Room(**result)

    @classmethod
    def add_room_rating(cls, number: int, rating: RoomRating):

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

    @classmethod
    def update_notification_settings_by_tg_id(cls, tg_id: str, settings: UserNotifications):
        cls.col.update_one(
            {'tg_id': tg_id},
            {'$set':{
                'notification_settings': settings.dict()
            }}
        )
