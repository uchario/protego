import pytest
from sqlalchemy.orm import Session
from app.services import PageVisitService
from app.schemas import PageVisitCreate
from app.exceptions import NotFoundError
from unittest.mock import Mock

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def mock_repository():
    return Mock()

def test_create_visit(mock_db, mock_repository, monkeypatch):
    visit_data = PageVisitCreate(
        url="http://example.com",
        link_count=10,
        word_count=100,
        image_count=5
    )
    mock_visit = Mock(
        url="http://example.com",
        link_count=10,
        word_count=100,
        image_count=5,
        id=1,
        datetime_visited="2025-10-21T12:00:00"
    )
    monkeypatch.setattr("app.services.PageVisitRepository.create", lambda db, visit: mock_visit)
    result = PageVisitService.create_visit(mock_db, visit_data)
    assert result.url == "http://example.com"
    assert result.link_count == 10
    assert result.id == 1

def test_get_latest_metrics_found(mock_db, mock_repository, monkeypatch):
    mock_visit = Mock(
        url="http://example.com",
        link_count=10,
        word_count=100,
        image_count=5
    )
    monkeypatch.setattr("app.services.PageVisitRepository.get_latest_by_url", lambda db, url: mock_visit)
    result = PageVisitService.get_latest_metrics(mock_db, "http://example.com")
    assert result["url"] == "http://example.com"
    assert result["link_count"] == 10

def test_get_latest_metrics_not_found(mock_db, mock_repository, monkeypatch):
    monkeypatch.setattr("app.services.PageVisitRepository.get_latest_by_url", lambda db, url: None)
    result = PageVisitService.get_latest_metrics(mock_db, "http://example.com")
    assert result["url"] == "http://example.com"
    assert result["link_count"] == 0

def test_get_visit_history(mock_db, mock_repository, monkeypatch):
    mock_visits = [
        Mock(datetime_visited="2025-10-21T12:00:00"),
        Mock(datetime_visited="2025-10-21T11:00:00")
    ]
    monkeypatch.setattr("app.services.PageVisitRepository.get_all_by_url", lambda db, url: mock_visits)
    result = PageVisitService.get_visit_history(mock_db, "http://example.com")
    assert len(result) == 2
    assert result[0] == "2025-10-21T12:00:00"

def test_get_visit_history_not_found(mock_db, mock_repository, monkeypatch):
    monkeypatch.setattr("app.services.PageVisitRepository.get_all_by_url", lambda db, url: [])
    with pytest.raises(NotFoundError):
        PageVisitService.get_visit_history(mock_db, "http://example.com")