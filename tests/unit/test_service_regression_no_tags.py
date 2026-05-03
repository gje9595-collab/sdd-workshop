"""T022: 서비스 회귀 테스트(태그 미사용 경로)"""


def test_service_add_without_tags_defaults_compatible(service):
    item, warning = service.add_todo("기존 add")
    assert warning is False
    assert item.tags is None


def test_service_done_delete_flow_compatible(service):
    item, _ = service.add_todo("기존 done/delete")
    done_item = service.mark_done(item.id)
    assert done_item.is_done is True

    service.delete_todo(item.id)
    items = service.list_todos()
    assert all(i.id != item.id for i in items)
