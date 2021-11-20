from logging import Logger, getLogger
from typing import IO, Any, Dict, List, Optional

from asking.actions import registered_actions
from asking.exceptions import Stop
from asking.state_protocol import StateProtocol
from asking.stop_reasons import InternalStopReason
from asking.types import StageKey


class State(StateProtocol):
    def __init__(self, out: IO[str]) -> None:
        self._out = out

    @property
    def logger(self) -> Logger:
        return getLogger("asking")

    @property
    def out(self) -> IO[str]:
        return self._out

    def perform_action(self, action_dict: Dict[str, Any]) -> Optional[StageKey]:
        self.logger.debug("Performing all known actions on: %s", action_dict)
        any_recognised = False
        for action_cls in registered_actions:
            action = action_cls(action=action_dict, state=self)
            result = action.perform()
            any_recognised = any_recognised or result.recognised
            if result.next:
                self.logger.debug("Action is redirecting to stage: %s", result.next)
                return result.next
        if any_recognised:
            self.logger.debug("Action did not direct to a next stage")
        else:
            self.logger.warning("ActionDict was unrecognised: %s", action_dict)
        return None

    def perform_actions(self, actions: List[Dict[str, Any]]) -> Optional[str]:
        for action_dict in actions:
            if next := self.perform_action(action_dict):
                return next
        self.logger.debug("No more actions: raising NO_MORE_ACTIONS")
        raise Stop(InternalStopReason.NO_MORE_ACTIONS)
