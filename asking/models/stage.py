from typing import Iterable, List, Optional
from asking.models.action import Action, ActionDict
from asking.models.performance import Performance
from asking.models.runtime import Runtime

StageType = List[ActionDict]


class Stage:
    def __init__(self, stage: StageType, run: Runtime) -> None:
        self._run = run
        self._stage = stage

    def actions(self) -> Iterable[Action]:
        for action in self._stage:
            yield Action(action=action, run=self._run)

    def next(self) -> Optional[Performance]:
        for action in self.actions():
            if performance := action.perform():
                return performance
        return None
