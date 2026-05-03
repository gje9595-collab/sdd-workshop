# Implementation Plan: CLI ToDo Manager

**Branch**: `003-cli-todo-manager` | **Date**: 2026-05-03 | **Spec**: `/specs/003-cli-todo-manager/spec.md`
**Input**: Feature specification from `/specs/003-cli-todo-manager/spec.md`

## Summary

터미널 기반 ToDo 관리 CLI를 Python 3.12 + uv 환경에서 구현한다. 비즈니스 로직은 `src/core/`에 독립 배치하고, `src/cli/`는 명령 파싱과 출력만 담당한다. 데이터 저장은 로컬 SQLite 파일을 사용하며, TDD 원칙에 따라 `pytest`/`pytest-cov`로 실패 테스트를 먼저 작성한 뒤 구현한다.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: typer, sqlalchemy  
**Storage**: SQLite (로컬 파일 기반)  
**Testing**: pytest, pytest-cov  
**Target Platform**: 로컬 개발 환경(Windows/macOS/Linux) 터미널  
**Project Type**: CLI 애플리케이션  
**Performance Goals**: 200개 항목 기준 목록/필터 조회 2초 이내  
**Constraints**: REST API/GUI 제외, 불필요한 추상 인터페이스 금지, 지정 의존성 외 추가 금지  
**Scale/Scope**: 단일 사용자 로컬 ToDo 관리, 핵심 명령 4종(add/list/done/delete)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gate

- [x] Gate 1: 비즈니스 로직과 입출력 계층 분리 설계 반영 (`src/core/` vs `src/cli/`, `src/adapters/`)
- [x] Gate 2: 사용자 스토리별 실패 테스트 선행 계획 존재 (`tests/` 선작성)
- [x] Gate 3: 의존성 필요성/대안/리스크 검토 근거 존재 (research.md에 기록)
- [x] Gate 4: 불필요한 추상화 배제 (ITodoRepository 등 인터페이스 미도입)
- [x] Gate 5: CLI 범위 고정, REST API/GUI 제외

### Post-Design Gate (Phase 1 Re-check)

- [x] Gate 1: 데이터 모델과 명령 계약이 레이어 분리를 유지한다.
- [x] Gate 2: quickstart에 테스트 우선 절차가 포함되었다.
- [x] Gate 3: 허용 의존성(typer, sqlalchemy, pytest, pytest-cov)만 사용한다.
- [x] Gate 4: 계약/모델이 단순 함수·클래스 중심으로 설계되었다.
- [x] Gate 5: 계약 문서가 CLI 명령 인터페이스만 정의한다.

## Project Structure

### Documentation (this feature)

```text
specs/003-cli-todo-manager/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── core/
│   ├── __init__.py
│   ├── models.py
│   ├── repository.py
│   ├── service.py
│   └── validation.py
├── cli/
│   ├── __init__.py
│   ├── app.py
│   └── formatters.py
└── adapters/          # 현재 미사용; 외부 연동 어댑터 확장 예약 계층
    └── __init__.py

tests/
├── unit/
│   ├── test_add_todo.py
│   ├── test_list_todo.py
│   ├── test_done_todo.py
│   └── test_delete_todo.py
└── integration/
    └── test_cli_commands.py
```

**Structure Decision**: 비즈니스 규칙과 데이터 접근은 `src/core/`에 집중시키고, `src/cli/`는 Typer 커맨드 및 출력 포맷만 담당한다. `src/adapters/`는 현재 기능 범위에서 사용하지 않으나 헌법 레이어 원칙에 따라 예약한다. 테스트는 사용자 스토리 단위로 실패 케이스부터 작성한다.

## Phase Plan

### Phase 0 - Research

- 저장소 선택: SQLite 파일 DB 사용 기준 확정
- ORM 선택: SQLAlchemy의 최소 기능(모델/세션/CRUD)만 사용
- CLI 프레임워크: Typer 명령 구조 및 인자 검증 패턴 확정
- 테스트 전략: pytest + pytest-cov로 스토리 기반 Red-Green-Refactor 흐름 확정

### Phase 1 - Design

- 데이터 모델 정의: ToDoItem, FilterCriteria, CommandResult
- 계약 정의: add/list/done/delete 명령 시그니처와 출력/오류 규칙
- 빠른 시작 가이드 작성: uv 환경 생성, 의존성 설치, 테스트/실행 명령 정리

### Phase 2 - Task Planning (for `/speckit.tasks`)

- 사용자 스토리 순서(P1 → P2 → P3)로 테스트/구현 작업 분해
- 각 스토리마다 테스트 선행 태스크를 구현 태스크보다 먼저 배치

## Complexity Tracking

헌법 위반 없음. 복잡성 예외 승인 불필요.
