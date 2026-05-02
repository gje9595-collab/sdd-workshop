# Feature Specification: CLI ToDo Manager

**Feature Branch**: `main`  
**Created**: 2026-05-02  
**Status**: Draft  
**Input**: User description: "CLI기반의 ToDo 관리앱을 만들고 싶어, 대상 사용자 :터미널을 사용하는 개인 개발자 주요기능은 1. ToDo 항목 추가, 제목(필수), 마감일(선택), 우선순위(선택) 2. 전체목록 조회, 완료/미완료/우선순위로 필터링 가능 3. 항목에 대한 완료 처리 4. 항목 삭제, 항목 ID로 삭제 기술 스택은 아직 미정"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 빠른 ToDo 기록 (Priority: P1)

터미널을 사용하는 개인 개발자는 해야 할 일을 빠르게 기록하기 위해 제목을 필수로 입력하고, 필요할 때만 마감일과 우선순위를 선택해 ToDo 항목을 추가할 수 있어야 한다.

**Why this priority**: ToDo 관리의 시작점이며, 항목을 생성하지 못하면 이후 조회/완료/삭제 흐름이 모두 성립하지 않는다.

**Independent Test**: 사용자가 제목만 입력해 항목을 생성하고, 선택값 없이도 저장이 성공하는지 확인하면 독립적으로 검증 가능하다. 추가로 마감일/우선순위를 함께 입력한 항목도 저장되는지 확인한다.

**Acceptance Scenarios**:

1. **Given** 사용자가 터미널에서 항목 추가 명령을 실행한 상태, **When** 제목만 입력한다, **Then** 새로운 ToDo 항목이 생성되고 기본 상태는 미완료로 저장된다.
2. **Given** 사용자가 항목 추가를 수행하는 상태, **When** 제목과 함께 마감일 및 우선순위를 입력한다, **Then** 선택 입력값이 함께 저장된 항목이 생성된다.
3. **Given** 사용자가 항목 추가를 수행하는 상태, **When** 제목을 비워 둔다, **Then** 시스템은 항목을 생성하지 않고 제목이 필수임을 알린다.

---

### User Story 2 - 상태/우선순위 기반 목록 확인 (Priority: P2)

사용자는 현재 할 일 상태를 파악하기 위해 전체 목록을 보고, 완료/미완료/우선순위 조건으로 목록을 좁혀 확인할 수 있어야 한다.

**Why this priority**: 생성된 항목을 실제로 관리하려면 현재 상태를 빠르게 파악하는 조회 기능이 필요하다.

**Independent Test**: 완료와 미완료 항목이 섞인 데이터에서 전체 조회와 각 필터 조회를 실행해, 조건에 맞는 항목만 표시되는지 확인한다.

**Acceptance Scenarios**:

1. **Given** 여러 ToDo 항목이 저장되어 있다, **When** 사용자가 전체 목록 조회를 실행한다, **Then** 모든 항목이 식별 가능한 ID와 함께 표시된다.
2. **Given** 완료와 미완료 항목이 함께 존재한다, **When** 사용자가 완료 상태 필터로 조회한다, **Then** 완료된 항목만 표시된다.
3. **Given** 서로 다른 우선순위 항목이 존재한다, **When** 사용자가 특정 우선순위 필터로 조회한다, **Then** 해당 우선순위 항목만 표시된다.

---

### User Story 3 - 항목 완료 및 삭제 정리 (Priority: P3)

사용자는 작업 흐름을 정리하기 위해 특정 항목을 완료 처리하고, 더 이상 필요 없는 항목을 ID로 삭제할 수 있어야 한다.

**Why this priority**: 기록된 할 일을 최신 상태로 유지해야 관리 효율이 유지되며, 정리 기능은 지속 사용에 필수적이다.

**Independent Test**: 특정 ID를 완료 처리한 뒤 조회에서 상태가 바뀌었는지 검증하고, 다른 ID를 삭제해 목록에서 제거되었는지 확인한다.

**Acceptance Scenarios**:

