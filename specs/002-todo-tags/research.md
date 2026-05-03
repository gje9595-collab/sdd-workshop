# Research: ToDo 태그 기능 통합

## Decision 1: 태그 저장 방식
- Decision: `ToDoItem.tags`를 SQLite JSON 컬럼으로 저장한다.
- Rationale: 단순함 우선 원칙을 충족하고, 기존 단일 테이블 구조를 유지할 수 있다.
- Alternatives considered:
  - 별도 `tags` 테이블 + 관계 테이블: 정규화 이점은 있으나 구현/마이그레이션 복잡도가 과도함.
  - 문자열 CSV 저장: 파싱/검증/필터 정확도가 떨어져 회귀 위험이 큼.

## Decision 2: CLI 태그 입력 형식
- Decision: `todo add`에서 `--tag` 옵션 반복 입력을 지원한다.
- Rationale: Typer 기본 패턴과 일치하며 사용자가 직관적으로 여러 태그를 전달할 수 있다.
- Alternatives considered:
  - 쉼표 구분 단일 문자열(`--tags a,b,c`): escaping/공백 처리 규칙이 복잡해짐.
  - 태그 파일 입력: 범위 과도 확장.

## Decision 3: 태그 필터 결합 규칙
- Decision: `list --tag`는 기존 `--filter`, `--priority`와 교집합으로 동작한다.
- Rationale: 기존 필터 정신을 유지하고 예측 가능한 결과를 제공한다.
- Alternatives considered:
  - 우선순위 기반 덮어쓰기: 조건 충돌 시 예측 불가능.
  - OR 결합: 기존 사용자 기대와 불일치.

## Decision 4: 회귀 전략
- Decision: 기존 테스트 전량 통과를 태그 기능 머지의 필수 게이트로 둔다.
- Rationale: 사용자 요청의 핵심 요구사항(기존 테스트가 깨지지 않아야 함)을 직접 보장한다.
- Alternatives considered:
  - 일부 스모크 테스트만 실행: 회귀 누락 가능성이 큼.

## Clarification Resolution
- Technical Context의 NEEDS CLARIFICATION 항목 없음.
- 스택/저장/필터 규칙은 spec의 FR-001~FR-008, Assumptions로 확정됨.
