# # from typing import Optional
# from asking.models.non_branching_action import (
#     NonBranchingActionDict,
#     # NonBranchingAction,
# )
# from asking.models.ask import AskDict
# # from asking.models.performance import Performance
# # from asking.models.runtime import Runtime
# # from logging import getLogger


# # class Action(NonBranchingAction):
# #     def __init__(self, action: ActionDict, run: Runtime) -> None:
# #         super().__init__(non_branching_action=action, run=run)
# #         self._action = action

# #     @property
# #     def ask(self) -> Optional[Ask]:
# #         log = getLogger("asking")
# #         try:
# #             ask = self._action["ask"]
# #         except KeyError:
# #             log.debug("%s has no ask", self)
# #             return None
# #         return Ask(ask=ask, run=self._run)

# #     def perform(self) -> Optional[Performance]:
# #         if performance := super().perform():
# #             return performance

# #         if ask := self.ask:
# #             return ask.perform()

# #         return None
