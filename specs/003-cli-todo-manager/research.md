# Research: CLI ToDo Manager

## Decision 1: Python 실행/패키지 관리
- Decision: Python 3.12 + uv를 사용한다.
- Rationale: 사용자 요구사항에 명시되었고, uv는 설치/실행 속도가 빠르며 단일 프로젝트 워크플로에 적합하다.
- Alternatives considered: pip + venv (기본적이지만 반복 작업 속도가 느림), poetry (기능은 풍부하지만 이번 범위에는 과함).

## Decision 2: CLI 프레임워크
- Decision: Typer를 사용한다.
- Rationale: 명령/옵션 정의가 명확하고, 요구된 명령 인터페이스(add/list/done/delete)를 직관적으로 표현할 수 있다.
- Alternatives considered: argparse (표준 라이브러리지만 코드량 증가), click (가능하지만 Typer 대비 타입 힌트 기반 사용성 낮음).

## Decision 3: 데이터 저장 방식
- Decision: 로컬 파일 기반 SQLite를 사용한다.
- Rationale: 서버 불필요, 단일 사용자 CLI에 적합, 운영 복잡도 최소화.
- Alternatives considered: JSON 파일 (간단하지만 필터/상태 업데이트 일관성 관리 부담), PostgreSQL (현재 범위 과도).

## Decision 4: 데이터 접근 라이브러리
- Decision: SQLAlchemy를 사용한다.
- Rationale: 허용 의존성 목록에 포함되어 있고, SQLite와 결합해 CRUD/필터 로직을 명확히 구현할 수 있다.
- Alternatives considered: sqlite3 직접 사용 (의존성 추가는 없지만 쿼리/매핑 보일러플레이트 증가).

## Decision 5: 테스트 도구
- Decision: pytest + pytest-cov를 사용한다.
- Rationale: 헌법 원칙의 테스트 우선을 실천하기에 적합하고, 커버리지 측정으로 완료 기준을 정량화할 수 있다.
- Alternatives considered: unittest (내장 도구이나 작성량 증가), nose2 (생태계/활성도 측면에서 우선순위 낮음).

## Decision 6: 레이어 분리 전략
- Decision: 비즈니스 로직은 todo_lib/, CLI 입출력은 cli/로 분리한다.
- Rationale: 헌법의 레이어 분리 원칙 충족, 테스트에서 비즈니스 로직 단독 검증이 가능하다.
- Alternatives considered: 단일 모듈 구조 (초기 작성은 빠르나 UI와 로직 결합이 커짐).

## Decision 7: 단순함 우선 구현 원칙
- Decision: 추상 인터페이스(예: ITodoRepository) 없이 직접 클래스/함수로 구현한다.
- Rationale: 현재 요구사항이 단일 저장소(SQLite)와 단일 UI(CLI)로 고정되어 추상 계층이 불필요하다.
- Alternatives considered: Repository 인터페이스 계층 도입 (확장성은 있으나 현재 범위에서 과설계).

## Decision 8: 우선순위 도메인 값
- Decision: 우선순위는 high|medium|low 3단계로 고정한다.
- Rationale: 사용자 입력 단순화, 필터 규칙 명확화, 테스트 케이스 축소.
- Alternatives considered: 1~5 정수 (세분화 이점은 있으나 요구사항 대비 복잡도 증가), 자유 텍스트 (검증/일관성 저하).
