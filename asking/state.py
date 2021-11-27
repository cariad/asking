from logging import Logger, getLogger
from sys import stdout
from typing import IO, Any, Dict, List, Optional

from asking.actions import registered_actions
from asking.exceptions import NothingToDoError, Stop
from asking.protocols import StateProtocol
from asking.stop_reasons import InternalStopReason
from asking.types import Responses, StageKey


class State(StateProtocol):
    """
    Script state.

    Arguments:
        responses:  Dictionary of previous and updated responses
        references: Values referencable during the script
        out:        Output writer (defaults to stdout)
    """

    def __init__(
        self,
        responses: Responses,
        references: Optional[Dict[str, str]] = None,
        out: Optional[IO[str]] = None,
    ) -> None:
        self._out = out or stdout
        self._references = references or {}
        self._responses = responses

    @property
    def logger(self) -> Logger:
        return getLogger("asking")

    @property
    def out(self) -> IO[str]:
        return self._out

    @property
    def references(self) -> Dict[str, str]:
        return self._references

    def perform_action(self, action_dict: Dict[str, Any]) -> Optional[StageKey]:
        self.logger.debug("Performing all known actions on: %s", action_dict)
        any_recognised = False
        for action_cls in registered_actions:
            action = action_cls(action=action_dict, state=self)
            try:
                result = action.perform()
                any_recognised = True
                if result.next:
                    self.logger.debug("Action is redirecting to stage: %s", result.next)
                    return result.next
            except NothingToDoError:
                pass
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

    @property
    def responses(self) -> Dict[Any, Any]:
        return self._responses

    def save_response(
        self,
        key: str,
        value: str,
        responses: Optional[Responses] = None,
    ) -> None:
        logger = getLogger("asking")

        responses = self._responses if responses is None else responses
        logger.debug("Saving a value for key %s in response %s", key, responses)

        if "." not in key:
            responses[key] = value
            return

        key_parts = key.split(".")
        sub_key = key_parts[0]

        if sub_key in responses:
            if not isinstance(responses[sub_key], dict):
                raise Exception("conflict")
        else:
            logger.debug("Creating sub_key %s subdictionary in %s", sub_key, responses)
            responses[sub_key] = {}

        subdictionary = responses[sub_key]

        self.save_response(
            key=".".join(key_parts[1:]),
            value=value,
            responses=subdictionary,
        )

    def get_response(
        self,
        key: str,
        responses: Optional[Responses] = None,
    ) -> Optional[str]:
        # logger = getLogger("asking")

        responses = self._responses if responses is None else responses
        # logger.debug("Saving a value for key %s in response %s", key, responses)

        if "." not in key:
            value = responses.get(key, None)
            return None if not value else str(value)

        key_parts = key.split(".")
        sub_key = key_parts[0]

        if sub_key in responses:
            if not isinstance(responses[sub_key], dict):
                raise Exception("conflict")
        else:
            return None
            # logger.debug("Creating sub_key %s subdictionary in %s", sub_key, responses)
            # responses[sub_key] = {}

        subdictionary = responses[sub_key]

        return self.get_response(
            key=".".join(key_parts[1:]),
            responses=subdictionary,
        )
