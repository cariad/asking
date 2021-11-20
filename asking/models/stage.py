from asking.exceptions import Stop
from asking.protocols import StateProtocol
from asking.stop_reasons import InternalStopReason
from asking.types import StageType


class Stage:
    def __init__(self, stage: StageType, state: StateProtocol) -> None:
        self._stage = stage
        self._state = state

    def perform(self) -> str:
        if next := self._state.perform_actions(self._stage):
            self._state.logger.debug("next stage: %s", next)
            return next
        self._state.logger.debug("No more stages: raising NO_NEXT_STAGE")
        raise Stop(InternalStopReason.NO_NEXT_STAGE)
