from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from .database import Base

class PageVisit(Base):
    __tablename__ = "page_visits"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    datetime_visited = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    link_count = Column(Integer)
    word_count = Column(Integer)
    image_count = Column(Integer)