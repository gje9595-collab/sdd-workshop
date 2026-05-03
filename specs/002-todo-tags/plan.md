# Implementation Plan: ToDo 태그 기능 통합

**Branch**: `004-prepare-specify-branch` | **Date**: 2026-05-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-tags/spec.md`

## Summary

기존 CLI ToDo 앱에 태그 기능을 추가한다. 핵심은 기존 계층(`todo_lib`의 도메인 규칙, `cli`의 입출력 역할)을 유지하면서 다음 변경을 통합하는 것이다.
1. 기존 Todo 모델에 `tags` 필드(JSON 컬럼) 추가
2. 기존 `service.py`에 태그 필터링 로직 추가
3. 기존 CLI 명령에 `--tag` 옵션 추가
4. 기존 테스트 전량 회귀 통과

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: Typer, SQLAlchemy, pytest, pytest-cov  
**Storage**: SQLite 로컬 파일(`todo.db`), tags는 JSON 컬럼 사용  
**Testing**: pytest (unit + integration + regression)  
**Target Platform**: Windows PowerShell/CMD, macOS, Linux
**Project Type**: CLI application (single project)  
**Performance Goals**: 기존 add/list/done/delete 응답성과 동급 유지, 태그 필터 포함 list도 체감상 즉시 응답  
**Constraints**: 기존 기술 스택 유지, 기존 명령 UX/에러 코드 규약 유지, 신규 의존성 추가 금지  
**Scale/Scope**: 단일 사용자 로컬 데이터(수백~수천 항목), 태그 CRUD 전용 명령은 범위 밖

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Gate 1: 비즈니스 로직과 입출력 계층 분리(`todo_lib` vs `cli`)가 설계에 반영됨
- [x] Gate 2: 사용자 스토리별 테스트 선행(실패 테스트 먼저) 계획이 존재함
- [x] Gate 3: 신규 외부 의존성 도입 없음 (검토 완료)
- [x] Gate 4: 별도 태그 테이블 대신 JSON 컬럼 채택으로 단순 설계 유지
- [x] Gate 5: 범위를 CLI ToDo 도구로 제한, REST API/GUI 제외

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-tags/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
todo_lib/
├── models.py            # ToDoItem에 tags 필드 추가
├── validation.py        # tags 검증 함수 추가
├── repository.py        # tags 저장/조회 필터 추가
└── service.py           # add/list에 tags 처리 통합

cli/
└── main.py              # add/list에 --tag 옵션 추가

tests/
├── unit/
│   ├── test_tags_validation.py
│   ├── test_service_add_tags.py
│   └── test_service_list_tags.py
└── integration/
    └── test_cli_tags.py
```

**Structure Decision**: 기존 코드베이스의 계층 경계를 유지하고, 태그 기능은 기존 모델/서비스/CLI 흐름에 최소 변경으로 삽입한다. 기존 명령(`done`, `delete`)과 기존 테스트의 동작은 변경하지 않는다.

## Phase 0: Research Plan

연구 결론은 [research.md](./research.md)에 기록한다.
1. JSON 컬럼 저장 전략과 기존 레코드 호환성
2. Typer의 반복 옵션(`--tag`) 입력 패턴
3. 태그 필터와 기존 필터(`--filter`, `--priority`) 교집합 규칙

## Phase 1: Design & Contracts

1. 데이터 모델 설계
- `ToDoItem.tags`를 JSON 컬럼으로 추가
- 기존 항목(`tags` 부재/NULL)의 읽기 호환 규칙 정의

2. 서비스 설계
- `add_todo(..., tags)` 시 tags 검증 및 저장
- `list_todos(..., tag)` 시 기존 필터와 교집합 적용

3. CLI 계약 설계
- `todo add ... --tag <value>` 반복 입력 허용
- `todo list ... --tag <value>` 단일 필터 지원

4. 테스트 설계
- 태그 기능 신규 테스트 추가
- 기존 테스트 전량 회귀 실행

## Post-Design Constitution Check

- [x] 레이어 분리: 도메인 로직은 `todo_lib`, 입출력은 `cli`에 유지
- [x] 테스트 우선: 태그 테스트를 실패 상태로 먼저 작성
- [x] 최소 의존성: 기존 라이브러리만 사용
- [x] 단순함 우선: JSON 컬럼 기반 최소 확장
- [x] CLI 범위 준수: CLI 외 인터페이스 추가 없음

## Phase 2: Task Planning Approach

`/speckit.tasks`에서 아래 순서로 작업 분해:
1. 기존 테스트 전량 실행으로 회귀 baseline 확정
2. 태그 기능 테스트 작성(Red)
3. 모델/검증/저장소/서비스/CLI 구현(Green)
4. 기존 + 신규 전체 테스트 재실행
5. 커버리지 및 quickstart 검증

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 없음 | N/A | N/A |
