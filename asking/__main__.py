from asking.cli import AskingCLI
from asking import __version__


def entry() -> None:
    AskingCLI.invoke_and_exit(log_level="DEBUG", version=__version__)


if __name__ == "__main__":
    entry()
