# from logging import getLogger
# from re import match
# from typing import Optional

# from asking.models.non_branching_action import NonBranchingActionDict


# class ResponseConditionDict(NonBranchingActionDict, total=False):
#     exact: str
#     like: str


# class ResponseCondition:
#     def __init__(self, response_condition: ResponseConditionDict) -> None:
#         self._response_condition = response_condition

#     def _get_string(self, key: str) -> Optional[str]:
#         log = getLogger("asking")
#         log.debug('Getting "%s" from: %s', key, self._response_condition)
#         if value := self._response_condition.get(key, None):
#             return str(value)
#         return None

#     @property
#     def exact(self) -> Optional[str]:
#         return self._get_string("exact")

#     @property
#     def like(self) -> Optional[str]:
#         return self._get_string("like")

#     def pass_exact(self, value: str) -> bool:
#         return self.exact is not None and self.exact == value

#     def pass_like(self, value: str) -> bool:
#         return self.like is not None and not not match(self.like, value)

#     def pass_any(self, value: str) -> bool:
#         checks = [
#             self.pass_exact,
#             self.pass_like,
#         ]

#         for check in checks:
#             if check(value):
#                 return True

#         return False
