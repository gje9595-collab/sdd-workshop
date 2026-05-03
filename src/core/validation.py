from __future__ import annotations

from datetime import date

from src.core.models import PriorityEnum, StatusEnum


def validate_title(title: str) -> str:
    normalized = title.strip()
    if not normalized:
        raise ValueError("error: title is required")
    return normalized


def parse_due_date(due: str | None) -> date | None:
    if due is None:
        return None
    try:
        return date.fromisoformat(due)
    except ValueError as exc:
        raise ValueError("error: due must be YYYY-MM-DD") from exc


def parse_priority(priority: str | None) -> PriorityEnum | None:
    if priority is None:
        return None
    try:
        return PriorityEnum(priority)
    except ValueError as exc:
        raise ValueError("error: priority must be one of high|medium|low") from exc


def parse_status_filter(value: str | None) -> StatusEnum | None:
    if value is None:
        return None
    try:
        return StatusEnum(value)
    except ValueError as exc:
        raise ValueError("error: filter must be one of done|pending") from exc


def validate_item_id(item_id: int) -> int:
    if item_id <= 0:
        raise ValueError("error: id must be a positive integer")
    return item_id
