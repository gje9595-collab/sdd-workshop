"""T002/T009/T015: 서비스 태그 저장/조회 테스트"""

import pytest
from todo_lib.errors import ValidationError


def test_add_todo_saves_tags(service):
    item, warning = service.add_todo("회의 준비", tags=["업무", "중요"])
    assert warning is False
    assert item.tags == ["업무", "중요"]


def test_add_todo_without_tags_keeps_existing_flow(service):
    item, _ = service.add_todo("태그 없는 항목")
    assert item.title == "태그 없는 항목"
    assert item.tags is None


def test_add_todo_rejects_invalid_tags(service):
    with pytest.raises(ValidationError):
        service.add_todo("잘못된 태그", tags=["bad tag"])


def test_list_todos_filters_by_tag(service):
    service.add_todo("업무1", tags=["업무"])
    service.add_todo("개인1", tags=["개인"])
    items = service.list_todos(tag="업무")
    assert len(items) == 1
    assert items[0].title == "업무1"


def test_list_todos_applies_intersection_with_existing_filters(service):
    a, _ = service.add_todo("high 업무", priority="high", tags=["업무"])
    b, _ = service.add_todo("high 개인", priority="high", tags=["개인"])
    service.mark_done(b.id)

    items = service.list_todos(filter_status="pending", priority="high", tag="업무")
    assert len(items) == 1
    assert items[0].id == a.id
