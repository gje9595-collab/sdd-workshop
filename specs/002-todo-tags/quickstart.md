# Quickstart: ToDo 태그 기능 통합

## 1) 테스트 baseline 확인

```powershell
uv run pytest
```

기대 결과: 기존 테스트 전부 통과

## 2) 태그 기능 구현 후 전체 검증

```powershell
uv run pytest
```

기대 결과: 기존 + 신규 태그 테스트 모두 통과

## 2-1) 커버리지 리포트 확인

```powershell
uv run pytest --cov=todo_lib --cov=cli --cov-report=term-missing
```

기대 결과: 태그 관련 변경 경로(add/list/validation/service)가 리포트에 포함된다.

## 3) 수동 CLI 확인

```powershell
todo add "회의 준비" --tag 업무 --tag 중요
todo add "운동" --tag 건강
todo list --tag 업무
todo list --filter pending --priority high --tag 중요
```

기대 결과:
- 태그 포함 항목이 정상 저장
- `--tag` 필터 결과 정확
- 기존 옵션과 결합 시 교집합 적용
- 기존 명령(done/delete) 동작 변화 없음
