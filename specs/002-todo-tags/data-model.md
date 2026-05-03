# Data Model: ToDo 태그 기능 통합

## Entity: ToDoItem (확장)

기존 엔티티에 아래 필드가 추가된다.

- `tags`
  - Type: JSON
  - Nullable: True
  - Default: `null` (런타임에서 빈 목록으로 취급)
  - Description: 항목에 연결된 태그 문자열 목록

## Validation Rules (tags)

- 태그 개수: 0개 이상 (상한은 팀 정책으로 tasks 단계에서 확정)
- 각 태그: 빈 문자열 금지
- 공백 normalize: 앞뒤 공백 제거
- 중복 태그: 중복 제거 또는 오류 처리 정책을 단일 규칙으로 고정 (tasks 단계에서 테스트로 확정)

## Query/Filter Semantics

- `list_todos(filter_status, priority, tag)`
  - `tag`가 주어지면 `tags`에 해당 태그를 포함하는 항목만 반환
  - `filter_status`/`priority`와 동시에 주어지면 교집합 조건으로 적용

## Compatibility

- 기존 레코드는 `tags`가 없거나 `null`일 수 있다.
- 서비스/포맷터는 이를 빈 목록으로 해석해야 한다.
- 기존 add/list/done/delete 동작과 종료 코드 계약은 변경하지 않는다.
