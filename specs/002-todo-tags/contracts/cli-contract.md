# CLI Contract: ToDo 태그 기능 통합

## Command: add

### Signature
- `todo add <title> [--due YYYY-MM-DD] [--priority high|medium|low] [--tag <value>]...`

### Behavior
- 태그 미지정 시: 기존 add와 동일
- 태그 지정 시: 태그 목록 저장
- 기존 성공/실패 메시지 규약 및 exit code 유지

## Command: list

### Signature
- `todo list [--filter done|pending] [--priority high|medium|low] [--tag <value>]`

### Behavior
- `--tag` 미지정: 기존 list와 동일
- `--tag` 지정: 해당 태그 포함 항목만 반환
- `--filter`, `--priority` 동시 지정 시 교집합 적용

## Unchanged Commands
- `todo done <id>`
- `todo delete <id>`

## Error/Exit Contract
- 사용자 입력 오류: 기존 정책 유지
- 데이터 접근 오류: 기존 정책 유지
- 태그 관련 오류는 기존 validation 오류 흐름으로 처리
