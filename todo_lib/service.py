"""
비즈니스 로직 서비스
"""

from datetime import date as date_type
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from todo_lib import repository, validation
from todo_lib.errors import AlreadyDoneError, DatabaseError, ItemNotFoundError, ValidationError
from todo_lib.models import Base, ToDoItem


class ToDoService:
    """ToDo CRUD 서비스"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        db_url = f"sqlite:///{db_path}"

        try:
            self._engine = create_engine(
                db_url,
                connect_args={"timeout": 5.0},
                echo=False,
            )
            self._SessionFactory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            )
            Base.metadata.create_all(bind=self._engine)
        except SQLAlchemyError as exc:
            raise DatabaseError("데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요") from exc

    def _get_session(self) -> Session:
        return self._SessionFactory()

    def dispose(self) -> None:
        self._engine.dispose()

    def add_todo(
        self,
        title: str,
        due: str | None = None,
        priority: str | None = None,
        tags: list[str] | None = None,
    ) -> tuple[ToDoItem, bool]:
        clean_title = validation.validate_title(title)

        parsed_due: date_type | None = None
        past_warning = False
        if due is not None:
            parsed_due = validation.validate_due_date(due)
            if validation.is_past_date(parsed_due):
                past_warning = True

        clean_priority: str | None = None
        if priority is not None:
            clean_priority = validation.validate_priority(priority)

        clean_tags = validation.validate_tags(tags)

        session = self._get_session()
        try:
            item = repository.add_item(
                session,
                title=clean_title,
                due_date=parsed_due,
                priority=clean_priority,
                tags=clean_tags,
            )
            session.commit()
            session.refresh(item)
            session.expunge(item)
            return item, past_warning
        except SQLAlchemyError as exc:
            session.rollback()
            raise DatabaseError("데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요") from exc
        finally:
            session.close()

    def list_todos(
        self,
        filter_status: str | None = None,
        priority: str | None = None,
        tag: str | None = None,
    ) -> list[ToDoItem]:
        if filter_status is not None and filter_status not in {"done", "pending"}:
            raise ValidationError("필터는 done 또는 pending 이어야 합니다")

        if priority is not None:
            validation.validate_priority(priority)

        tag_filter = None
        if tag is not None:
            validated_tags = validation.validate_tags([tag])
            tag_filter = validated_tags[0] if validated_tags else None

        session = self._get_session()
        try:
            items = repository.list_items(
                session,
                filter_status=filter_status,
                priority=priority,
                tag=tag_filter,
            )
            result: list[ToDoItem] = []
            for item in items:
                session.expunge(item)
                result.append(item)
            return result
        except SQLAlchemyError as exc:
            session.rollback()
            raise DatabaseError("데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요") from exc
        finally:
            session.close()

    def mark_done(self, item_id: int) -> ToDoItem:
        session = self._get_session()
        try:
            item = repository.get_item(session, item_id)
            if item is None:
                raise ItemNotFoundError(item_id)
            if item.is_done:
                raise AlreadyDoneError(item_id)

            repository.mark_done(session, item)
            session.commit()
            session.refresh(item)
            session.expunge(item)
            return item
        except (ItemNotFoundError, AlreadyDoneError):
            session.rollback()
            raise
        except SQLAlchemyError as exc:
            session.rollback()
            raise DatabaseError("데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요") from exc
        finally:
            session.close()

    def delete_todo(self, item_id: int) -> None:
        session = self._get_session()
        try:
            item = repository.get_item(session, item_id)
            if item is None:
                raise ItemNotFoundError(item_id)

            repository.delete_item(session, item)
            session.commit()
        except ItemNotFoundError:
            session.rollback()
            raise
        except SQLAlchemyError as exc:
            session.rollback()
            raise DatabaseError("데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요") from exc
        finally:
            session.close()
