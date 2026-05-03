# Tasks: CLI 기반 ToDo 관리 앱

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: 테스트는 필수다. 각 사용자 스토리의 구현 작업 전에 실패하는 테스트 작업을 반드시 포함한다.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- 비즈니스 로직: `todo_lib/` (models, repository, service, validation, db, errors)
- CLI 레이어: `cli/` (main entry point, output formatting)
- 테스트: `tests/unit/`, `tests/integration/`
- 설계 문서: `specs/001-cli-todo-app/`
- REST API/GUI/Web 관련 경로는 사용하지 않는다.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 프로젝트 초기화와 공통 개발 환경 준비

- [ ] T001 pyproject.toml에서 uv 프로젝트 메타데이터 및 의존성 그룹 정의 (Typer, SQLAlchemy, pytest, pytest-cov)
- [ ] T002 todo_lib/__init__.py와 cli/__init__.py에 패키지 마커 추가
- [ ] T003 [P] cli/main.py에 Typer 앱 스캐폴드 작성
- [ ] T004 [P] tests/unit/__init__.py와 tests/integration/__init__.py에 테스트 마커 추가
- [ ] T005 pyproject.toml에서 pytest 및 커버리지 기본값 설정
- [ ] T006 [P] tests/conftest.py에 임시 SQLite 경로 pytest fixture 추가

---

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 모든 user story에 공통으로 필요한 핵심 기반 구현

**⚠️ CRITICAL**: 이 단계가 완료되기 전에는 user story 작업이 시작될 수 없다.

- [ ] T007 todo_lib/db.py에서 SQLAlchemy engine/session factory 및 busy-timeout 설정 구현
- [ ] T008 [P] todo_lib/models.py에서 ToDoItem ORM 모델 스키마 구현 (id, title, due_date, priority, status, created_at, updated_at)
- [ ] T009 [P] todo_lib/db.py에서 DB 초기화 및 테이블 생성 헬퍼 구현
- [ ] T010 todo_lib/repository.py에서 repository CRUD 기본 연산 구현 (add_item, list_items, mark_done, delete_item, get_item)
- [ ] T011 todo_lib/validation.py에서 제목/날짜/우선순위/ID 공유 검증 헬퍼 구현
- [ ] T012 [P] cli/formatters.py에서 CLI 출력 포맷팅 및 오류 출력 헬퍼 구현
- [ ] T013 todo_lib/errors.py에서 서비스 레벨 예외 클래스 및 오류 매핑 구현

**Checkpoint**: Foundation 완성 - 이제 user story 구현을 병렬로 시작할 수 있다.

---

---

## Phase 3: User Story 1 - ToDo 항목 추가 (Priority: P1) 🎯 MVP

**Goal**: 제목(필수)/마감일(선택)/우선순위(선택)를 받아 새 항목을 저장하고 ID 포함 확인 메시지 제공

**Independent Test**: `todo add` 실행 후 DB에 항목이 저장되고, 빈 제목/잘못된 날짜/과거 날짜 입력이 올바르게 처리되는지 검증

### Tests for User Story 1 (REQUIRED) ⚠️

> **NOTE: 구현 전에 이 테스트들을 먼저 작성하고 FAIL 상태 확인**

- [ ] T014 [P] [US1] tests/unit/test_add_todo.py에서 add 검증 및 ID 할당에 대한 단위 테스트 작성
- [ ] T015 [P] [US1] tests/integration/test_cli_add.py에서 add 명령 성공 및 입력 오류에 대한 통합 테스트 작성
- [ ] T039 [US1] tests/integration/test_cli_persistence.py에서 프로세스 재시작 후 list 재조회 영속성 통합 테스트 추가

### Implementation for User Story 1

