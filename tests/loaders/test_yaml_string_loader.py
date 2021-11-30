from asking.loaders import YamlStringLoader


def test() -> None:
    assert YamlStringLoader("start: []").load() == {
        "start": [],
    }
