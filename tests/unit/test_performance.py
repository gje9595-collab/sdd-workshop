from __future__ import annotations

from time import perf_counter

from src.core.service import ToDoService


def test_list_and_filter_under_two_seconds_with_200_items(repository) -> None:
    service = ToDoService(repository)

    for idx in range(200):
        priority = "high" if idx % 2 == 0 else "low"
        created = service.add_todo(title=f"todo-{idx}", priority=priority)
        if idx % 3 == 0:
            service.done_todo(created.item_id)

    start = perf_counter()
    list_result, all_items = service.list_todos()
    done_result, done_items = service.list_todos(status_filter="done")
    high_result, high_items = service.list_todos(priority="high")
    elapsed = perf_counter() - start

    assert list_result.success is True
    assert done_result.success is True
    assert high_result.success is True
    assert len(all_items) == 200
    assert len(done_items) > 0
    assert len(high_items) > 0
    assert elapsed < 2.0
