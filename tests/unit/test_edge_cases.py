from __future__ import annotations

from src.cli.formatters import format_list
from src.core.service import ToDoService


def test_empty_list_returns_readable_message(repository) -> None:
    service = ToDoService(repository)

    result, items = service.list_todos()

    assert result.success is True
    assert items == []
    assert format_list(items) == "no items"


def test_duplicate_titles_are_managed_by_id(repository) -> None:
    service = ToDoService(repository)
    first = service.add_todo(title="중복")
    second = service.add_todo(title="중복")

    service.done_todo(first.item_id)

    first_item = repository.get_item(first.item_id)
    second_item = repository.get_item(second.item_id)
    assert first_item is not None and first_item.status.value == "done"
    assert second_item is not None and second_item.status.value == "pending"


def test_invalid_due_or_priority_is_rejected(repository) -> None:
    service = ToDoService(repository)

    invalid_due = service.add_todo(title="테스트", due="2026/05/10")
    invalid_priority = service.add_todo(title="테스트", priority="urgent")

    assert invalid_due.success is False
    assert invalid_due.message == "error: due must be YYYY-MM-DD"
    assert invalid_priority.success is False
    assert invalid_priority.message == "error: priority must be one of high|medium|low"
