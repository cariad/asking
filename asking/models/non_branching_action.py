# from logging import getLogger
from typing import TypedDict

# from asking.models.performance import Performance
# from asking.models.runtime import Runtime


class NonBranchingActionDict(TypedDict, total=False):
    text: str
    title: str


# class NonBranchingAction:
#     def __init__(
#         self,
#         non_branching_action: NonBranchingActionDict,
#         run: Runtime,
#     ) -> None:
#         self._non_branching_action = non_branching_action
#         self._run = run

#     def _get_string(self, key: str) -> Optional[str]:
#         log = getLogger("asking")
#         log.debug('Getting "%s" from: %s', key, self._non_branching_action)
#         if value := self._non_branching_action.get(key, None):
#             return str(value)
#         return None

#     @property
#     def goto(self) -> Optional[str]:
#         return self._get_string("goto")

#     @property
#     def text(self) -> Optional[str]:
#         return self._get_string("text")

#     @property
#     def title(self) -> Optional[str]:
#         return self._get_string("title")

#     def render_text(self) -> None:
#         if not self.text:
#             return

#         self._run.out.write("\n")
#         self._run.out.write("text: ")
#         self._run.out.write(self.text)
#         self._run.out.write("\n")

#     def render_title(self) -> None:
#         if not self.title:
#             return

#         self._run.out.write("\n")
#         self._run.out.write("title: ")
#         self._run.out.write(self.title)
#         self._run.out.write("\n")

#     def perform(self) -> Optional[Performance]:
#         self.render_title()
#         self.render_text()

#         if self.goto:
#             return Performance(next=self.goto)

#         return None
