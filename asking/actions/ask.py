import re
from typing import Any, Dict, List, Optional, Union

from ansiscape import bright_green

from asking.actions.action import Action, ActionResult
from asking.state_protocol import StateProtocol
from asking.exceptions import AskingError


class Branch:
    def __init__(self, branch: Dict[str, Any], state: StateProtocol) -> None:
        self._branch = branch
        self._state = state

    @property
    def response(self) -> List[str]:
        response: Union[None, Any, List[Any]] = self._branch.get("response", None)
        if response is None:
            raise AskingError("no response key")

        if isinstance(response, list):
            return ["" if r is None else str(r) for r in response]

        return ["" if response is None else str(response)]

    def matches_response(self, value: str) -> bool:
        for response in self.response:
            if response == "" and response == value:
                return True

            if not response.startswith("^"):
                response = f"^{response}"

            if not response.endswith("$"):
                response = f"{response}$"

            if re.match(response, value):
                self._state.logger.debug('value "%s" matches "%s"', value, response)
                return True
            self._state.logger.debug('value "%s" does not match "%s"', value, response)

        return False

    def perform_actions(self) -> Optional[str]:
        actions: Union[None, Any, List[Dict[str, Any]]] = self._branch.get("then", None)
        if not isinstance(actions, list):
            raise AskingError("no then")
        return self._state.perform_actions(actions)


class AskAction(Action):
    def perform(self) -> ActionResult:
        try:
            ask = self._action["ask"]
        except KeyError:
            return ActionResult(next=None, recognised=False)

        question = ask.get("question", None)
        if question:
            self.state.out.write("\n")
            self.state.out.write(bright_green(question).encoded)
            self.state.out.write("\n")

        branches: Union[None, Any, List[Dict[str, Any]]] = ask.get("branches", None)
        if not isinstance(branches, list):
            raise AskingError("no branches")

        next: Optional[str] = None

        while next is None:
            response = input("\n> ")

            for branch_dict in branches:
                branch = Branch(branch=branch_dict, state=self.state)
                if branch.matches_response(response):
                    next = branch.perform_actions()

        return ActionResult(next=next, recognised=True)
