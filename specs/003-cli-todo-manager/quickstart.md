# Quickstart: CLI ToDo Manager

## 1) 환경 준비
```powershell
uv python install 3.12
uv venv
. .venv/Scripts/Activate.ps1
```

## 2) 의존성 설치
```powershell
uv add typer sqlalchemy
uv add --dev pytest pytest-cov
```

## 3) 테스트 우선 개발 흐름
1. 사용자 스토리별 실패 테스트를 먼저 작성한다.
2. 테스트를 실행해 실패를 확인한다.
3. 최소 구현으로 테스트를 통과시킨다.
4. 리팩터링 후 전체 테스트를 다시 실행한다.

## 4) 테스트 실행
```powershell
uv run pytest
uv run pytest --cov=todo_lib --cov=cli --cov-report=term-missing
```

## 5) CLI 실행 예시
```powershell
uv run python -m cli.app add "문서 정리" --due 2026-05-10 --priority high
uv run python -m cli.app list --filter pending
uv run python -m cli.app done 1
uv run python -m cli.app delete 1
```

## 6) 완료 조건
- add/list/done/delete 명령이 계약 문서와 동일하게 동작한다.
- 테스트가 모두 통과한다.
- 커버리지 리포트에서 핵심 비즈니스 경로가 누락되지 않는다.
