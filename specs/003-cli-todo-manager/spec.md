# Feature Specification: CLI ToDo Manager

**Feature Branch**: `003-cli-todo-manager`  
**Created**: 2026-05-03  
**Status**: Draft  
**Input**: User description: "CLI기반의 ToDo 관리앱을 만들고 싶어,
대상 사용자 :터미널을 사용하는 개인 개발자
주요기능은
1. ToDo 항목 추가, 제목(필수), 마감일(선택), 우선순위(선택)
2. 전체목록 조회, 완료/미완료/우선순위로 필터링 가능
3. 항목에 대한 완료 처리
4. 항목 삭제, 항목 ID로 삭제

기술 스택은 아직 미정"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 빠른 할 일 등록 (Priority: P1)

터미널을 사용하는 개인 개발자는 해야 할 일을 놓치지 않기 위해 제목을 필수로 입력하고, 필요할 때만 마감일과 우선순위를 선택해 ToDo 항목을 추가할 수 있어야 한다.

**Why this priority**: 항목 추가가 가능해야 조회, 완료, 삭제 기능이 의미를 가지며 제품의 최소 가치가 성립한다.

**Independent Test**: 제목만으로 항목이 생성되는지 검증하고, 선택값(마감일/우선순위)을 포함한 항목도 별도로 생성 가능한지 확인하면 독립적으로 테스트할 수 있다.

**Acceptance Scenarios**:

1. **Given** 사용자가 새 항목 추가를 시도하는 상태, **When** 제목만 입력한다, **Then** 항목이 미완료 상태로 생성된다.
2. **Given** 사용자가 새 항목 추가를 시도하는 상태, **When** 제목과 함께 마감일 및 우선순위를 입력한다, **Then** 선택 입력값이 포함된 항목이 생성된다.
3. **Given** 사용자가 새 항목 추가를 시도하는 상태, **When** 제목을 비워 둔다, **Then** 항목은 생성되지 않고 제목이 필수라는 안내가 표시된다.

---

### User Story 2 - 필터 기반 목록 확인 (Priority: P2)

사용자는 현재 해야 할 일의 상태를 빠르게 파악하기 위해 전체 목록을 조회하고 완료/미완료/우선순위 조건으로 항목을 필터링할 수 있어야 한다.

**Why this priority**: 생성된 항목이 늘어날수록 탐색 비용이 커지므로 조회 및 필터 기능은 일상 사용성에 직접적인 영향을 준다.

**Independent Test**: 완료/미완료/우선순위가 섞인 데이터를 준비한 뒤 전체 조회와 각 필터 조회 결과가 조건과 일치하는지 확인하면 독립적으로 검증 가능하다.

**Acceptance Scenarios**:

1. **Given** 여러 항목이 저장되어 있다, **When** 사용자가 전체 목록 조회를 실행한다, **Then** 모든 항목이 고유 ID와 함께 표시된다.
2. **Given** 완료와 미완료 항목이 모두 존재한다, **When** 사용자가 완료 상태 필터를 적용한다, **Then** 조건에 맞는 항목만 표시된다.
3. **Given** 서로 다른 우선순위 항목이 존재한다, **When** 사용자가 특정 우선순위 필터를 적용한다, **Then** 해당 우선순위 항목만 표시된다.

---

### User Story 3 - 항목 완료 및 삭제 (Priority: P3)

사용자는 관리 중인 할 일을 최신 상태로 유지하기 위해 항목을 완료 처리하고, 불필요한 항목은 ID를 기준으로 삭제할 수 있어야 한다.

**Why this priority**: 생성과 조회만으로는 목록이 누적되므로 완료/삭제 기능이 있어야 지속적인 관리가 가능하다.

**Independent Test**: 특정 ID를 완료 처리해 상태 변경을 확인하고, 다른 ID를 삭제해 목록에서 제거되는지 확인하면 독립적으로 테스트할 수 있다.

**Acceptance Scenarios**:

