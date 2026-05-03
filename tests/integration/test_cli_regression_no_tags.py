"""T021: 태그 미사용 회귀 테스트"""

from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()


def _make_service(tmp_path, monkeypatch):
    import cli.main as main_mod
    from todo_lib.service import ToDoService

    svc = ToDoService(db_path=str(tmp_path / "todo.db"))
    monkeypatch.setattr(main_mod, "_get_service", lambda: svc)
    return svc


def test_add_list_done_delete_without_tags_still_works(tmp_path, monkeypatch):
    svc = _make_service(tmp_path, monkeypatch)

    add_result = runner.invoke(app, ["add", "기존 흐름"])
    assert add_result.exit_code == 0

    items = svc.list_todos()
    target_id = items[0].id

    list_result = runner.invoke(app, ["list"])
    assert list_result.exit_code == 0
    assert "기존 흐름" in list_result.output

    done_result = runner.invoke(app, ["done", str(target_id)])
    assert done_result.exit_code == 0

    delete_result = runner.invoke(app, ["delete", str(target_id)])
    assert delete_result.exit_code == 0
