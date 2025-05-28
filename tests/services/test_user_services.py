import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import uuid
from unittest.mock import MagicMock
from app.services import user_services

# -------- Mock Fixtures --------

@pytest.fixture
def mock_user_doc_exists():
    user_data = {
        "difficulty_level": 1,
        "previous_sessions": [],
        "name": "John Tester",
    }
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = user_data
    return mock_doc

@pytest.fixture
def mock_user_doc_not_exists():
    mock_doc = MagicMock()
    mock_doc.exists = False
    return mock_doc

@pytest.fixture(autouse=True)
def mock_firestore(monkeypatch, mock_user_doc_exists):
    mock_db = MagicMock()
    mock_collection = mock_db.collection.return_value
    mock_document = mock_collection.document.return_value
    mock_document.get.return_value = mock_user_doc_exists
    monkeypatch.setattr("app.services.user_services.db", mock_db)
    return mock_db

# -------- Tests for find_user_by_id_demo --------

def test_find_user_by_id_demo_found():
    result = user_services.find_user_by_id_demo(2)
    assert result["name"] == "Jane Smith"

def test_find_user_by_id_demo_not_found():
    result = user_services.find_user_by_id_demo(99)
    assert result is None

# -------- Tests for find_user_by_id --------

def test_find_user_by_id_found(mock_firestore, mock_user_doc_exists):
    result = user_services.find_user_by_id("123")
    assert result["difficulty_level"] == 1
    assert result["name"] == "John Tester"

def test_find_user_by_id_not_found(monkeypatch, mock_user_doc_not_exists):
    mock_db = MagicMock()
    mock_collection = mock_db.collection.return_value
    mock_document = mock_collection.document.return_value
    mock_document.get.return_value = mock_user_doc_not_exists
    monkeypatch.setattr("app.services.user_services.db", mock_db)

    result = user_services.find_user_by_id("999")
    assert result is None

# -------- Tests for update_difficulty_level --------

def test_update_difficulty_level_success(mock_firestore, mock_user_doc_exists):
    user_id = "123"
    result = user_services.update_difficulty_level(
        user_id=user_id,
        new_difficulty_level=2,
        recent_avg_score=0.85,
        recent_avg_res_time=12.3,
        recent_action_taken="increase"
    )
    assert result["success"] is True
    assert "updated successfully" in result["message"]

def test_update_difficulty_level_user_not_found(monkeypatch, mock_user_doc_not_exists):
    mock_db = MagicMock()
    mock_collection = mock_db.collection.return_value
    mock_document = mock_collection.document.return_value
    mock_document.get.return_value = mock_user_doc_not_exists
    monkeypatch.setattr("app.services.user_services.db", mock_db)

    result = user_services.update_difficulty_level(
        user_id="999",
        new_difficulty_level=0,
        recent_avg_score=0.25,
        recent_avg_res_time=85.0,
        recent_action_taken="decrease"
    )
    assert result["success"] is False
    assert result["message"] == "User not found."
