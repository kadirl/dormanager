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
    number: int
    rating: float = 5.0
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
        room = cls.get_room_by_number(number)
        room_rating = room.rating
        room_ratings_count = max(1, len(room.ratings))

        cls.col.update_one(
            {'number': number},
            {
                '$set': {
                    'rating': (room_rating * room_ratings_count + rating.rating) / (room_ratings_count + 1)
                },
                '$push': {'ratings': rating.dict()}
            }
        )

    @classmethod
    def get_all_rooms(cls):
        result = cls.col.find().sort('rating', -1)

        return [Room(**data) for data in result]
