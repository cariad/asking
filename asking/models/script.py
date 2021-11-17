from typing import Dict, Optional, cast
from asking.models.performance import Performance
from asking.models.stage import StageType, Stage
from pathlib import Path
import re
from yaml import safe_load
from logging import getLogger
from asking.exceptions import AskingError, StageNotFoundError
from asking.models.runtime import Runtime
from sys import stdout

from asking.types import StopType

ScriptType = Dict[str, StageType]


class Script:
    def __init__(self, script: ScriptType, run: Runtime) -> None:
        self._run = run
        self._script = script

    @staticmethod
    def deserialize_yaml_file(path: Path) -> ScriptType:
        with open(path, "r") as f:
            return cast(ScriptType, safe_load(f))

    @staticmethod
    def is_yaml_filename(filename: str) -> bool:
        log = getLogger("asking")
        log.debug("checking if %s is a YAML file", filename)
        yes = not not re.match(r"^.*\.y(a?)ml$", filename, re.IGNORECASE)
        log.debug("%s is %sa YAML file", filename, "" if yes else "not ")
        return yes

    @classmethod
    def load_file(cls, path: Path) -> "Script":
        if Script.is_yaml_filename(path.name):
            script = Script.deserialize_yaml_file(path)
        else:
            raise Exception("unknown file type")
        return Script(script=script, run=Runtime(out=stdout))

    def get(self, key: str) -> Stage:
        stage = self._script.get(key, None)
        if not stage:
            raise StageNotFoundError(key)
        return Stage(stage=stage, run=self._run)

    def start(self) -> StopType:
        stage = self.get("start")
        performance: Optional[Performance] = None

        while not performance or performance.stop is None:
            performance = stage.next()
            if not performance:
                raise AskingError("unexpected stop")
            if performance.stop:
                return performance.stop
            if not performance.next:
                raise AskingError("no next")
            stage = self.get(performance.next)
