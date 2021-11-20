from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from asking.state_protocol import StateProtocol

from dataclasses import dataclass

@dataclass
class ActionResult:
    next: Optional[str]
    recognised: bool


class Action(ABC):
    def __init__(self, action: Dict[str, Any], state: StateProtocol) -> None:
        self._action = action
        self._state = state

    @abstractmethod
    def perform(self) -> ActionResult:
        pass

    @property
    def state(self) -> StateProtocol:
        return self._state
