from typing import Any, Dict, List, TypedDict, Union

StopReason = Any

AnyDict = Dict[Any, Any]

StageKey = str

BranchingKey = Union[List[str], str]


# class ActionDict(TypedDict, total=False):
#     question: str
#     text: str
#     title: str


class PathDict(TypedDict):
    response: List[str]
    then: List[Dict[str, Any]]


# class BranchingActionDict(ActionDict, total=False):
#     branch: List[PathDict]


StageType = List[Dict[str, Any]]
