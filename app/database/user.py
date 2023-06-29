from __future__ import annotations

from pymongo.database import Database, Collection
from pydantic import BaseModel
from pydantic.types import Optional
from bson.objectid import ObjectId
from typing import List

from datetime import datetime, timedelta, date

from app.utils import AppModel
from app.database import database


class User(AppModel):
    tg_id: str
    name: str
    room: int
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
