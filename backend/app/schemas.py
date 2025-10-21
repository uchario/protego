from pydantic import BaseModel
from datetime import datetime

class PageVisitCreate(BaseModel):
    url: str
    link_count: int
    word_count: int
    image_count: int

class PageVisitResponse(BaseModel):
    id: int
    url: str
    datetime_visited: datetime
    link_count: int
    word_count: int
    image_count: int

    class Config:
        from_attributes = True