from asking.actions import TextAction
from asking.state import State


def test_get_string__missed_reference() -> None:

    state = State({})
    action = TextAction(
        action={"text": "{foo}"},
        state=state,
    )

    assert action.get_string("text") == "{foo}"
