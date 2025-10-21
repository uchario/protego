import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, PageVisit
from app.repositories import PageVisitRepository
from app.schemas import PageVisitCreate
from app.exceptions import DatabaseError

# In-memory SQLite for testing
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_page_visit(db):
    visit_data = PageVisitCreate(
        url="http://example.com",
        link_count=10,
        word_count=100,
        image_count=5
    )
    visit = PageVisitRepository.create(db, visit_data)
    assert visit.url == "http://example.com"
    assert visit.link_count == 10
    assert visit.word_count == 100
    assert visit.image_count == 5
    assert visit.id is not None

def test_get_latest_by_url(db):
    visit_data = PageVisitCreate(
        url="http://example.com",
        link_count=10,
        word_count=100,
        image_count=5
    )
    PageVisitRepository.create(db, visit_data)
    visit = PageVisitRepository.get_latest_by_url(db, "http://example.com")
    assert visit.url == "http://example.com"
    assert visit.link_count == 10

def test_get_all_by_url(db):
    visit_data1 = PageVisitCreate(
        url="http://example.com",
        link_count=10,
        word_count=100,
        image_count=5
    )
    visit_data2 = PageVisitCreate(
        url="http://example.com",
        link_count=20,
        word_count=200,
        image_count=10
    )
    PageVisitRepository.create(db, visit_data1)
    PageVisitRepository.create(db, visit_data2)
    visits = PageVisitRepository.get_all_by_url(db, "http://example.com")
    assert len(visits) == 2
    assert visits[0].link_count == 20  # Latest visit
    assert visits[1].link_count == 10