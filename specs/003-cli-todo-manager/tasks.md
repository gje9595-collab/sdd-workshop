# Tasks: CLI ToDo Manager

**Input**: Design documents from `/specs/003-cli-todo-manager/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-contract.md, quickstart.md

**Tests**: 테스트는 필수다. 각 사용자 스토리에서 실패 테스트를 먼저 작성한 뒤 구현한다.

**Organization**: 사용자 스토리별 독립 구현/독립 테스트가 가능하도록 Phase를 분리한다.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Python 3.12 + uv 기반 프로젝트 초기 구조를 준비한다.

- [X] T001 `pyproject.toml` 생성 및 Python 3.12, uv 기본 설정 추가 (`pyproject.toml`)
- [X] T002 런타임/개발 의존성 최소 목록 추가 (`typer`, `sqlalchemy`, `pytest`, `pytest-cov`) (`pyproject.toml`)
- [X] T003 [P] 소스/테스트 디렉터리 초기화 (`src/core/__init__.py`, `src/cli/__init__.py`, `src/adapters/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`)
- [X] T004 [P] CLI 실행 진입점 및 패키지 실행 설정 추가 (`src/cli/app.py`, `pyproject.toml`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 모든 사용자 스토리가 공통으로 사용하는 핵심 기반을 구축한다.

**⚠️ CRITICAL**: 이 단계 완료 전에는 사용자 스토리 구현을 시작하지 않는다.

- [X] T005 SQLite 엔진/세션/테이블 초기화 코드 구현 (`src/core/repository.py`)
- [X] T006 [P] ToDoItem 영속 모델 및 공통 enum 정의 (`src/core/models.py`)
- [X] T007 [P] 입력 검증 규칙 구현(제목, 날짜, 우선순위, ID) (`src/core/validation.py`)
- [X] T008 CLI 공통 출력 포맷 함수 골격 구현 (`src/cli/formatters.py`)
- [X] T009 테스트 공통 fixture(임시 SQLite DB, 서비스 fixture) 작성 (`tests/conftest.py`)

**Checkpoint**: Foundation complete - 사용자 스토리 작업 시작 가능

---

## Phase 3: User Story 1 - 빠른 할 일 등록 (Priority: P1) 🎯 MVP

**Goal**: 제목 필수 + 선택값(마감일/우선순위) 기반 ToDo 추가를 제공한다.

**Independent Test**: `todo add` 명령으로 제목만 입력한 생성과 선택값 포함 생성을 모두 검증한다.

### Tests for User Story 1 (REQUIRED)

- [X] T010 [P] [US1] 항목 추가 비즈니스 규칙 실패 테스트 작성 (`tests/unit/test_add_todo.py`)
- [X] T011 [P] [US1] `todo add` CLI 통합 실패 테스트 작성 (`tests/integration/test_cli_add.py`)

### Implementation for User Story 1

- [X] T012 [US1] 항목 추가 서비스 로직 구현 (`src/core/service.py`)
- [X] T013 [US1] `todo add "<title>" [--due] [--priority]` 명령 구현 (`src/cli/app.py`)
- [X] T014 [US1] add 성공/실패 메시지 포맷 구현 (`src/cli/formatters.py`)

**Checkpoint**: US1 단독 실행/테스트 통과 (MVP)

---

## Phase 4: User Story 2 - 필터 기반 목록 확인 (Priority: P2)

**Goal**: 전체 목록 조회와 상태/우선순위 필터 조회를 제공한다.

**Independent Test**: `todo list`, `todo list --filter`, `todo list --priority` 결과가 조건에 맞는지 검증한다.

### Tests for User Story 2 (REQUIRED)

- [X] T015 [P] [US2] 목록 조회/필터 비즈니스 규칙 실패 테스트 작성 (`tests/unit/test_list_todo.py`)
- [X] T016 [P] [US2] `todo list` CLI 통합 실패 테스트 작성 (`tests/integration/test_cli_list.py`)

### Implementation for User Story 2

- [X] T017 [US2] 목록 조회 및 필터 서비스 로직 구현 (`src/core/service.py`)
- [X] T018 [US2] `todo list [--filter done|pending] [--priority high|medium|low]` 명령 구현 (`src/cli/app.py`)
- [X] T019 [US2] 목록 출력 포맷 구현 (`src/cli/formatters.py`)

**Checkpoint**: US2 단독 실행/테스트 통과

---

## Phase 5: User Story 3 - 항목 완료 및 삭제 (Priority: P3)

**Goal**: ID 기준 완료 처리(`done`)와 삭제(`delete`)를 제공한다.

**Independent Test**: `todo done <id>`, `todo delete <id>`와 미존재 ID 오류를 검증한다.

### Tests for User Story 3 (REQUIRED)

- [X] T020 [P] [US3] 완료 비즈니스 규칙 실패 테스트 작성 (`tests/unit/test_done_todo.py`)
- [X] T020b [P] [US3] 삭제 비즈니스 규칙 실패 테스트 작성 (`tests/unit/test_delete_todo.py`)
- [X] T021 [P] [US3] `todo done`, `todo delete` CLI 통합 실패 테스트 작성 (`tests/integration/test_cli_done_delete.py`)

### Implementation for User Story 3

- [X] T022 [US3] 완료 처리 및 삭제 서비스 로직 구현 (`src/core/service.py`)
- [X] T023 [US3] `todo done <id>`, `todo delete <id>` 명령 구현 (`src/cli/app.py`)
- [X] T024 [US3] done/delete 성공/오류 메시지 포맷 구현 (`src/cli/formatters.py`)

**Checkpoint**: US3 단독 실행/테스트 통과

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 전체 스토리를 묶어 품질 게이트를 마무리한다.

- [X] T025 [P] 커버리지 리포트 및 누락 경로 보강 테스트 추가 (`tests/unit/test_edge_cases.py`)
- [X] T026 quickstart 실행 검증 절차와 실제 명령 예시 동기화 (`specs/003-cli-todo-manager/quickstart.md`)
- [X] T027 전체 테스트/커버리지 실행 및 결과 기준선 기록 (`pyproject.toml`, `specs/003-cli-todo-manager/quickstart.md`)
- [X] T028 [SC-002] 성능 검증: 200개 항목 seed 후 `todo list` 및 필터 조회 응답시간 2초 이내 측정 (`tests/unit/test_performance.py`)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 즉시 시작 가능
- **Phase 2 (Foundational)**: Phase 1 완료 후 시작, 모든 사용자 스토리의 선행 조건
- **Phase 3~5 (User Stories)**: Phase 2 완료 후 시작 가능
- **Phase 6 (Polish)**: 모든 선택한 사용자 스토리 완료 후 진행

### User Story Dependencies

- **US1 (P1)**: Foundational 완료 후 독립 시작 가능
- **US2 (P2)**: Foundational 완료 후 독립 시작 가능
- **US3 (P3)**: Foundational 완료 후 독립 시작 가능

### Within Each User Story

- 테스트 태스크(Txxx Tests) 먼저 작성하고 실패를 확인한다.
- 서비스 로직 구현 후 CLI 명령을 연결한다.
- 출력 포맷/오류 메시지를 마지막에 정리한다.
- 각 태스크는 1커밋 단위로 완료한다.

### Story Completion Order

- 권장 순서: **US1 → US2 → US3**
- 팀 여건에 따라 Foundational 완료 후 병렬 개발 가능

---

## Parallel Execution Examples

### Setup Phase

```bash
# 병렬 가능 예시
T003: 소스/테스트 디렉터리 초기화
T004: CLI 실행 진입점/패키지 실행 설정
```

### User Story 1

```bash
# 테스트 선행 병렬 작성
T010: tests/unit/test_add_todo.py
T011: tests/integration/test_cli_add.py
```

### User Story 2

```bash
# 테스트 선행 병렬 작성
T015: tests/unit/test_list_todo.py
T016: tests/integration/test_cli_list.py
```

### User Story 3

```bash
# 테스트 선행 병렬 작성
T020: tests/unit/test_done_todo.py
T020b: tests/unit/test_delete_todo.py
T021: tests/integration/test_cli_done_delete.py
```

---

## Implementation Strategy

### MVP First (US1)

1. Phase 1 완료
2. Phase 2 완료
3. US1 테스트 선행 후 구현
4. US1 독립 검증 후 데모

### Incremental Delivery

1. US1 추가 후 배포 가능한 최소 가치 확보
2. US2 추가로 조회/필터 완성
3. US3 추가로 라이프사이클(완료/삭제) 완성
4. 마지막에 커버리지/문서 동기화로 마감

### Commit Strategy (One Task = One Commit)

- 각 T-ID 완료 시점에 단일 커밋 수행
- 권장 메시지 예: `feat(us1): implement T012 add todo service`
- [P] 태스크도 개별 커밋 유지, 충돌 가능 파일은 직렬 처리