- [ ] T016 [US1] todo_lib/service.py에서 add_todo 서비스 워크플로우 구현
- [ ] T017 [US1] todo_lib/service.py에서 과거 날짜 마감일 경고 동작 구현
- [ ] T018 [US1] cli/main.py에서 `todo add` 명령 옵션 및 서비스 호출 연결
- [ ] T019 [US1] cli/formatters.py에서 add 명령 성공/오류/경고 메시지 구현

**Checkpoint**: 이 지점에서 User Story 1이 완전히 기능하고 독립적으로 테스트 가능해야 함

---

---

## Phase 4: User Story 2 - 전체 목록 조회 및 필터링 (Priority: P2)

**Goal**: 전체 목록 조회 및 완료 상태/우선순위 필터링 조회 지원

**Independent Test**: 혼합 데이터에서 `todo list` 기본 조회 및 필터 조합 결과가 정확한지 검증

### Tests for User Story 2 (REQUIRED) ⚠️

- [ ] T020 [P] [US2] tests/unit/test_list_todo.py에서 list 필터링 규칙에 대한 단위 테스트 작성
- [ ] T021 [P] [US2] tests/integration/test_cli_list.py에서 list 명령 출력에 대한 통합 테스트 작성

### Implementation for User Story 2

- [ ] T022 [US2] todo_lib/service.py에서 list_todos 필터링 쿼리 로직 구현
- [ ] T023 [US2] cli/main.py에서 `todo list` 필터 옵션 및 서비스 호출 연결
- [ ] T024 [US2] cli/formatters.py에서 list 행 렌더링 및 빈 목록 메시지 구현

**Checkpoint**: 이 지점에서 User Story 1과 2가 모두 독립적으로 작동해야 함

---

---

## Phase 5: User Story 3 - 항목 완료 처리 (Priority: P3)

**Goal**: ID 기준 완료 처리 및 중복 완료/없는 ID 오류 응답 지원

**Independent Test**: `todo done <id>` 실행 후 상태 전환, 중복 완료 안내, 없는 ID 오류를 각각 검증

### Tests for User Story 3 (REQUIRED) ⚠️

- [ ] T025 [P] [US3] tests/unit/test_done_todo.py에서 done 상태 전환 규칙에 대한 단위 테스트 작성
- [ ] T026 [P] [US3] tests/integration/test_cli_done.py에서 done 명령 응답에 대한 통합 테스트 작성
- [ ] T040 [US3] tests/integration/test_cli_done.py에서 `todo done` 시 숫자가 아닌 ID 입력에 대한 통합 테스트 추가

### Implementation for User Story 3

- [ ] T027 [US3] todo_lib/service.py에서 mark_done 워크플로우 및 completed_at 처리 구현
- [ ] T028 [US3] cli/main.py에서 `todo done` 명령 및 ID 파싱 동작 연결
- [ ] T029 [US3] cli/formatters.py에서 done 명령 응답 메시지 구현

**Checkpoint**: User Story 1, 2, 3이 독립적으로 기능해야 함

---

---

## Phase 6: User Story 4 - 항목 삭제 (Priority: P4)

**Goal**: ID 기준 영구 삭제 및 없는 ID 오류 응답 지원

**Independent Test**: `todo delete <id>` 실행 후 항목 제거 및 존재하지 않는 ID 오류 검증

### Tests for User Story 4 (REQUIRED) ⚠️

- [ ] T030 [P] [US4] tests/unit/test_delete_todo.py에서 delete 동작에 대한 단위 테스트 작성
- [ ] T031 [P] [US4] tests/integration/test_cli_delete.py에서 delete 명령 응답에 대한 통합 테스트 작성
- [ ] T041 [US4] tests/integration/test_cli_delete.py에서 `todo delete` 시 숫자가 아닌 ID 입력에 대한 통합 테스트 추가

### Implementation for User Story 4

- [ ] T032 [US4] todo_lib/service.py에서 delete_todo 워크플로우 구현
- [ ] T033 [US4] cli/main.py에서 `todo delete` 명령 및 ID 파싱 동작 연결
- [ ] T034 [US4] cli/formatters.py에서 delete 명령 응답 메시지 구현