1. **Given** 미완료 항목 ID가 존재한다, **When** 사용자가 해당 ID를 완료 처리한다, **Then** 항목 상태가 완료로 변경된다.
2. **Given** 삭제 대상 항목 ID가 존재한다, **When** 사용자가 해당 ID 삭제를 실행한다, **Then** 항목이 목록에서 제거된다.
3. **Given** 존재하지 않는 항목 ID를 입력한다, **When** 완료 처리 또는 삭제를 시도한다, **Then** 항목 변경 없이 유효하지 않은 ID 안내가 표시된다.

---

### Edge Cases

- 저장된 항목이 전혀 없을 때 목록 조회를 실행하면 빈 상태를 이해 가능한 메시지로 보여주는가?
- 동일한 제목을 가진 항목이 여러 개일 때 ID 기준 완료/삭제가 정확히 1개 항목에만 적용되는가?
- 마감일 없이 생성된 항목과 마감일이 있는 항목이 함께 있을 때 조회/필터 결과가 혼동 없이 표시되는가?
- 잘못된 형식의 마감일 또는 허용되지 않은 우선순위를 입력한 경우 항목 생성이 차단되고 수정 방법이 안내되는가?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a ToDo item with a required title.
- **FR-002**: System MUST allow users to optionally provide a due date when creating a ToDo item.
- **FR-003**: System MUST allow users to optionally provide a priority when creating a ToDo item.
- **FR-004**: System MUST assign a unique ID to each ToDo item.
- **FR-005**: System MUST provide a full list view of all ToDo items.
- **FR-006**: System MUST allow filtering the list by completion status (completed or not completed).
- **FR-007**: System MUST allow filtering the list by priority.
- **FR-008**: System MUST allow users to mark an item as completed using item ID.
- **FR-009**: System MUST allow users to delete an item using item ID.
- **FR-010**: System MUST provide clear feedback when a required field is missing.
- **FR-011**: System MUST provide clear feedback when an invalid item ID is entered for completion or deletion.
- **FR-012**: System MUST preserve each item's title, optional due date, optional priority, and completion status across user interactions.

### Key Entities *(include if feature involves data)*

- **ToDo Item**: 단일 할 일 단위이며 고유 ID, 제목, 마감일(선택), 우선순위(선택), 완료 상태를 가진다.
- **FilterCriteria**: 목록 조회 시 적용되는 조건 집합이며 완료 상태와 우선순위를 포함한다.

## Out of Scope *(mandatory)*

- REST API 서버 구현은 범위 밖으로 유지한다.
- GUI/웹/모바일 인터페이스 구현은 범위 밖으로 유지한다.
- 멀티 사용자 협업, 계정/권한 관리, 외부 동기화 기능은 범위 밖으로 유지한다.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 사용자는 제목 필수 조건을 만족해 신규 ToDo 항목을 10초 이내에 등록할 수 있다.
- **SC-002**: 사용자는 최대 200개 항목 환경에서 전체 조회 또는 필터 조회 결과를 2초 이내에 확인할 수 있다.
- **SC-003**: 사용자 검증에서 완료 처리 및 ID 기반 삭제를 첫 시도에 성공하는 비율이 95% 이상이다.
- **SC-004**: 필수값 누락 또는 잘못된 ID 입력 시 100%의 테스트 시나리오에서 원인과 다음 행동이 명확히 안내된다.

## Assumptions

- 대상 사용자는 터미널 환경을 익숙하게 사용하는 개인 개발자다.
- 초기 릴리스는 단일 사용자 기준이며 동시 편집 충돌 해결은 고려하지 않는다.
- 우선순위는 사용자에게 명확한 제한된 선택값 집합으로 제공된다고 가정한다.
- 항목 ID는 항목 수명주기 동안 변하지 않는 식별자로 사용된다고 가정한다.
- 데이터는 로컬 환경에서 관리되며 네트워크 연동은 포함하지 않는다.
