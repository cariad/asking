from logging import Logger
from typing import IO, Any, Dict, List, Optional, Protocol


class StateProtocol(Protocol):
    @property
    def logger(self) -> Logger:
        """..."""

    @property
    def out(self) -> IO[str]:
        """..."""

    def perform_actions(self, actions: List[Dict[str, Any]]) -> Optional[str]:
        """..."""

    @property
    def responses(self) -> Dict[Any, Any]:
        ...

    def get_response(self, key: str) -> Optional[str]:
        ...

    def save_response(self, key: str, value: str) -> None:
        ...

    @property
    def references(self) -> Dict[str, str]:
        ...
