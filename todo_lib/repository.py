"""
Repository CRUD 연산
"""

from datetime import datetime
from sqlalchemy.orm import Session
from todo_lib.models import ToDoItem


def add_item(
    session: Session,
    title: str,
    due_date=None,
    priority=None,
    tags: list[str] | None = None,
) -> ToDoItem:
    item = ToDoItem(
        title=title,
        due_date=due_date,
        priority=priority,
        tags=tags if tags else None,
        is_done=False,
        created_at=datetime.now(),
    )
    session.add(item)
    session.flush()
    return item


def list_items(
    session: Session,
    filter_status: str | None = None,
    priority: str | None = None,
    tag: str | None = None,
) -> list[ToDoItem]:
    query = session.query(ToDoItem)

    if filter_status == "done":
        query = query.filter(ToDoItem.is_done.is_(True))
    elif filter_status == "pending":
        query = query.filter(ToDoItem.is_done.is_(False))

    if priority is not None:
        query = query.filter(ToDoItem.priority == priority)

    items = query.order_by(ToDoItem.id.asc()).all()

    if tag is None:
        return items

    return [item for item in items if tag in (item.tags or [])]


def get_item(session: Session, item_id: int) -> ToDoItem | None:
    return session.get(ToDoItem, item_id)


def mark_done(session: Session, item: ToDoItem) -> ToDoItem:
    item.is_done = True
    item.completed_at = datetime.now()
    session.flush()
    return item


def delete_item(session: Session, item: ToDoItem) -> None:
    session.delete(item)
    session.flush()
