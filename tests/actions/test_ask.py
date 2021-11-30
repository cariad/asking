from pytest import raises

from asking import State
from asking.actions import ActionResult, AskAction
from asking.exceptions import AskingError


def test() -> None:
    state = State({}, directions={"k": "n"})
    action = AskAction(
        action={
            "ask": {
                "question": "?",
                "key": "k",
                "branches": [
                    {
                        "response": "y",
                        "then": [{"goto": "foo"}],
                    },
                    {
                        "response": "n",
                        "then": [{"goto": "bar"}],
                    },
                ],
            }
        },
        state=state,
    )

    assert action.perform() == ActionResult(next="bar")


def test_branch__no_branches() -> None:
    state = State({}, directions={"k": "n"})
    action = AskAction(
        action={
            "ask": {
                "question": "?",
                "key": "k",
            }
        },
        state=state,
    )

    with raises(AskingError):
        action.perform()


def test_branch__no_response() -> None:
    state = State({}, directions={"k": "n"})
    action = AskAction(
        action={
            "ask": {
                "question": "?",
                "key": "k",
                "branches": [
                    {},
                ],
            }
        },
        state=state,
    )

    with raises(AskingError):
        action.perform()


def test_branch__no_then() -> None:
    state = State({}, directions={"k": "n"})
    action = AskAction(
        action={
            "ask": {
                "question": "?",
                "key": "k",
                "branches": [
                    {"response": "n"},
                ],
            }
        },
        state=state,
    )

    with raises(AskingError):
        action.perform()


def test_natch_empty() -> None:
    state = State({}, directions={"k": ""})
    action = AskAction(
        action={
            "ask": {
                "question": "?",
                "key": "k",
                "branches": [
                    {
                        "response": "",
                        "then": [{"goto": "foo"}],
                    },
                    {
                        "response": "n",
                        "then": [{"goto": "bar"}],
                    },
                ],
            }
        },
        state=state,
    )

    assert action.perform() == ActionResult(next="foo")


def test__uses_previous_value() -> None:
    responses = {"k": "war"}
    state = State(responses, directions={"k": ""})
    action = AskAction(
        action={
            "ask": {
                "question": "?",
                "recall": True,
                "key": "k",
                "branches": [
                    {
                        "response": "^.+$",
                        "then": [{"goto": "soup"}],
                    },
                ],
            }
        },
        state=state,
    )

    action.perform()
    assert responses == {"k": "war"}
