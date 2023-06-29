from __future__ import annotations

from pymongo.database import Database, Collection
from pydantic import BaseModel
from pydantic.types import Optional
from bson.objectid import ObjectId
from typing import List

from datetime import datetime, timedelta, date

from app.utils import AppModel
from app.database import database


class InviteLinks(AppModel):
    link: str
    created_at: datetime
    expire_time: timedelta
    used: bool = False
    expired: bool = False
    joined_at: datetime | None = None


class Location(AppModel):
    city: str
    country: str


class Affiliation(AppModel):
    type: str
    name: str
    study_year: int | None = None
    degree: str | None = None
    location: Location


class Events(AppModel):
    event_id: ObjectId
    registered_at: datetime
    check_in_time: datetime | None = None
    check_out_time: datetime | None = None
    attended: bool = False


class Tasks(AppModel):
    status: str
    created_at: datetime
    completed_at: datetime | None = None
    text: str
    issuer_id: ObjectId


class User(AppModel):
    type: Optional[str] = "volunteer"
    photo: Optional[str] | None = None
    gender: str
    telegram_id: Optional[str] | None = None
    telegram_handle: Optional[str] | None = None
    first_name: str
    last_name: str
    instagram: Optional[str] | None = None
    dob: datetime | None = None
    phone_number: str | None = None
    volunteering_hours: int = 0
    password: Optional[str] | None = None
    email: str
    registered_at: datetime | date = datetime.now()
    leaved_at: datetime | None = None
    points: int = 0
    invite_links: List[InviteLinks] | None = None
    location: Location | None = None
    affiliation: Affiliation | None = None
    events: Events | None = None
    tasks: List[Tasks] | None = None
    certificate_requests: List[int] | None = None


class UpdateUser(AppModel):
    _id: ObjectId | None = None
    type: Optional[str] | None = None
    photo: Optional[str] | None = None
    gender: Optional[str] | None = None
    telegram_id: Optional[str] | None = None
    telegram_handle: Optional[str] | None = None
    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    instagram: Optional[str] | None = None
    dob: Optional[datetime] | None = None
    phone_number: Optional[str] | None = None
    email: Optional[str] | None = None
    leaved_at: Optional[datetime] | None = None
    points: Optional[int] | None = None


class VolunteerCollection:
    col: Collection = database['volunteers']

    @classmethod
    def get_volunteer_by_id(cls, id: str | ObjectId):
        if isinstance(id, str):
            id = ObjectId(id)

        v = cls.col.find_one({'_id': id})
        print(v, id)

        if v:
            return User(**v)
        else:
            return None

    @classmethod
    def create_volunteer(cls, v: User):
        v.registered_at = datetime.now()
        print(v)
        print(dict(v))

        result = cls.col.insert_one(v.dict())

        if result.acknowledged:
            return result.inserted_id
        else:
            return False

    @classmethod
    def update_user(cls, v: UpdateUser):
        pass