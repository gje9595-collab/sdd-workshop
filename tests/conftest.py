from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from src.cli.app import app
from src.core.repository import ToDoRepository


@pytest.fixture()
def temp_db_path(tmp_path: Path) -> Path:
    return tmp_path / "test.db"


@pytest.fixture()
def repository(temp_db_path: Path) -> ToDoRepository:
    repo = ToDoRepository.from_db_file(temp_db_path)
    repo.init_db()
    try:
        yield repo
    finally:
        repo.close()


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(autouse=True)
def set_test_db(monkeypatch: pytest.MonkeyPatch, temp_db_path: Path) -> None:
    monkeypatch.setenv("TODO_DB_PATH", str(temp_db_path))


@pytest.fixture()
def cli_app():
    return app
