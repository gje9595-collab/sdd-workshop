from __future__ import annotations


def test_cli_done_and_delete(runner, cli_app) -> None:
    add_result = runner.invoke(cli_app, ["add", "완료 후 삭제"])
    created_id = int(add_result.stdout.split("id=")[1].split(",")[0])

    done_result = runner.invoke(cli_app, ["done", str(created_id)])
    delete_result = runner.invoke(cli_app, ["delete", str(created_id)])

    assert done_result.exit_code == 0
    assert f"done: id={created_id}" in done_result.stdout
    assert delete_result.exit_code == 0
    assert f"deleted: id={created_id}" in delete_result.stdout


def test_cli_done_rejects_missing_id(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["done", "999"])

    assert result.exit_code == 1
    assert "error: todo item not found" in result.stdout


def test_cli_delete_rejects_missing_id(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["delete", "999"])

    assert result.exit_code == 1
    assert "error: todo item not found" in result.stdout
