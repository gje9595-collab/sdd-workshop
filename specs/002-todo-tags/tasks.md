# Tasks: ToDo 태그 기능 통합

**Input**: Design documents from `/specs/002-todo-tags/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: 테스트는 필수다. 각 사용자 스토리 구현 전에 실패하는 테스트를 먼저 작성한다.

**Organization**: 사용자 스토리별 독립 구현/검증이 가능하도록 그룹화한다.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 병렬 가능(서로 다른 파일, 선행 의존성 없음)
- **[Story]**: 해당 사용자 스토리(US1, US2, US3)
- 모든 작업 설명에는 정확한 파일 경로를 포함한다.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 태그 기능 작업을 위한 테스트/검증 준비

- [ ] T001 [P] 태그 검증 테스트 스캐폴드 작성 in tests/unit/test_tags_validation.py
- [ ] T002 [P] 태그 서비스 테스트 스캐폴드 작성 in tests/unit/test_service_tags.py
- [ ] T003 [P] 태그 CLI 통합 테스트 스캐폴드 작성 in tests/integration/test_cli_tags.py
- [ ] T004 회귀 baseline 실행 절차를 정리 in specs/002-todo-tags/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 모든 스토리에서 공통으로 사용하는 태그 데이터/검증 기반 구축

**⚠️ CRITICAL**: 이 단계 완료 전에는 사용자 스토리 구현을 시작하지 않는다.

- [ ] T005 ToDoItem에 tags JSON 컬럼 추가 in todo_lib/models.py
- [ ] T006 [P] tags 정규화/중복/형식 검증 함수 추가 in todo_lib/validation.py
- [ ] T007 [P] add/list 태그 파라미터 수용 시그니처 확장 in todo_lib/repository.py
- [ ] T008 tags null/빈 목록 호환 처리 규칙 통합 in todo_lib/service.py

**Checkpoint**: 태그 저장 구조와 공통 검증 기반이 준비되어 스토리 구현을 병렬로 시작할 수 있다.

---

## Phase 3: User Story 1 - 태그 포함 항목 생성 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 `todo add`에서 선택적으로 태그를 지정해 저장할 수 있다.

**Independent Test**: `todo add "제목" --tag 업무 --tag 중요` 실행 후 저장 항목에 태그가 반영되고, 태그 미지정 add는 기존과 동일하게 성공해야 한다.

### Tests for User Story 1 (REQUIRED) ⚠️

- [ ] T009 [P] [US1] add_todo 태그 저장/미지정 호환 단위 테스트 작성 in tests/unit/test_service_tags.py
- [ ] T010 [P] [US1] `todo add --tag` 성공/입력오류 통합 테스트 작성 in tests/integration/test_cli_tags.py

### Implementation for User Story 1

- [ ] T011 [US1] add_item 태그 저장 로직 구현 in todo_lib/repository.py
- [ ] T012 [US1] add_todo tags 파라미터 및 검증 흐름 구현 in todo_lib/service.py
- [ ] T013 [US1] `todo add` 반복 `--tag` 옵션 연결 in cli/main.py
- [ ] T014 [US1] add 명령 태그 입력 오류 메시지 매핑 보강 in cli/main.py

**Checkpoint**: US1 단독으로 태그 저장 기능이 동작하고 테스트 가능해야 한다.

---

## Phase 4: User Story 2 - 태그 기반 목록 조회 (Priority: P2)

**Goal**: 사용자가 `todo list --tag`로 태그가 포함된 항목만 조회할 수 있다.

**Independent Test**: 서로 다른 태그 항목을 만든 후 `todo list --tag 업무`가 일치 항목만 출력하고, 기존 필터와 동시 사용 시 교집합 결과를 반환해야 한다.

### Tests for User Story 2 (REQUIRED) ⚠️

- [ ] T015 [P] [US2] list_todos 태그 필터/교집합 단위 테스트 작성 in tests/unit/test_service_tags.py
- [ ] T016 [P] [US2] `todo list --tag` 출력/교집합 통합 테스트 작성 in tests/integration/test_cli_tags.py

### Implementation for User Story 2

- [ ] T017 [US2] list_items 태그 필터 조건 구현 in todo_lib/repository.py
- [ ] T018 [US2] list_todos tag 파라미터 결합 로직 구현 in todo_lib/service.py
- [ ] T019 [US2] `todo list`의 `--tag` 옵션 추가 in cli/main.py
- [ ] T020 [US2] 목록 출력에 태그 컬럼 렌더링 추가 in cli/formatters.py

**Checkpoint**: US1과 US2가 각각 독립적으로 동작하고 함께 사용할 수 있어야 한다.

---

## Phase 5: User Story 3 - 회귀 없는 확장 (Priority: P3)

**Goal**: 태그 기능 추가 후 기존 add/list/done/delete 동작이 깨지지 않는다.

**Independent Test**: 기존 테스트 스위트를 그대로 실행해 100% 통과하고, 태그 옵션 미사용 명령의 결과/종료 코드가 기존과 동일해야 한다.

### Tests for User Story 3 (REQUIRED) ⚠️

- [ ] T021 [P] [US3] 태그 미사용 기존 동작 회귀 테스트 작성 in tests/integration/test_cli_regression_no_tags.py
- [ ] T022 [P] [US3] 기존 서비스 경로 회귀 테스트 보강 in tests/unit/test_service_regression_no_tags.py

### Implementation for User Story 3

- [ ] T023 [US3] done/delete 명령 비영향성 검증 및 최소 수정 반영 in cli/main.py
- [ ] T024 [US3] tags null 기존 레코드 호환성 보강 in todo_lib/service.py
- [ ] T025 [US3] 회귀 검증 기준을 quickstart에 반영 in specs/002-todo-tags/quickstart.md

**Checkpoint**: 기존 기능 회귀 없이 태그 기능이 통합되어야 한다.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 전체 품질/문서/검증 마무리

- [ ] T026 [P] CLI 계약 최종 동기화 in specs/002-todo-tags/contracts/cli-contract.md
- [ ] T027 [P] 데이터 모델 문서 최종 동기화 in specs/002-todo-tags/data-model.md
- [ ] T028 전체 테스트 실행 및 결과 확인 in specs/002-todo-tags/quickstart.md
- [ ] T029 커버리지 결과 기록 및 누락 보강 in specs/002-todo-tags/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 즉시 시작 가능
- **Phase 2 (Foundational)**: Phase 1 완료 후 시작, 모든 사용자 스토리를 블로킹
- **Phase 3~5 (User Stories)**: Phase 2 완료 후 시작
- **Phase 6 (Polish)**: 모든 사용자 스토리 완료 후 시작

### User Story Dependencies

- **US1 (P1)**: Foundation 이후 독립 시작 가능 (MVP)
- **US2 (P2)**: Foundation 이후 시작 가능, US1 결과와 병행 가능
- **US3 (P3)**: US1/US2 완료 후 회귀 안정화 단계로 진행 권장

### Within Each User Story

- 테스트 작성 및 실패 확인 후 구현 시작
- repository/service 구현 후 CLI 연결
- 스토리 단위 테스트 통과 후 다음 스토리 진행

### Parallel Opportunities

- Setup의 T001, T002, T003 병렬 가능
- Foundation의 T006, T007 병렬 가능
- 각 스토리의 테스트 작업(T009/T010, T015/T016, T021/T022) 병렬 가능
- Polish의 T026, T027 병렬 가능

---

## Parallel Example: User Story 1

```bash
# US1 테스트를 병렬로 먼저 작성
Task: T009 tests/unit/test_service_tags.py
Task: T010 tests/integration/test_cli_tags.py

# US1 구현 순서
Task: T011 todo_lib/repository.py
Task: T012 todo_lib/service.py
Task: T013 cli/main.py
```

---

## Implementation Strategy

### MVP First (US1)

1. Phase 1 완료
2. Phase 2 완료
3. Phase 3(US1) 완료
4. US1 단독 검증 후 데모

### Incremental Delivery

1. US1(태그 저장) 배포 가능 상태 확보
2. US2(태그 조회) 추가
3. US3(회귀 안정화) 완료
4. Polish로 문서/검증 마무리

### Parallel Team Strategy

1. 한 명: Foundation(T005~T008)
2. 두 명 병행: US1 테스트/구현 분담
3. 이후 US2 테스트/구현 병행
4. 마지막 US3 회귀 전담 + 전체 검증

---

## Notes

- [P] 표시는 서로 다른 파일을 수정하고 선행 의존성이 없는 경우만 부여했다.
- 모든 태스크는 구체적 파일 경로를 포함해 즉시 실행 가능하게 작성했다.
- 기존 테스트 유지가 핵심 요구사항이므로 US3를 회귀 전용 단계로 분리했다.
