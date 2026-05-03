from __future__ import annotations


def test_cli_list_all_items(runner, cli_app) -> None:
    runner.invoke(cli_app, ["add", "문서 정리", "--priority", "high"])
    runner.invoke(cli_app, ["add", "회의 준비", "--priority", "low"])

    result = runner.invoke(cli_app, ["list"])

    assert result.exit_code == 0
    assert "문서 정리" in result.stdout
    assert "회의 준비" in result.stdout


def test_cli_list_with_filter(runner, cli_app) -> None:
    add_result = runner.invoke(cli_app, ["add", "완료할 작업", "--priority", "high"])
    created_id = int(add_result.stdout.split("id=")[1].split(",")[0])
    runner.invoke(cli_app, ["done", str(created_id)])

    result = runner.invoke(cli_app, ["list", "--filter", "done", "--priority", "high"])

    assert result.exit_code == 0
    assert "완료할 작업" in result.stdout
    assert "done" in result.stdout


def test_cli_list_rejects_invalid_filter(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["list", "--filter", "invalid"])

    assert result.exit_code == 1
    assert "error: filter must be one of done|pending" in result.stdout
