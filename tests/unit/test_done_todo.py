from __future__ import annotations

from src.core.service import ToDoService


def test_done_todo_marks_item_as_done(repository) -> None:
    service = ToDoService(repository)
    created = service.add_todo(title="완료 대상")

    result = service.done_todo(created.item_id)

    assert result.success is True
    item = repository.get_item(created.item_id)
    assert item is not None
    assert item.status.value == "done"


def test_done_todo_returns_error_for_invalid_id(repository) -> None:
    service = ToDoService(repository)

    result = service.done_todo(-1)

    assert result.success is False
    assert result.message == "error: id must be a positive integer"


def test_done_todo_returns_error_for_missing_id(repository) -> None:
    service = ToDoService(repository)

    result = service.done_todo(999)

    assert result.success is False
    assert result.message == "error: todo item not found"
