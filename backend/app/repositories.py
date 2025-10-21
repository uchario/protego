from sqlalchemy.orm import Session
from .models import PageVisit
from .schemas import PageVisitCreate
from .exceptions import DatabaseError
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    if 'google.com' in parsed.netloc:
        query = parse_qs(parsed.query)
        query.pop('zx', None)
        query.pop('no_sw_cr', None)
    elif 'youtube.com' in parsed.netloc and parsed.path == '/watch':
        query = parse_qs(parsed.query)
        query.pop('t', None)  # Remove timestamp parameter
    else:
        return url  # No normalization for other URLs
    new_query = urlencode(query, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

class PageVisitRepository:
    @staticmethod
    def create(db: Session, visit: PageVisitCreate) -> PageVisit:
        try:
            visit_dict = visit.dict()
            visit_dict['url'] = normalize_url(visit_dict['url'])
            db_visit = PageVisit(**visit_dict)
            db.add(db_visit)
            db.commit()
            db.refresh(db_visit)
            return db_visit
        except Exception as e:
            db.rollback()
            raise DatabaseError(f"Failed to create page visit: {str(e)}")

    @staticmethod
    def get_latest_by_url(db: Session, url: str) -> PageVisit:
        try:
            normalized_url = normalize_url(url)
            return (
                db.query(PageVisit)
                .filter(PageVisit.url == normalized_url)
                .order_by(PageVisit.datetime_visited.desc())
                .first()
            )
        except Exception as e:
            raise DatabaseError(f"Failed to retrieve latest visit: {str(e)}")

    @staticmethod
    def get_all_by_url(db: Session, url: str) -> list[PageVisit]:
        try:
            normalized_url = normalize_url(url)
            return (
                db.query(PageVisit)
                .filter(PageVisit.url == normalized_url)
                .order_by(PageVisit.datetime_visited.desc())
                .all()
            )
        except Exception as e:
            raise DatabaseError(f"Failed to retrieve visit history: {str(e)}")