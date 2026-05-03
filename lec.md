제일먼저 constitution 파일을 먼저 작성한다.
agent: speckit.constitution를 프롬프트로 부르면
agent가 실행

---
## SDD 워크샵 흐름 도식화
학습자는 아래와 같은 흐름으로 '생각의 구조화'에서 '기술적 구현'으로 이행함.
- Definition (Constitution): 프로젝트의 흔들리지 않는 원칙 수립.
- Structuring (Specify): 디자인 토큰 및 요구사항 정의.
- Refinement (Clarify): 모호함 제거 및 기술적 제약 사항 검토.
- Automation (Spec Kit): 정의된 명세를 실제 폴더 구조(.specify)에 녹여내고 자동화 준비.

---
### speckit.constitution
- 프로젝트 헌법 관리: .specify/memory/constitution.md 파일을 프로젝트의 핵심 원칙과 거버넌스(운영 규칙)를 담은 최신 상태로 유지함.
- 동기화 보장: 헌법 내용이 변경될 때, 이와 연결된 다른 템플릿(Plan, Spec, Tasks 등)들도 일관성을 유지하도록 자동으로 전파하고 검증함.
- [포함내용]
    - 사전 체크 (Hooks)	업데이트 시작 전, 설정된 확장 도구(.specify/extensions.yml)나 자동 명령이 있는지 확인하고 실행함.
    - 데이터 수집 및 분석	기존 헌법 파일 로드, 사용자 입력값 반영, README 등 주변 문맥을 통해 [PLACEHOLDER] 값들을 채움.
    - 버전 관리 (SemVer)	변경 수준에 따라 버전 번호를 갱신함 (MAJOR: 중대 변경, MINOR: 원칙 추가, PATCH: 단순 수정).
    - 본문 작성	모든 플레이스홀더를 실제 값으로 교체하고, '원칙(Principle)'과 '거버넌스(Governance)' 섹션을 명확히 기술함.
    - 일관성 전파	수정된 원칙이 다른 설계 템플릿(Plan, Spec, Tasks)의 규칙과 충돌하지 않는지 확인하고 동기화함.
    - 결과 보고 및 검증	변경 사항 리포트(Sync Impact Report)를 작성하고, 날짜 형식(ISO) 및 누락된 항목이 없는지 최종 검증함.
    - 사후 체크 (Hooks)	업데이트 완료 후 실행해야 할 자동화 작업이 있는지 확인하고 호출함.

---
### speckit.specify.prompt.md



수정이 이루어질때는 task만 변경하는것이 좋다.