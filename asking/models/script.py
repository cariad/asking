import re
from logging import getLogger
from pathlib import Path
from sys import stdout
from typing import IO, Any, Dict, cast

from ruamel.yaml.main import YAML

from asking.exceptions import StageNotFoundError, Stop
from asking.models.stage import Stage
from asking.state import State
from asking.types import StageType, StopReason

ScriptType = Dict[str, StageType]


class Script:
    def __init__(self, script: ScriptType, out: IO[str]) -> None:
        self._state = State(out=out)
        self._script = script

    @staticmethod
    def deserialize_yaml_file(path: Path) -> ScriptType:
        yaml = YAML(typ="safe")
        with open(path, "r") as f:
            loaded: Any = yaml.load(f)  # pyright: reportUnknownMemberType=false
        return cast(ScriptType, loaded)

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
        return Script(script=script, out=stdout)

    def get(self, key: str) -> Stage:
        stage = self._script.get(key, None)
        if not stage:
            raise StageNotFoundError(key)
        return Stage(stage=stage, state=self._state)

    def start(self) -> StopReason:
        stage = self.get("start")

        try:
            while True:
                next = stage.perform()
                stage = self.get(next)
        except Stop as ex:
            return ex.reason
