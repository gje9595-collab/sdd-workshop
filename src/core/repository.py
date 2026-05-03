from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from src.core.models import Base, PriorityEnum, StatusEnum, ToDoItem


class ToDoRepository:
    def __init__(self, db_url: str = "sqlite:///todo.db") -> None:
        self.engine = create_engine(db_url, future=True)
        self._session_factory = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, future=True)

    @classmethod
    def from_db_file(cls, db_file: str | Path) -> "ToDoRepository":
        db_path = Path(db_file)
        return cls(f"sqlite:///{db_path.as_posix()}")

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def session(self) -> Session:
        return self._session_factory()

    def add_item(self, *, title: str, due_date=None, priority: PriorityEnum | None = None) -> ToDoItem:
        with self.session() as session:
            item = ToDoItem(title=title, due_date=due_date, priority=priority, status=StatusEnum.PENDING)
            session.add(item)
            session.commit()
            session.refresh(item)
            return item

    def list_items(self, *, status: StatusEnum | None = None, priority: PriorityEnum | None = None) -> list[ToDoItem]:
        with self.session() as session:
            stmt = select(ToDoItem).order_by(ToDoItem.id.asc())
            if status is not None:
                stmt = stmt.where(ToDoItem.status == status)
            if priority is not None:
                stmt = stmt.where(ToDoItem.priority == priority)
            return list(session.scalars(stmt).all())

    def get_item(self, item_id: int) -> ToDoItem | None:
        with self.session() as session:
            return session.get(ToDoItem, item_id)

    def mark_done(self, item_id: int) -> ToDoItem | None:
        with self.session() as session:
            item = session.get(ToDoItem, item_id)
            if item is None:
                return None
            item.status = StatusEnum.DONE
            session.commit()
            session.refresh(item)
            return item

    def delete_item(self, item_id: int) -> bool:
        with self.session() as session:
            item = session.get(ToDoItem, item_id)
            if item is None:
                return False
            session.delete(item)
            session.commit()
            return True

    def close(self) -> None:
        self.engine.dispose()
