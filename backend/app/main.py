from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel

from .database import engine, get_db, Base
from .models import PageVisit

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/store")
def store_visit(visit: PageVisitCreate, db: Session = Depends(get_db)):
    db_visit = PageVisit(**visit.dict())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

@app.get("/metrics")
def get_metrics(url: str, db: Session = Depends(get_db)):
    visit = db.query(PageVisit).filter(PageVisit.url == url).order_by(PageVisit.datetime_visited.desc()).first()
    if visit:
        return {
            "url": visit.url,
            "link_count": visit.link_count,
            "word_count": visit.word_count,
            "image_count": visit.image_count
        }
    return {
        "url": url,
        "link_count": 0,
        "word_count": 0,
        "image_count": 0
    }

@app.get("/history")
def get_history(url: str, db: Session = Depends(get_db)):
    visits = db.query(PageVisit).filter(PageVisit.url == url).order_by(PageVisit.datetime_visited.desc()).all()
    if len(visits) > 1:
        return [v.datetime_visited.isoformat() for v in visits[:]]
    return []