from asking.loaders import YamlResourceLoader


def test() -> None:
    loader = YamlResourceLoader(__package__, "test.asking.yml")
    assert loader.load() == {
        "start": [],
    }
