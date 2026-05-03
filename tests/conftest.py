"""
Pytest fixtures for isolated testing
"""

import tempfile
from pathlib import Path
import pytest
from todo_lib.service import ToDoService


@pytest.fixture
def temp_db():
    """임시 SQLite 데이터베이스 경로를 제공하는 fixture"""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        db_path = Path(tmpdir) / "test_todo.db"
        yield str(db_path)


@pytest.fixture
def service(temp_db):
    """임시 DB로 초기화된 ToDoService를 제공하는 fixture"""
    svc = ToDoService(db_path=temp_db)
    yield svc
    svc.dispose()
