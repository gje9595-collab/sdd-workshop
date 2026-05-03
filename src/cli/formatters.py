from __future__ import annotations

from src.core.models import ToDoItem


def format_add_success(item: ToDoItem) -> str:
    return f"added: id={item.id}, status={item.status.value}"


def format_list(items: list[ToDoItem]) -> str:
    if not items:
        return "no items"

    lines: list[str] = []
    for item in items:
        due = item.due_date.isoformat() if item.due_date is not None else "-"
        priority = item.priority.value if item.priority is not None else "-"
        lines.append(f"{item.id} | {item.title} | {due} | {priority} | {item.status.value}")
    return "\n".join(lines)


def format_done_success(item_id: int, already_done: bool = False) -> str:
    if already_done:
        return f"already done: id={item_id}"
    return f"done: id={item_id}"


def format_delete_success(item_id: int) -> str:
    return f"deleted: id={item_id}"
