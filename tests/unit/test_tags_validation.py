"""T001/T006: 태그 검증 단위 테스트"""

import pytest
from todo_lib.errors import ValidationError
from todo_lib.validation import validate_tags


def test_validate_tags_empty_returns_empty_list():
    assert validate_tags([]) == []


def test_validate_tags_none_returns_empty_list():
    assert validate_tags(None) == []


def test_validate_tags_normalizes_and_deduplicates():
    assert validate_tags([" Work ", "work", "중요"]) == ["work", "중요"]


def test_validate_tags_rejects_blank_tag():
    with pytest.raises(ValidationError, match="빈 문자열"):
        validate_tags([" "])


def test_validate_tags_rejects_invalid_characters():
    with pytest.raises(ValidationError, match="태그 형식이 올바르지 않습니다"):
        validate_tags(["bad tag"])  # 공백 포함


def test_validate_tags_rejects_too_many_tags():
    too_many = [f"t{i}" for i in range(11)]
    with pytest.raises(ValidationError, match="최대"):
        validate_tags(too_many)
