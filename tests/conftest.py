"""
Pytest fixtures for isolated testing
"""

import tempfile
import os
from pathlib import Path
import pytest


@pytest.fixture
def temp_db():
    """임시 SQLite 데이터베이스 경로를 제공하는 fixture"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_todo.db"
        yield str(db_path)


@pytest.fixture
def service_with_temp_db(temp_db):
    """임시 DB로 초기화된 ToDoService를 제공하는 fixture"""
    # Phase 2에서 구현될 service.ToDoService를 사용
    # 현재는 placeholder - 나중에 실제 service import로 변경
    from unittest.mock import MagicMock
    
    service = MagicMock()
    service.db_path = temp_db
    return service
