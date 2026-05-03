from __future__ import annotations


def test_cli_add_with_title(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["add", "문서 정리"])

    assert result.exit_code == 0
    assert "added:" in result.stdout
    assert "status=pending" in result.stdout


def test_cli_add_with_optional_values(runner, cli_app) -> None:
    result = runner.invoke(
        cli_app,
        ["add", "회의 준비", "--due", "2026-05-10", "--priority", "high"],
    )

    assert result.exit_code == 0
    assert "added:" in result.stdout


def test_cli_add_requires_title(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["add", "   "])

    assert result.exit_code == 1
    assert "error: title is required" in result.stdout
