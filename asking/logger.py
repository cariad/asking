class LogMessage:
    def __init__(self, cls: type) -> None:
        self._cls = cls

    def debug(self, msg: str) -> str:
        return f"{self._cls.__class__} -> {msg}"
