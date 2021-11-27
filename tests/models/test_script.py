from pytest import raises

from asking.exceptions import StageNotFoundError
from asking.loaders import DictionaryLoader
from asking.models import Script
from asking.state import State


def test_start__no_start() -> None:
    state = State({})
    script = Script(DictionaryLoader({}), state)
    with raises(StageNotFoundError):
        script.start()
