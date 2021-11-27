from pytest import raises

from asking.exceptions import Stop
from asking.state import State


def test_get_response__sub_key_not_dict() -> None:
    state = State({"foo": "war"})
    with raises(TypeError):
        state.get_response(
            key="foo.bar",
        )


def test_perform_action__none_recognised() -> None:
    state = State({})
    action = {"pringles": "ouch"}
    assert state.perform_action(action) is None


def test_perform_actions__no_more() -> None:
    with raises(Stop):
        State({}).perform_actions([])


def test_save_response__sub_key_not_dict() -> None:
    state = State({"foo": "war"})
    with raises(TypeError):
        state.save_response(
            key="foo.bar",
            value="woo",
        )
