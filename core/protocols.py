# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> core/protocols.py

> Defines the abs classes for the two streams that make core interact
> with the input and output modules.
> Defines:
>   - a read func   (PickFromStream(self))
>   - a write func  (SendToStream(self, raw_data))
"""

from typing import Protocol, List, Any, runtime_checkable
from collections import deque

@runtime_checkable
class ToStream(Protocol):
    def SendToStream(self,raw_data:List[Any]) -> None:
        ...
class FromStream(Protocol):
    def PickFromStream(self) -> List[Any]:
        ...
