# Feature Specification: ToDo 태그 기능 통합

**Feature Branch**: `002-todo-tags`  
**Created**: 2026-05-03  
**Status**: Draft  
**Input**: 기존 Todo CLI 앱에 tags 기능을 추가하고 기존 기능 회귀 없이 통합한다.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 태그 포함 항목 생성 (Priority: P1)

사용자는 기존 add 명령 흐름을 유지한 채 태그를 선택적으로 추가할 수 있어야 한다.

**Why this priority**: 태그 기능의 출발점은 저장 시점이며, 저장이 되지 않으면 필터링 가치가 없다.

**Independent Test**: add 명령으로 태그 1개/다중/없음 케이스를 실행해 저장 결과를 검증하면 독립적으로 검증 가능하다.

**Acceptance Scenarios**:

1. **Given** 사용자가 제목과 태그를 입력한 상태, **When** add 명령을 실행하면, **Then** 항목과 태그가 함께 저장된다.
2. **Given** 사용자가 태그 없이 add 명령을 실행한 상태, **When** 항목이 저장되면, **Then** 기존 동작과 동일하게 성공한다.

---

### User Story 2 - 태그 기반 목록 조회 (Priority: P2)

사용자는 list 명령에서 태그 필터를 지정해 해당 태그가 포함된 항목만 조회할 수 있어야 한다.

**Why this priority**: 저장된 태그를 실제 작업 흐름에서 활용하는 핵심 가치는 조회 필터링이다.

**Independent Test**: 서로 다른 태그를 가진 항목을 만든 뒤 list --tag 결과 집합을 비교하면 독립적으로 검증 가능하다.

**Acceptance Scenarios**:

1. **Given** 태그가 다른 항목들이 존재할 때, **When** list --tag를 실행하면, **Then** 해당 태그를 포함한 항목만 출력된다.
2. **Given** 상태/우선순위 필터와 태그 필터를 함께 사용할 때, **When** list를 실행하면, **Then** 조건 교집합만 출력된다.

---

### User Story 3 - 회귀 없는 확장 (Priority: P3)

사용자는 태그 기능 도입 후에도 기존 add/list/done/delete 기능을 동일하게 사용할 수 있어야 한다.

**Why this priority**: 신규 기능으로 기존 기능이 깨지면 배포 가치를 상실한다.

**Independent Test**: 기존 테스트 스위트를 그대로 실행해 전부 통과하는지 확인하면 독립적으로 검증 가능하다.

**Acceptance Scenarios**:

1. **Given** 태그 기능이 반영된 코드베이스, **When** 기존 테스트를 실행하면, **Then** 회귀 실패가 없어야 한다.
2. **Given** 사용자가 태그 옵션을 사용하지 않을 때, **When** 기존 명령을 실행하면, **Then** 결과/종료 코드가 기존과 동일해야 한다.

### Edge Cases

- 태그가 중복 입력되면 중복 제거 후 저장하거나 입력 오류로 처리되어야 한다.
- 허용되지 않는 태그 형식(빈 값, 과도한 길이, 허용 외 문자)은 입력 오류여야 한다.
- 태그 없는 기존 데이터도 조회/출력 시 오류 없이 처리되어야 한다.
- 태그 필터 결과가 없을 때 기존 빈 목록 메시지 규약을 유지해야 한다.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST 기존 Todo 모델에 tags 속성을 추가하고 다중 태그를 저장할 수 있어야 한다.
- **FR-002**: System MUST 태그 저장 형식으로 JSON 컬럼을 사용해야 한다.
- **FR-003**: System MUST add 명령에서 반복 가능한 --tag 옵션 입력을 허용해야 한다.
- **FR-004**: System MUST list 명령에서 --tag 필터를 지원해야 한다.
- **FR-005**: System MUST --tag 필터를 기존 상태/우선순위 필터와 함께 사용할 수 있어야 한다.
- **FR-006**: System MUST 기존 service 레이어에 태그 필터링 로직을 통합해야 한다.
- **FR-007**: System MUST 기존 테스트가 깨지지 않도록 회귀 호환성을 유지해야 한다.
- **FR-008**: System MUST 기존 기술 스택(Python, Typer, SQLite+SQLAlchemy, pytest)을 유지해야 한다.

### Key Entities *(include if feature involves data)*

- **ToDoItem**: 기존 할 일 엔티티. tags 속성이 추가된다.
- **TagSet**: 항목에 귀속되는 태그 집합. 저장 단위는 JSON 배열.
- **ListFilter**: 상태/우선순위/태그를 결합해 목록 결과를 제한하는 조건 집합.

## Out of Scope *(mandatory)*

- REST API 서버 구현은 범위 밖으로 유지한다.
- GUI/웹/모바일 인터페이스 구현은 범위 밖으로 유지한다.
- 태그 전용 관리 기능(별도 태그 CRUD, 태그 통계)은 범위 밖이다.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 태그 포함 add/list 명령이 기존 명령 체감 속도를 유지해야 한다.
- **SC-002**: 태그 필터 결과 정확도는 테스트 기준 100%여야 한다.
- **SC-003**: 기존 회귀 테스트 통과율은 100%여야 한다.
- **SC-004**: 태그 옵션 미사용 시 기존 사용자 시나리오 결과가 변하지 않아야 한다.

## Assumptions

- 태그는 단순함 우선 원칙에 따라 JSON 컬럼 1개로 저장한다.
- 기존 코드 구조(todo_lib, cli, tests)를 유지하며 확장한다.
- 태그 기능은 기존 워크플로우를 대체하지 않고 보강한다.
