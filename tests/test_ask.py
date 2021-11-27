from asking import ask
from asking.loaders import DictionaryLoader
from asking.state import State


def test() -> None:
    loader = DictionaryLoader({"start": [{"stop": "foo"}]})
    state = State({})
    assert ask(loader, state) == "foo"
