from logging import getLogger
from typing import Iterable, List, Optional, TypedDict
from asking.models.non_branching_action import NonBranchingActionDict,NonBranchingAction
from asking.models.response_condition import ResponseCondition, ResponseConditionDict
from asking.models.performance import Performance
from asking.exceptions import MissingKeyError,KeyTypeError
from asking.models.runtime import Runtime
from asking.logger import LogMessage

BranchDict = TypedDict(
    "BranchDict",
    {
        "response": List[Optional[ResponseConditionDict]],
        "then": List[NonBranchingActionDict],
    },
    total=False,
)

class Branch:
    def __init__(self, branch: BranchDict, run: Runtime) -> None:
        self._branch = branch
        self._lm = LogMessage(self.__class__)
        self._run = run

    @property
    def response_conditions(self) -> Iterable[Optional[ResponseCondition]]:
        try:
            response_conditions = self._branch["response"]
        except KeyError as ex:
            raise MissingKeyError(ex, self._branch)

        if not isinstance(response_conditions, list):  # pyright: reportUnnecessaryIsInstance=false
            raise KeyTypeError("if", list, self._branch)

        for response_condition in response_conditions:
            if response_condition:
                yield ResponseCondition(response_condition)
            else:
                yield None

    @property
    def non_branching_actions(self) -> Iterable[NonBranchingAction]:
        log = getLogger("asking")

        try:
            non_branching_actions = self._branch["then"]
        except KeyError as ex:
            raise MissingKeyError(ex, self._branch)

        if not isinstance(non_branching_actions, list):  # pyright: reportUnnecessaryIsInstance=false
            raise KeyTypeError("then", list, self._branch)

        for non_branching_action in non_branching_actions:
            log.debug("Yielding NonBranchingAction with: %s", non_branching_action)
            yield NonBranchingAction(non_branching_action=non_branching_action, run=self._run,)

    def pass_any(self, response: str) -> bool:
        for response_condition in self.response_conditions:
            if response_condition:
                if response_condition.pass_any(response):
                    return True
            elif not response:
                return True
        return False

    def perform(self, response: str) -> Optional[Performance]:
        if self.pass_any(response):
            for non_branching_action in self.non_branching_actions:
                if performance := non_branching_action.perform():
                    return performance
        return None
