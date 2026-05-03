<!--
Sync Impact Report
- Version change: template -> 1.0.1
- Modified principles:
  - PRINCIPLE_1_NAME -> I. 레이어 분리
  - PRINCIPLE_2_NAME -> II. 테스트 우선 (NON-NEGOTIABLE)
  - PRINCIPLE_3_NAME -> III. 최소 의존성
  - PRINCIPLE_4_NAME -> IV. 단순함 우선
  - PRINCIPLE_5_NAME -> V. CLI 도구 구현
- Added sections:
  - Project Scope & Constraints
  - Development Workflow & Quality Gates
- Removed sections:
  - 없음
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
  - ✅ no files found: .specify/templates/commands/*.md
- Deferred TODOs:
  - 없음
-->
# CLI ToDo Manager Constitution

## Core Principles

### I. 레이어 분리

비즈니스 로직은 MUST `src/core` 계층에 위치하고, 입출력 처리(인자 파싱, 화면 출력, 파일 I/O)는
MUST 별도 인터페이스 계층(`src/cli`, `src/adapters`)에 위치한다. core 계층은 CLI 프레임워크,
터미널 출력 형식, 외부 전송 프로토콜에 직접 의존하면 안 된다.
Rationale: 계층 결합을 낮추면 테스트 작성이 단순해지고 기능 변경 시 회귀 범위를 줄일 수 있다.

### II. 테스트 우선 (NON-NEGOTIABLE)

모든 구현 작업은 MUST 실패하는 테스트 코드를 먼저 작성한 뒤 시작한다. 테스트 코드가 없는
구현 코드는 MUST 작성하거나 병합할 수 없다. 버그 수정 또한 MUST 재현 테스트를 먼저 추가한 뒤
수정한다.
Rationale: 테스트 우선은 요구사항 누락을 조기 발견하고 회귀를 방지하는 가장 직접적인 품질 게이트다.

### III. 최소 의존성

외부 패키지 추가 전에는 MUST 표준 라이브러리 대안, 유지보수 비용, 라이선스, 보안 위험을
검토한다. 검토 근거가 없는 신규 의존성은 MUST 추가하지 않는다. 사용되지 않는 의존성은
SHOULD 즉시 제거한다.
Rationale: 의존성 축소는 빌드 안정성, 보안성, 온보딩 속도를 동시에 개선한다.

### IV. 단순함 우선

현재 요구사항으로 정당화되지 않는 추상화, 확장 포인트, 레이어는 MUST 도입하지 않는다.
구현은 SHOULD 명확하고 직접적인 흐름을 우선하며, 복잡한 설계는 실증된 필요가 있을 때만
도입한다.
Rationale: 불필요한 일반화는 학습 비용과 결함 가능성을 증가시키며 전달 속도를 저하시킨다.

### V. CLI 도구 구현

이 프로젝트의 전달 대상은 MUST 터미널에서 실행되는 CLI ToDo 관리 도구다. REST API,
GUI, 웹 인터페이스, 모바일 앱은 MUST 프로젝트 범위 밖으로 유지한다. 관련 제안이 발생하면 별도
프로젝트 또는 후속 헌법 개정으로 분리한다.
Rationale: 범위를 고정해야 기능 우선순위와 아키텍처 판단이 일관되게 유지된다.

## Project Scope & Constraints

- 대상 사용자 경험은 터미널 명령 기반이다.
- 명령 인터페이스는 MUST 일관된 옵션 체계와 오류 메시지 규칙을 유지한다.
- 데이터 저장 방식은 파일 기반 또는 로컬 데이터베이스 중 선택할 수 있으나, 선택된 방식은
  MUST core 계층 추상화 뒤에 배치한다.
- 네트워크 API 제공, 브라우저 렌더링, GUI 이벤트 루프 통합은 현재 릴리스 범위에서 제외한다.

## Development Workflow & Quality Gates

- 기능 단위 작업 시작 조건: 실패하는 테스트 작성 완료.
- 작업 완료 조건: 테스트 통과, 계층 분리 검토 통과, 신규 의존성 검토 기록 완료(해당 시).
- 코드 리뷰는 MUST 다음 항목을 확인한다: 테스트 선행 여부, core 계층 순수성, 범위 준수 여부.
- 문서(`spec.md`, `plan.md`, `tasks.md`)는 MUST 본 헌법의 MUST 규칙과 충돌하지 않아야 한다.

## Governance

이 헌법은 프로젝트 내 다른 실행 관행보다 우선한다. 개정 절차는 다음을 따른다.

1. 변경 제안자는 수정 이유, 영향 범위, 마이그레이션 필요 여부를 문서화해야 한다.
2. 변경안은 관련 템플릿(`.specify/templates/*.md`)과의 정합성 검토를 통과해야 한다.
3. 승인 후 버전은 Semantic Versioning으로 갱신한다.

버전 정책:

- MAJOR: 기존 원칙 삭제, 의미 역전, 비호환 거버넌스 변경.
- MINOR: 새로운 원칙/섹션 추가 또는 의무 규칙의 실질적 확장.
- PATCH: 의미 변화 없는 문구 명확화, 오탈자 수정, 표현 개선.

준수 점검 정책:

- 모든 Plan의 Constitution Check는 본 헌법의 5개 원칙을 게이트로 검증해야 한다.
- 모든 Tasks는 테스트 선행 작업을 구현 작업보다 먼저 배치해야 한다.
- 범위 외 항목(REST API/GUI)이 탐지되면 Plan 또는 Spec 단계에서 차단한다.

**Version**: 1.0.1 | **Ratified**: 2026-05-02 | **Last Amended**: 2026-05-03
