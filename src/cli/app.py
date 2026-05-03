from __future__ import annotations

import os
from typing import Optional

import typer

from src.cli.formatters import format_add_success, format_delete_success, format_done_success, format_list
from src.core.repository import ToDoRepository
from src.core.service import ToDoService

app = typer.Typer(help="CLI ToDo Manager")


def _get_service() -> tuple[ToDoService, ToDoRepository]:
    db_path = os.getenv("TODO_DB_PATH", "todo.db")
    repository = ToDoRepository.from_db_file(db_path)
    repository.init_db()
    return ToDoService(repository), repository


@app.command("add")
def add_command(
    title: str = typer.Argument(...),
    due: Optional[str] = typer.Option(None, "--due"),
    priority: Optional[str] = typer.Option(None, "--priority"),
) -> None:
    service, repository = _get_service()
    try:
        result = service.add_todo(title=title, due=due, priority=priority)
        if not result.success:
            typer.echo(result.message)
            raise typer.Exit(code=1)

        item = service.repository.get_item(result.item_id)
        if item is None:
            typer.echo("error: todo item not found")
            raise typer.Exit(code=1)
        typer.echo(format_add_success(item))
    finally:
        repository.close()


@app.command("list")
def list_command(
    status_filter: Optional[str] = typer.Option(None, "--filter"),
    priority: Optional[str] = typer.Option(None, "--priority"),
) -> None:
    service, repository = _get_service()
    try:
        result, items = service.list_todos(status_filter=status_filter, priority=priority)
        if not result.success:
            typer.echo(result.message)
            raise typer.Exit(code=1)
        typer.echo(format_list(items))
    finally:
        repository.close()


@app.command("done")
def done_command(item_id: int = typer.Argument(...)) -> None:
    service, repository = _get_service()
    try:
        result = service.done_todo(item_id)
        if not result.success:
            typer.echo(result.message)
            raise typer.Exit(code=1)
        typer.echo(format_done_success(item_id, already_done=result.already_done))
    finally:
        repository.close()


@app.command("delete")
def delete_command(item_id: int = typer.Argument(...)) -> None:
    service, repository = _get_service()
    try:
        result = service.delete_todo(item_id)
        if not result.success:
            typer.echo(result.message)
            raise typer.Exit(code=1)
        typer.echo(format_delete_success(item_id))
    finally:
        repository.close()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
