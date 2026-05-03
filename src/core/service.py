from __future__ import annotations

from dataclasses import dataclass

from src.core.models import StatusEnum
from src.core.repository import ToDoRepository
from src.core.validation import parse_due_date, parse_priority, parse_status_filter, validate_item_id, validate_title


@dataclass
class CommandResult:
    success: bool
    message: str
    item_id: int | None = None
    affected_count: int | None = None
    already_done: bool = False


class ToDoService:
    def __init__(self, repository: ToDoRepository) -> None:
        self.repository = repository

    def add_todo(self, *, title: str, due: str | None = None, priority: str | None = None) -> CommandResult:
        try:
            normalized_title = validate_title(title)
            due_date = parse_due_date(due)
            priority_value = parse_priority(priority)
        except ValueError as exc:
            return CommandResult(success=False, message=str(exc))

        item = self.repository.add_item(title=normalized_title, due_date=due_date, priority=priority_value)
        return CommandResult(success=True, message="added", item_id=item.id)

    def list_todos(self, *, status_filter: str | None = None, priority: str | None = None):
        try:
            status = parse_status_filter(status_filter)
            priority_value = parse_priority(priority)
        except ValueError as exc:
            return CommandResult(success=False, message=str(exc)), []

        items = self.repository.list_items(status=status, priority=priority_value)
        return CommandResult(success=True, message="listed", affected_count=len(items)), items

    def done_todo(self, item_id: int) -> CommandResult:
        try:
            valid_id = validate_item_id(item_id)
        except ValueError as exc:
            return CommandResult(success=False, message=str(exc))

        current = self.repository.get_item(valid_id)
        if current is None:
            return CommandResult(success=False, message="error: todo item not found")

        already_done = current.status == StatusEnum.DONE
        self.repository.mark_done(valid_id)
        return CommandResult(success=True, message="done", item_id=valid_id, already_done=already_done)

    def delete_todo(self, item_id: int) -> CommandResult:
        try:
            valid_id = validate_item_id(item_id)
        except ValueError as exc:
            return CommandResult(success=False, message=str(exc))

        deleted = self.repository.delete_item(valid_id)
        if not deleted:
            return CommandResult(success=False, message="error: todo item not found")
        return CommandResult(success=True, message="deleted", item_id=valid_id, affected_count=1)
