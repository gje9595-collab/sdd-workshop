"""
입력 검증 헬퍼
"""

import re
from datetime import date as date_type
from todo_lib.errors import ValidationError

_TAG_PATTERN = re.compile(r"^[\w\-가-힣]{1,20}$")
_MAX_TAGS = 10


def validate_title(title: str) -> str:
    stripped = title.strip()
    if not stripped:
        raise ValidationError("제목은 필수 입력 항목입니다")
    return stripped


def validate_due_date(due: str) -> date_type:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due or ""):
        raise ValidationError("유효한 날짜 형식이 아닙니다: YYYY-MM-DD")
    try:
        return date_type.fromisoformat(due)
    except ValueError as exc:
        raise ValidationError("유효한 날짜 형식이 아닙니다: YYYY-MM-DD") from exc


def validate_priority(priority: str) -> str:
    allowed = {"high", "medium", "low"}
    if priority not in allowed:
        raise ValidationError("우선순위는 high|medium|low 중 하나여야 합니다")
    return priority


def validate_tags(tags: list[str] | None) -> list[str]:
    if not tags:
        return []

    if len(tags) > _MAX_TAGS:
        raise ValidationError(f"태그는 최대 {_MAX_TAGS}개까지 지정할 수 있습니다")

    normalized: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        clean = tag.strip().lower()
        if not clean:
            raise ValidationError("태그는 빈 문자열일 수 없습니다")
        if not _TAG_PATTERN.match(clean):
            raise ValidationError(
                f"태그 형식이 올바르지 않습니다: '{clean}' (영문·숫자·한글·-·_ 1~20자)"
            )
        if clean not in seen:
            seen.add(clean)
            normalized.append(clean)

    return normalized


def is_past_date(value: date_type) -> bool:
    return value < date_type.today()
