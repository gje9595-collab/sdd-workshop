"""
CLI 출력 포맷팅 헬퍼
"""

import typer
from todo_lib.models import ToDoItem


def print_add_success(item: ToDoItem) -> None:
    typer.echo(f"항목이 추가되었습니다 (ID: {item.id})")


def print_add_warning_past_date() -> None:
    typer.echo("경고: 마감일이 오늘 이전 날짜입니다", err=True)


def print_list(items: list[ToDoItem]) -> None:
    if not items:
        typer.echo("등록된 항목이 없습니다")
        return

    header = f"{'ID':<6} {'제목':<24} {'마감일':<12} {'우선순위':<10} {'태그':<18} {'완료'}"
    typer.echo(header)
    typer.echo("-" * len(header))

    for item in items:
        due = str(item.due_date) if item.due_date else "-"
        priority = item.priority if item.priority else "-"
        tags = ",".join(item.tags or []) if item.tags else "-"
        done = "O" if item.is_done else "X"
        typer.echo(f"{item.id:<6} {item.title:<24} {due:<12} {priority:<10} {tags:<18} {done}")


def print_done_success(item_id: int) -> None:
    typer.echo(f"항목 {item_id}가 완료 처리되었습니다")


def print_already_done(item_id: int) -> None:
    typer.echo(f"항목 {item_id}는 이미 완료된 항목입니다")


def print_delete_success(item_id: int) -> None:
    typer.echo(f"항목 {item_id}가 삭제되었습니다")


def print_error(message: str) -> None:
    typer.echo(message, err=True)


def print_not_found(item_id: int) -> None:
    typer.echo(f"항목 {item_id}를 찾을 수 없습니다", err=True)


def print_db_error() -> None:
    typer.echo("데이터 파일이 손상되었습니다. 파일을 백업하거나 삭제 후 재시도하세요", err=True)
