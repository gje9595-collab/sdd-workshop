from __future__ import annotations

from src.core.service import ToDoService


def test_list_todos_returns_all_items(repository) -> None:
    service = ToDoService(repository)
    service.add_todo(title="a", priority="high")
    service.add_todo(title="b", priority="low")

    result, items = service.list_todos()

    assert result.success is True
    assert len(items) == 2


def test_list_todos_filters_by_status_and_priority(repository) -> None:
    service = ToDoService(repository)
    first = service.add_todo(title="a", priority="high")
    service.add_todo(title="b", priority="low")
    service.done_todo(first.item_id)

    result, items = service.list_todos(status_filter="done", priority="high")

    assert result.success is True
    assert len(items) == 1
    assert items[0].status.value == "done"
    assert items[0].priority.value == "high"


def test_list_todos_rejects_invalid_filter(repository) -> None:
    service = ToDoService(repository)

    result, items = service.list_todos(status_filter="invalid")

    assert result.success is False
    assert result.message == "error: filter must be one of done|pending"
    assert items == []
