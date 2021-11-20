from typing import Any, Optional

from asking.actions.action import Action, ActionResult
from asking.exceptions import NothingToDoError


class GotoAction(Action):
    def perform(self) -> ActionResult:
        raw: Optional[Any] = self._action.get("goto", None)

        if raw is None:
            raise NothingToDoError()

        goto = None if raw is None else str(raw)
        if goto is not None:
            self.state.logger.debug("goto: %s", goto)

        return ActionResult(next=goto)
