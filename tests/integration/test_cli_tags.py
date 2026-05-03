"""T003/T010/T016: CLI 태그 통합 테스트"""

from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()


def _make_service(tmp_path, monkeypatch):
    import cli.main as main_mod
    from todo_lib.service import ToDoService

    svc = ToDoService(db_path=str(tmp_path / "todo.db"))
    monkeypatch.setattr(main_mod, "_get_service", lambda: svc)
    return svc


def test_cli_add_with_tags(tmp_path, monkeypatch):
    _make_service(tmp_path, monkeypatch)
    result = runner.invoke(app, ["add", "회의 준비", "--tag", "업무", "--tag", "중요"])
    assert result.exit_code == 0
    assert "항목이 추가되었습니다" in result.output


def test_cli_add_invalid_tag_fails(tmp_path, monkeypatch):
    _make_service(tmp_path, monkeypatch)
    result = runner.invoke(app, ["add", "회의 준비", "--tag", "bad tag"])
    assert result.exit_code == 1


def test_cli_list_with_tag_filter(tmp_path, monkeypatch):
    svc = _make_service(tmp_path, monkeypatch)
    svc.add_todo("업무 항목", tags=["업무"])
    svc.add_todo("개인 항목", tags=["개인"])

    result = runner.invoke(app, ["list", "--tag", "업무"])
    assert result.exit_code == 0
    assert "업무 항목" in result.output
    assert "개인 항목" not in result.output


def test_cli_list_with_intersection_filters(tmp_path, monkeypatch):
    svc = _make_service(tmp_path, monkeypatch)
    svc.add_todo("high 업무", priority="high", tags=["업무"])
    svc.add_todo("high 개인", priority="high", tags=["개인"])

    result = runner.invoke(app, ["list", "--priority", "high", "--tag", "업무"])
    assert result.exit_code == 0
    assert "high 업무" in result.output
    assert "high 개인" not in result.output
