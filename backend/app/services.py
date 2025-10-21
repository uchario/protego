from sqlalchemy.orm import Session
from .repositories import PageVisitRepository
from .schemas import PageVisitCreate, PageVisitResponse
from .exceptions import NotFoundError
from datetime import datetime

class PageVisitService:
    @staticmethod
    def create_visit(db: Session, visit: PageVisitCreate) -> PageVisitResponse:
        db_visit = PageVisitRepository.create(db, visit)
        return PageVisitResponse.from_orm(db_visit)

    @staticmethod
    def get_latest_metrics(db: Session, url: str) -> dict:
        visit = PageVisitRepository.get_latest_by_url(db, url)
        if visit:
            return {
                "url": visit.url,
                "link_count": visit.link_count,
                "word_count": visit.word_count,
                "image_count": visit.image_count,
            }
        return {"url": url, "link_count": 0, "word_count": 0, "image_count": 0}

    @staticmethod
    def get_visit_history(db: Session, url: str) -> list[str]:
        visits = PageVisitRepository.get_all_by_url(db, url)
        if not visits:
            raise NotFoundError(f"No visits found for URL: {url}")

        iso_list: list[str] = []
        for v in visits:
            dt = getattr(v, "datetime_visited", None)
            if isinstance(dt, datetime):
                iso_list.append(dt.isoformat())
            elif isinstance(dt, str):
                # Already a string (as in tests' monkeypatch)
                iso_list.append(dt)
            else:
                raise TypeError("datetime_visited must be datetime or ISO string")
        return iso_list