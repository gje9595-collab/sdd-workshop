"""
CLI entry point using Typer framework

Commands:
  todo add <title> [--due YYYY-MM-DD] [--priority high|medium|low]
  todo list [--filter done|pending] [--priority high|medium|low]
  todo done <id>
  todo delete <id>

Run with --help for more information.
"""

import typer
from typing import Optional

# CLI 앱 인스턴스 생성
app = typer.Typer(
    help="CLI 기반 ToDo 관리 앱",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def add(
    title: str = typer.Argument(..., help="항목 제목 (필수)"),
    due: Optional[str] = typer.Option(None, "--due", help="마감일 (YYYY-MM-DD 형식, 선택)"),
    priority: Optional[str] = typer.Option(None, "--priority", help="우선순위 (high|medium|low, 선택)"),
):
    """새로운 ToDo 항목을 추가합니다."""
    # T016-T019에서 구현
    pass


@app.command()
def list(
    filter: Optional[str] = typer.Option(None, "--filter", help="필터: done|pending"),
    priority: Optional[str] = typer.Option(None, "--priority", help="우선순위 필터: high|medium|low"),
):
    """저장된 ToDo 항목 목록을 조회합니다."""
    # T022-T024에서 구현
    pass


@app.command()
def done(
    item_id: int = typer.Argument(..., help="완료할 항목의 ID"),
):
    """항목을 완료 상태로 변경합니다."""
    # T027-T029에서 구현
    pass


@app.command()
def delete(
    item_id: int = typer.Argument(..., help="삭제할 항목의 ID"),
):
    """항목을 영구 삭제합니다."""
    # T032-T034에서 구현
    pass


def main():
    """CLI 애플리케이션 진입점"""
    app()


if __name__ == "__main__":
    main()
