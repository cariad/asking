from typing import IO, Any, Dict, List, Optional, Protocol
from logging import Logger

class StateProtocol(Protocol):
    @property
    def logger(self) -> Logger:
        """..."""

    @property
    def out(self) -> IO[str]:
        """..."""

    def perform_actions(self, actions: List[Dict[str, Any]]) -> Optional[str]:
        """..."""
