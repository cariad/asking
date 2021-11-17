from typing import Iterable, List, Optional, TypedDict
from asking.models.branch import Branch, BranchDict
from asking.models.runtime import Runtime
from asking.models.performance import Performance
from asking.exceptions import KeyTypeError, MissingKeyError
from logging import getLogger

AskDict = TypedDict(
    "AskDict",
    {
        "if": List[BranchDict],
        "question": str,
    },
    total=False,
)


class Ask:
    def __init__(self, ask: AskDict, run: Runtime) -> None:
        self._ask = ask
        self._run = run

    @property
    def question(self) -> str:
        try:
            return str(self._ask["question"])
        except KeyError as ex:
            raise MissingKeyError(ex, self._ask)

    def render_question(self) -> None:
        log = getLogger("asking")
        log.debug("rendering question")
        self._run.out.write("\n")
        self._run.out.write("question: ")
        self._run.out.write(self.question)
        self._run.out.write("\n")

    def read(self) -> str:
        return input("\n> ")

    @property
    def branches(self) -> Iterable[Branch]:
        try:
            branches = self._ask["if"]
        except KeyError as ex:
            raise MissingKeyError(ex, self._ask)

        if not isinstance(branches, list):  # pyright: reportUnnecessaryIsInstance=false
            raise KeyTypeError("if", list, self._ask)

        for branch in branches:
            yield Branch(branch=branch, run=self._run)

    def perform(self) -> Optional[Performance]:
        self.render_question()
        response = self.read()

        log = getLogger("asking")
        log.debug('Looking for a branch interested in response "%s"', response)
        for branch in self.branches:
            if performance := branch.perform(response):
                log.debug('Branch "%s" was interested in response "%s"', branch, response)
                return performance

        log.debug('No branches were interested in response "%s"', response)
        return None