**Checkpoint**: 모든 user story가 독립적으로 기능해야 함

---

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 전체 품질 보강 및 문서/검증 마무리

- [ ] T035 [P] tests/integration/test_cli_system_errors.py에 손상된 DB 처리 통합 테스트 추가
- [ ] T036 cli/main.py와 todo_lib/errors.py에서 SQLite 오픈/읽기 실패를 exit-code 매핑으로 구현
- [ ] T037 [P] specs/001-cli-todo-app/quickstart.md에서 검증 단계 업데이트
- [ ] T038 모든 단위 테스트 및 통합 테스트가 통과하고 커버리지 98% 이상 달성 확인
- [X] T038 Run full test and coverage command documentation update in specs/001-cli-todo-app/quickstart.md
- [X] T042 Add measurable command-time benchmark test for SC-001 (<=30s) in tests/integration/test_cli_performance.py
- [X] T043 Add 1,000-item responsiveness test for SC-005 in tests/integration/test_cli_performance.py
- [X] T044 Add invalid-input matrix test for SC-003 (error message + no data corruption) in tests/integration/test_cli_validation_matrix.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - MVP baseline
- **User Story 2 (P2)**: Depends on US1 command skeleton reuse in cli/main.py
- **User Story 3 (P3)**: Depends on US1 data creation path and shared ID validation
- **User Story 4 (P4)**: Depends on US1 data creation path and shared ID validation

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Service rule implementation before CLI wiring
- CLI wiring before output polish
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004, T006 can run in parallel during Setup
- T008, T009, T012 can run in parallel during Foundational
- Each story의 테스트 2개는 [P]로 병렬 작성 가능
- T042, T043, T044는 기능 구현 완료 후 병렬로 수행 가능
- Story 간 병렬 개발은 가능하지만, 현재 계획은 커밋 단위 안정성을 위해 우선순위 순차 진행을 권장

---

## Parallel Example: User Story 1

```bash
# Run in parallel after entering Phase 3:
Task: T014 [US1] unit tests in tests/unit/test_service_add.py
Task: T015 [US1] integration tests in tests/integration/test_cli_add.py
```

## Parallel Example: User Story 2

```bash
# Run in parallel after entering Phase 4:
Task: T020 [US2] unit tests in tests/unit/test_service_list.py
Task: T021 [US2] integration tests in tests/integration/test_cli_list.py
```

## Parallel Example: User Story 3

```bash
# Run in parallel after entering Phase 5:
Task: T025 [US3] unit tests in tests/unit/test_service_done.py
Task: T026 [US3] integration tests in tests/integration/test_cli_done.py
```

## Parallel Example: User Story 4

```bash
# Run in parallel after entering Phase 6:
Task: T030 [US4] unit tests in tests/unit/test_service_delete.py
Task: T031 [US4] integration tests in tests/integration/test_cli_delete.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate with US1 unit/integration tests
5. Demo MVP (`todo add` + persistence)

### Incremental Delivery

1. Setup + Foundational 완료
2. US1 추가 후 검증
3. US2 추가 후 검증
4. US3 추가 후 검증
5. US4 추가 후 검증
6. Polish 단계에서 시스템 오류/문서/커버리지 마무리

### Commit Strategy (One Task = One Commit)

- 각 체크박스 task를 하나의 커밋 단위로 수행한다.
- 커밋 메시지는 `feat:`/`test:`/`chore:` 접두사로 task ID를 포함한다.
- 예: `test: T014 add unit tests for add_todo validation`

---

## Notes

- [P] tasks는 서로 다른 파일을 변경하도록 분해했다.
- [Story] 라벨은 User Story phase에만 부여했다.
- 모든 user story는 독립 테스트 기준을 포함한다.
- spec, plan, tasks는 SQLite + SQLAlchemy 결정으로 정렬했다.
