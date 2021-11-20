from typing import Any, Optional
from asking.actions.action import Action, ActionResult
from asking.exceptions import Stop


class StopAction(Action):
    def perform(self) -> ActionResult:
        stop: Optional[Any] = self._action.get("stop", None)
        if stop is None:
            return ActionResult(next=None, recognised=False)
        self.state.logger.debug("Stopping with: %s", stop)
        raise Stop(stop)
