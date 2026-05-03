# CLI Contract: CLI ToDo Manager

## Command 1: add
- Syntax: `todo add "<title>" [--due YYYY-MM-DD] [--priority high|medium|low]`
- Behavior:
  - title 필수
  - due, priority 선택
  - 성공 시 생성된 항목 ID와 상태(pending) 출력
- Error Contract:
  - title 누락: `error: title is required`
  - due 형식 오류: `error: due must be YYYY-MM-DD`
  - priority 오류: `error: priority must be one of high|medium|low`

## Command 2: list
- Syntax: `todo list [--filter done|pending] [--priority high|medium|low]`
- Behavior:
  - 기본값: 전체 항목 조회
  - filter 지정 시 상태 조건 적용
  - priority 지정 시 우선순위 조건 적용
  - 두 옵션 동시 지정 시 AND 조건으로 적용
- Output Contract:
  - 각 항목은 `id | title | due(optional) | priority(optional) | status` 형식 표시

## Command 3: done
- Syntax: `todo done <id>`
- Behavior:
  - 대상 항목 상태를 done으로 변경
  - 이미 done이면 안내 메시지 출력
- Error Contract:
  - id 형식 오류: `error: id must be a positive integer`
  - id 미존재: `error: todo item not found`

## Command 4: delete
- Syntax: `todo delete <id>`
- Behavior:
  - 대상 항목 영구 삭제
- Error Contract:
  - id 형식 오류: `error: id must be a positive integer`
  - id 미존재: `error: todo item not found`

## Non-Functional Contract
- 본 계약은 CLI 인터페이스만 다루며 REST API/GUI는 포함하지 않는다.
- 출력 메시지는 사용자가 다음 행동을 이해할 수 있도록 간결하고 명확해야 한다.
