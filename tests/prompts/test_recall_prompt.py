from asking.actions import AskAction
from asking.prompts.recall_prompt import RecallPromptBuilder
from asking.state import State


def test_prompt__no_recall() -> None:
    ask = AskAction({"ask": {"recall": False}}, State({}))
    builder = RecallPromptBuilder(ask)
    assert builder.prompt is None


def test_prompt__no_key() -> None:
    ask = AskAction({"ask": {"recall": True}}, State({}))
    builder = RecallPromptBuilder(ask)
    assert builder.prompt is None


def test_prompt__no_value() -> None:
    ask = AskAction({"ask": {"key": "foo", "recall": True}}, State({}))
    builder = RecallPromptBuilder(ask)
    assert builder.prompt == ""


def test_prompt() -> None:
    ask = AskAction({"ask": {"key": "foo", "recall": True}}, State({"foo": "bar"}))
    builder = RecallPromptBuilder(ask)
    assert builder.prompt == "default: bar"
