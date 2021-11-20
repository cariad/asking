from typing import List, Type

from asking.actions.action import Action
from asking.actions.ask import AskAction
from asking.actions.text import TextAction
from asking.actions.title import TitleAction
from asking.actions.stop import StopAction
from asking.actions.goto import GotoAction

registered_actions: List[Type[Action]] = [
    TitleAction,
    TextAction,
    AskAction,
    GotoAction,
    StopAction,
]

"""In execution order."""

__all__ = [
    "AskAction",
    "GotoAction",
    "StopAction",
    "TextAction",
    "TitleAction",
]
