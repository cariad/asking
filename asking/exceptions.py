from typing import Any


class AskingError(Exception):
    pass


class StageError(AskingError):
    def __init__(self, key: str, msg: str) -> None:
        super().__init__(f'"{key}" stage: {msg}')


class StageNotFoundError(StageError):
    def __init__(self, key: str) -> None:
        super().__init__(key, "not found")


class MissingGotoError(StageError):
    def __init__(self, key: str) -> None:
        super().__init__(key, "no goto")


class MissingKeyError(AskingError):
    def __init__(self, ex: KeyError, obj: Any) -> None:
        super().__init__(f"missing {ex} in: {repr(obj)}")


class KeyTypeError(AskingError):
    def __init__(self, key: str, expected: type, obj: Any) -> None:
        super().__init__(f'expected "{key}" to be {expected} in: {repr(obj)}')
