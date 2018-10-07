from typing import TypeVar, Callable, Generic

from match import Match

T = TypeVar("T")
SelfType = TypeVar("SelfType", bound="Should")


class Should(Generic[T, SelfType], Match[T]):
    def __init__(self: SelfType, supplier: Callable[[], T]) -> None:
        self._supplier = supplier

    def match(self: SelfType, condition: Callable[[T], bool]) -> T:
        print("match")
        obj = self._supplier()
        assert condition(obj)
        return obj

    @property
    def Not(self: SelfType) -> SelfType:
        prop = "_base_should_object"
        if self.__class__.__name__.endswith("Not") and hasattr(self, prop):
            return getattr(self, prop)

        def not_match(inner_self, condition: Callable[[T], bool]) -> T:
            print("not_match")
            obj = inner_self._supplier()
            assert not condition(obj)
            return obj

        attributes = dict(self.__class__.__dict__)
        attributes[self.match.__name__] = not_match
        attributes[prop] = self
        return type(self.__class__.__name__ + "Not", (self.__class__,), attributes)(self._supplier)
