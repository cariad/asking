from typing import List, Protocol


class BranchProtocol(Protocol):
    @property
    def response(self) -> List[str]:
        ...

    def is_regex(self, value: str) -> bool:
        ...
