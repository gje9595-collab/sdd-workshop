from __future__ import annotations

import pytest

from src.core.service import ToDoService


def test_add_todo_with_required_title(repository) -> None:
    service = ToDoService(repository)

    result = service.add_todo(title="문서 정리")

    assert result.success is True
    assert result.item_id is not None
    items = repository.list_items()
    assert len(items) == 1
    assert items[0].title == "문서 정리"
    assert items[0].status.value == "pending"


def test_add_todo_with_optional_due_and_priority(repository) -> None:
    service = ToDoService(repository)

    result = service.add_todo(title="테스트", due="2026-05-10", priority="high")

    assert result.success is True
    assert result.item_id is not None
    item = repository.get_item(result.item_id)
    assert item is not None
    assert item.due_date.isoformat() == "2026-05-10"
    assert item.priority.value == "high"


@pytest.mark.parametrize(
    "title, expected_message",
    [
        ("", "error: title is required"),
        ("   ", "error: title is required"),
    ],
)
def test_add_todo_requires_title(repository, title: str, expected_message: str) -> None:
    service = ToDoService(repository)

    result = service.add_todo(title=title)

    assert result.success is False
    assert result.message == expected_message