1. **Given** 미완료 상태의 항목 ID가 존재한다, **When** 사용자가 해당 ID를 완료 처리한다, **Then** 항목 상태가 완료로 변경된다.
2. **Given** 삭제 대상 항목 ID가 존재한다, **When** 사용자가 해당 ID 삭제를 실행한다, **Then** 항목이 목록에서 제거된다.
3. **Given** 존재하지 않는 항목 ID를 사용한다, **When** 완료 처리 또는 삭제를 시도한다, **Then** 시스템은 변경 없이 유효하지 않은 ID임을 알린다.

---

### Edge Cases

- 사용자가 매우 긴 제목을 입력할 때도 항목이 잘리거나 손실되지 않고 일관되게 저장/표시되는가?
- 마감일을 입력하지 않은 항목과 입력한 항목이 함께 있을 때 목록/필터 결과가 혼동 없이 표시되는가?
- 빈 목록에서 조회, 완료 처리, 삭제를 실행할 때 시스템이 실패하지 않고 이해 가능한 안내를 제공하는가?
- 동일한 제목의 항목이 여러 개 있을 때도 ID 기준 완료/삭제가 정확히 대상 1건에만 적용되는가?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a ToDo item with a required title.
- **FR-002**: System MUST allow users to optionally provide due date when creating a ToDo item.
- **FR-003**: System MUST allow users to optionally provide priority when creating a ToDo item.
- **FR-004**: System MUST assign a unique item ID to each created ToDo item so users can reference it.
- **FR-005**: System MUST present a full list view of all ToDo items.
- **FR-006**: System MUST allow list filtering by completion status (completed or not completed).
- **FR-007**: System MUST allow list filtering by priority.
- **FR-008**: System MUST allow users to mark a ToDo item as completed using item ID.
- **FR-009**: System MUST allow users to delete a ToDo item using item ID.
- **FR-010**: System MUST provide clear feedback when a required field is missing or when an invalid item ID is provided.
- **FR-011**: System MUST preserve each item's title, optional due date, optional priority, and completion status between user interactions.

### Key Entities *(include if feature involves data)*

- **ToDo Item**: 사용자의 단일 할 일 단위를 나타내며, 고유 ID, 제목, 마감일(선택), 우선순위(선택), 완료 상태를 가진다.
- **Filter Criteria**: 목록 조회 시 적용되는 조건을 나타내며, 완료 상태와 우선순위 값을 포함한다.

## Out of Scope *(mandatory)*

- REST API 서버 구현은 범위 밖으로 유지한다.
- GUI/웹/모바일 인터페이스 구현은 범위 밖으로 유지한다.
- 멀티 사용자 협업, 계정/인증, 권한 관리 기능은 범위 밖으로 유지한다.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 사용자는 신규 ToDo 항목(제목 필수, 선택값 포함 가능)을 10초 이내에 입력 완료할 수 있다.
- **SC-002**: 사용자는 최대 200개 항목이 있는 목록에서 전체 조회 또는 필터 조회 결과를 2초 이내에 확인할 수 있다.
- **SC-003**: 사용자 테스트 시 항목 완료 처리 및 ID 기반 삭제를 첫 시도에 성공하는 비율이 95% 이상이다.
- **SC-004**: 사용자 테스트 시 필수값 누락/잘못된 ID 입력 상황에서 100%의 시나리오가 실패 원인을 이해 가능한 안내로 제공한다.

## Assumptions

- 대상 사용자는 단일 로컬 환경에서 CLI를 사용하는 개인 개발자다.
- 초기 버전은 개인 사용 중심으로 설계되며, 동시 다중 사용자 편집은 고려하지 않는다.
- 우선순위는 사용자가 구분 가능한 사전 정의 단계(예: 높음/중간/낮음)로 해석한다.
- 항목 ID는 사용자 세션과 무관하게 항목 식별에 일관되게 사용된다고 가정한다.
- 기능 범위는 항목 추가/조회(필터)/완료/삭제에 한정하며 통계, 알림, 자동 동기화는 제외한다.
