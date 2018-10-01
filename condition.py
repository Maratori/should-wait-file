from typing import Callable


class Condition:
    def __init__(self,
                 predicate: Callable[..., bool],
                 *args,
                 **kwargs) -> None:
        self._predicate = predicate
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs) -> None:
        self.check(*args, **kwargs)

    def check(self, *args, **kwargs) -> None:
        assert self._predicate(*args, *self._args, **kwargs, **self._kwargs)


class NotCondition(Condition):
    def __init__(self, base: Condition) -> None:
        super().__init__(lambda: not base._predicate(*base._args, **base._kwargs))
