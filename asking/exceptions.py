from typing import Any

from asking.types import StopReason


class Stop(Exception):
    def __init__(self, reason: StopReason) -> None:
        self._reason = reason
        super().__init__(repr(reason))

    @property
    def reason(self) -> StopReason:
        return self._reason


class AskingError(Exception):
    pass


class NothingToDoError(AskingError):
    def __init__(self) -> None:
        super().__init__("nothing to do")


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
