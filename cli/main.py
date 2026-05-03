"""CLI entry point using Typer framework."""

from pathlib import Path
from typing import Optional

import typer

from cli import formatters
from todo_lib.errors import AlreadyDoneError, DatabaseError, ItemNotFoundError, ValidationError
from todo_lib.service import ToDoService

# CLI 앱 인스턴스 생성
app = typer.Typer(
    help="CLI 기반 ToDo 관리 앱",
    no_args_is_help=True,
    rich_markup_mode=None,
)

_DEFAULT_DB_PATH = str(Path.cwd() / "todo.db")


def _get_service() -> ToDoService:
    return ToDoService(db_path=_DEFAULT_DB_PATH)


@app.command()
def add(
    title: str = typer.Argument(..., help="항목 제목 (필수)"),
    due: Optional[str] = typer.Option(None, "--due", help="마감일 (YYYY-MM-DD 형식, 선택)"),
    priority: Optional[str] = typer.Option(None, "--priority", help="우선순위 (high|medium|low, 선택)"),
    tag: list[str] = typer.Option(None, "--tag", help="태그(반복 가능)"),
):
    """새로운 ToDo 항목을 추가합니다."""
    try:
        svc = _get_service()
        item, past_warning = svc.add_todo(title, due=due, priority=priority, tags=tag)
        if past_warning:
            formatters.print_add_warning_past_date()
        formatters.print_add_success(item)
    except ValidationError as exc:
        formatters.print_error(str(exc))
        raise typer.Exit(code=1)
    except DatabaseError:
        formatters.print_db_error()
        raise typer.Exit(code=2)


@app.command(name="list")
def list_todos(
    filter: Optional[str] = typer.Option(None, "--filter", help="필터: done|pending"),
    priority: Optional[str] = typer.Option(None, "--priority", help="우선순위 필터: high|medium|low"),
    tag: Optional[str] = typer.Option(None, "--tag", help="태그 필터"),
):
    """저장된 ToDo 항목 목록을 조회합니다."""
    try:
        svc = _get_service()
        items = svc.list_todos(filter_status=filter, priority=priority, tag=tag)
        formatters.print_list(items)
    except ValidationError as exc:
        formatters.print_error(str(exc))
        raise typer.Exit(code=1)
    except DatabaseError:
        formatters.print_db_error()
        raise typer.Exit(code=2)


@app.command()
def done(
    item_id: str = typer.Argument(..., help="완료할 항목의 ID"),
):
    """항목을 완료 상태로 변경합니다."""
    try:
        int_id = int(item_id)
    except ValueError:
        formatters.print_error("ID는 숫자여야 합니다")
        raise typer.Exit(code=1)

    try:
        svc = _get_service()
        svc.mark_done(int_id)
        formatters.print_done_success(int_id)
    except ItemNotFoundError as exc:
        formatters.print_not_found(exc.item_id)
        raise typer.Exit(code=1)
    except AlreadyDoneError as exc:
        formatters.print_already_done(exc.item_id)
        raise typer.Exit(code=1)
    except DatabaseError:
        formatters.print_db_error()
        raise typer.Exit(code=2)


@app.command()
def delete(
    item_id: str = typer.Argument(..., help="삭제할 항목의 ID"),
):
    """항목을 영구 삭제합니다."""
    try:
        int_id = int(item_id)
    except ValueError:
        formatters.print_error("ID는 숫자여야 합니다")
        raise typer.Exit(code=1)

    try:
        svc = _get_service()
        svc.delete_todo(int_id)
        formatters.print_delete_success(int_id)
    except ItemNotFoundError as exc:
        formatters.print_not_found(exc.item_id)
        raise typer.Exit(code=1)
    except DatabaseError:
        formatters.print_db_error()
        raise typer.Exit(code=2)


def main():
    """CLI 애플리케이션 진입점"""
    app()


if __name__ == "__main__":
    main()
