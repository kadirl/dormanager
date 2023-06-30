from __future__ import annotations

from pymongo.database import Database, Collection
from pydantic import BaseModel, Field
from pydantic.types import Optional
from bson.objectid import ObjectId
from typing import List

from datetime import datetime, timedelta, date

from app.utils import AppModel
from app.database import database


class Event(AppModel):
    name: str
    description: str
    place: str
    time: datetime
    host: ObjectId


class EventsCollection:
    col: Collection = database['event']

    @classmethod
    def create_event(cls, e: Event):

        result = cls.col.insert_one(e.dict())

        if result.acknowledged:
            return result.inserted_id
        else:
            return False

    @classmethod
    def get_event_by_id(cls, id: str | ObjectId):

        if isinstance(id, str): id = ObjectId(id)

        result = cls.col.find_one({'_id': id})

        return Event(**result)

    @classmethod
    def get_upcoming_events(cls):
        result = cls.col.find(
            {'time': {'$gte': datetime.now()}}
        ).sort('time', 1)

        return [Event(**data) for data in result]
