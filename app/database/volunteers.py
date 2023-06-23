from pymongo.database import Database
from pydantic import BaseModel

from app.database import client


class VolunteerBaseSchema(BaseModel):
    id: str | None = None
    title: str
    content: str
    category: str = ""
    published: bool = False
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class VolunteerCollection:
    def __init__(self, database: Database):
        self.db = database['volunteers']


