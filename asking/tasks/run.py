from dataclasses import dataclass

from cline import CommandLineArguments, Task
from asking.models import Script
from pathlib import Path


@dataclass
class RunTaskArguments:
    path: Path


class RunTask(Task[RunTaskArguments]):
    @classmethod
    def make_task_args(cls, args: CommandLineArguments) -> RunTaskArguments:
        return RunTaskArguments(
            path=Path(args.get_string("path")),
        )

    def invoke(self) -> int:
        script = Script.load_file(self.args.path)
        script.start()
        return 0
