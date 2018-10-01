from typing import TypeVar, Generic

from condition import NotCondition

T = TypeVar('T', bound='BaseShould')


class BaseShould(Generic[T]):
    @property
    def Not(self: T) -> T:
        prop = "_base_should_object"
        if self.__class__.__name__.endswith("Not") and hasattr(self, prop):
            return getattr(self, prop)
        return type(self.__class__.__name__ + "Not", (), {
            "__getattr__": lambda inner_self, item: NotCondition(getattr(getattr(inner_self, prop), item)),
            prop: self,
            "Not": BaseShould.Not,
        })()
