from __future__ import annotations

from src.core.service import ToDoService


def test_delete_todo_removes_item(repository) -> None:
    service = ToDoService(repository)
    created = service.add_todo(title="삭제 대상")

    result = service.delete_todo(created.item_id)

    assert result.success is True
    assert repository.get_item(created.item_id) is None


def test_delete_todo_returns_error_for_invalid_id(repository) -> None:
    service = ToDoService(repository)

    result = service.delete_todo(0)

    assert result.success is False
    assert result.message == "error: id must be a positive integer"


def test_delete_todo_returns_error_for_missing_id(repository) -> None:
    service = ToDoService(repository)

    result = service.delete_todo(12345)

    assert result.success is False
    assert result.message == "error: todo item not found"
