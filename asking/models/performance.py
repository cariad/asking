from dataclasses import dataclass

from asking.types import StopType
from typing import Optional


@dataclass
class Performance:
    stop: Optional[StopType] = None
    next: Optional[str] = None
