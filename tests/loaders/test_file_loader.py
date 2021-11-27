from pathlib import Path

from pytest import raises

from asking.loaders import FileLoader

# def test() -> None:
#     loader = FileLoader(Path() / "tests" / "loaders" / "test.asking.yml")
#     assert loader.load() == {
#         "start": [],
#     }


def test__not_yaml() -> None:
    loader = FileLoader(Path("foo.json"))
    with raises(Exception):
        loader.load()
