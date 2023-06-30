from __future__ import annotations

from pymongo.database import Database, Collection
from pydantic import BaseModel
from pydantic.types import Optional
from bson.objectid import ObjectId
from typing import List

from datetime import datetime, timedelta, date

from app.utils import AppModel
from app.database import database


class Offer(AppModel):
    _id: ObjectId = ObjectId()
    issuer_id: ObjectId
    text: str | None = None


class OfferCollection:
    col: Collection = database['offer']

    @classmethod
    def create_offer(cls, o: Offer):

        result = cls.col.insert_one(o.dict())

        if result.acknowledged:
            return result.inserted_id
        else:
            return False

    @classmethod
    def get_offer_by_id(cls, id: str | ObjectId):
        if isinstance(id, str):
            id = ObjectId(id)

        result = cls.col.find_one({'_id': id})

        return Offer(**result)

    @classmethod
    def get_offer_by_issuer_id(cls, id: str | ObjectId):
        if isinstance(id, str):
            id = ObjectId(id)

        result = cls.col.find_one({'issuer_id': id}, sort=[('_id', 1)])

        return Offer(**result)
