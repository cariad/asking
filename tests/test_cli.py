from asking.cli import AskingCLI
from asking.tasks import PerformTask


def test() -> None:
    cli = AskingCLI(args=["foo.yml"])
    assert isinstance(cli.task, PerformTask)
