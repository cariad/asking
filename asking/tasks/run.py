from dataclasses import dataclass
from getpass import getuser
from json import dumps
from pathlib import Path

from cline import CommandLineArguments, Task

from asking.loaders.file_loader import FileLoader
from asking.models import Script
from asking.state import State
from asking.types import Responses


@dataclass
class RunTaskArguments:
    path: Path


class RunTask(Task[RunTaskArguments]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> RunTaskArguments:
        return RunTaskArguments(
            path=Path(args.get_string("path")),
        )

    def invoke(self) -> int:
        responses: Responses = {
            "user": {
                "name": getuser(),
            }
        }
        state = State(responses)

        script = Script(
            loader=FileLoader(self.args.path),
            state=state,
        )

        stop_reason = script.start()

        self.out.write("Stopped with reason: ")
        self.out.write(str(stop_reason))
        self.out.write("\n")
        self.out.write("Stopped with responses: ")
        self.out.write(dumps(responses, indent=2, sort_keys=True))
        self.out.write("\n")

        return 0
