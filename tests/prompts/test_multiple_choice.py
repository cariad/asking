from asking.actions import AskAction
from asking.prompts.prompt import MultipleChoicePromptBuilder
from asking.state import State


def test_prompt__default_after_value() -> None:
    ask = AskAction(
        {
            "ask": {"branches": [{"response": ["y", ""]}]},
        },
        State({}),
    )
    builder = MultipleChoicePromptBuilder(ask)
    assert builder.prompt == "Y"


def test_prompt__default_before_value() -> None:
    ask = AskAction(
        {
            "ask": {"branches": [{"response": ["", "y"]}]},
        },
        State({}),
    )
    builder = MultipleChoicePromptBuilder(ask)
    assert builder.prompt == "Y"
