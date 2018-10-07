from abc import ABC
from typing import Generic, Callable, TypeVar

T = TypeVar("T")


class Match(Generic[T], ABC):
    def match(self, condition: Callable[[T], bool]) -> T: ...


class ChildMatch(Match[T], ABC):
    def __init__(self, parent: Match[T]) -> None:
        self._parent = parent

    def match(self, condition: Callable[[T], bool]) -> T:
        return self._parent.match(condition)
