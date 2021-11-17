from typing import IO


class Runtime:
    def __init__(self, out: IO[str]) -> None:
        self._out = out

    @property
    def out(self) -> IO[str]:
        return self._out
