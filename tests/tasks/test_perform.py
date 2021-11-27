from io import StringIO
from logging import basicConfig, getLogger
from pathlib import Path

from cline import CommandLineArguments

from asking.tasks.perform import PerformTask, PerformTaskArguments

basicConfig(level="DEBUG")
getLogger("asking").setLevel("DEBUG")


def test_make_args() -> None:
    args = CommandLineArguments({"path": "."})
    assert PerformTask.make_args(args) == PerformTaskArguments(path=Path("."))


def test_invoke() -> None:
    args = PerformTaskArguments(
        directions={
            "ready": "y",
            "user.name": "bobby",
            "user.smell": "star wars",
            "save": "y",
        },
        path=Path(".") / "sample.asking.yml",
        responses={},
    )

    out = StringIO()
    task = PerformTask(args, out)
    exit_code = task.invoke()

    assert args.responses == {}
    assert exit_code == 0
