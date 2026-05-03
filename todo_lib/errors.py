"""
서비스 레벨 예외 클래스
"""


class ToDoError(Exception):
    """ToDo 앱 기본 예외"""


class ValidationError(ToDoError):
    """사용자 입력 오류"""


class ItemNotFoundError(ToDoError):
    """존재하지 않는 항목 ID 오류"""

    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"항목 {item_id}를 찾을 수 없습니다")


class AlreadyDoneError(ToDoError):
    """이미 완료된 항목 오류"""

    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"항목 {item_id}는 이미 완료된 항목입니다")


class DatabaseError(ToDoError):
    """DB 접근/처리 오류"""
