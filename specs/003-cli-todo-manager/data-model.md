# Data Model: CLI ToDo Manager

## Entity: ToDoItem
- Description: 사용자의 단일 할 일 항목
- Fields:
  - id: integer, primary key, auto increment
  - title: string, required, 1자 이상
  - due_date: date, optional
  - priority: enum(high, medium, low), optional
  - status: enum(pending, done), required, 기본값 pending
  - created_at: datetime, required
  - updated_at: datetime, required

## Entity: ListFilter
- Description: 목록 조회 시 적용할 조건
- Fields:
  - status_filter: enum(done, pending), optional
  - priority_filter: enum(high, medium, low), optional

## Entity: CommandResult
- Description: CLI 명령 실행 결과 표준 표현
- Fields:
  - success: boolean
  - message: string
  - item_id: integer, optional
  - affected_count: integer, optional

## Validation Rules
- title은 공백 문자열을 허용하지 않는다.
- due_date가 제공되면 YYYY-MM-DD 형식이어야 한다.
- priority가 제공되면 high|medium|low 중 하나여야 한다.
- done/delete 명령의 id는 양의 정수여야 한다.
- 존재하지 않는 id에 대한 done/delete는 데이터 변경 없이 오류 메시지를 반환한다.

## State Transitions
- ToDoItem.status:
  - pending -> done: `todo done <id>` 성공 시
  - done -> done: 재완료 요청 시 변경 없음(멱등 처리) 또는 안내 메시지 반환
- ToDoItem lifecycle:
  - created -> deleted: `todo delete <id>` 성공 시 영구 삭제

## Relationships
- ToDoItem은 독립 엔티티이며 다른 엔티티와의 외래키 관계가 없다.
- ListFilter는 영속 엔티티가 아닌 조회 요청 모델이다.
- CommandResult는 영속 엔티티가 아닌 응답 모델이다.
