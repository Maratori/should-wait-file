import re
import time
from typing import TypeVar, Generic, Callable, overload

from condition import Condition


def wait_for(condition: Condition, *, timeout: int = 5, interval: float = 0.1) -> None:
    last_exception = None
    start = time.time()
    while time.time() < start + timeout:
        try:
            return condition()
        except Exception as ex:
            last_exception = ex
            # TODO: remove redundant last time sleep
            time.sleep(interval)
    raise TimeoutError from last_exception


T = TypeVar("T")


class ShouldNot(Generic[T]):
    def __init__(self, supplier: Callable[[], T]) -> None:
        self._supplier = supplier

    def match(self, condition: Callable[[T], bool]) -> T:
        obj = self._supplier()
        assert not condition(obj)
        return obj


class Should(ShouldNot[T]):
    def match(self, condition: Callable[[T], bool]) -> T:
        obj = self._supplier()
        assert condition(obj)
        return obj

    # noinspection PyPep8Naming
    @property
    def Not(self) -> ShouldNot[T]:
        return ShouldNot(self._supplier)


class IntShouldBe:
    def __init__(self, parent: 'IntShould') -> None:
        self._parent = parent

    def equal(self, other: int) -> int:
        return self._parent.match(lambda it: it == other)

    def greater(self, other: int) -> int:
        return self._parent.match(lambda it: it > other)

    def greater_or_equal(self, other: int) -> int:
        return self._parent.match(lambda it: it >= other)

    def less(self, other: int) -> int:
        return self._parent.match(lambda it: it < other)

    def less_or_equal(self, other: int) -> int:
        return self._parent.match(lambda it: it <= other)


class IntShould(Should[int]):
    @property
    def be(self) -> IntShouldBe:
        return IntShouldBe(self)


class StrShouldBe:
    def __init__(self, parent: 'StrShould') -> None:
        self._parent = parent

    def equal(self, other: str) -> str:
        return self._parent.match(lambda it: it == other)


class StrShould(Should[str]):
    @property
    def be(self) -> StrShouldBe:
        return StrShouldBe(self)

    def start_with(self, other: str) -> str:
        return self.match(lambda it: it.startswith(other))

    def end_with(self, other: str) -> str:
        return self.match(lambda it: it.endswith(other))

    def contain(self, other: str) -> str:
        return self.match(lambda it: other in it)

    def match_regex(self, pattern: str) -> str:
        return self.match(lambda it: bool(re.match(pattern, it)))


class Int(int):
    @property
    def should(self):
        return IntShould(lambda: self)


class Str(str):
    @overload
    def __init__(self, value: object = ...) -> None: ...

    @overload
    def __init__(self, value: bytes, encoding: str = ..., errors: str = ...) -> None: ...

    def __init__(self, value='', encoding=None, errors='strict'):
        super().__init__(value, encoding, errors)

    # def __init__(self, supplier: Callable[[], T]) -> None:

    @property
    def should(self):
        return StrShould(lambda: self)


class File:
    @property
    def size(self) -> Int:
        return Int(10)

    @property
    def text(self) -> Str:
        return Str("abc")


if __name__ == '__main__':
    print(Should(lambda: 10).match(lambda it: it == 10))
    print(Should(lambda: 10).Not.match(lambda it: it == 11))

    File().size.should.match(lambda it: it == 10)
    print(File().size.should.be.equal(10))
    File().text.should.match(lambda it: it == "abc")
    File().text.should.be.equal("abc")
    File().text.should.start_with("a")
    File().text.should.end_with("c")
    File().text.should.contain("b")
    File().text.should.match_regex(r"abc")

    # file.size.should.match(Condition())
    # file.size.should.Not.match(Condition())
    # file.size.should.be > 0
    #
    # file.text.should.be == "asdasd"
    # file.text.should.Not.be == "asdasd"
    # file.text.should.contain("asdasd")
    # file.text.should.start_with("asdasd")
    # file.text.should.end_with("asdasd")
    # file.text.should.Not.contain("asdasd")
    # file.text.should.Not.start_with("asdasd")
    # file.text.should.Not.end_with("asdasd")
    # file.text.should.meet(CustomCondition())
    # file.text.should.Not.meet(CustomCondition())
    #
    # partial(file.text.should.Not.contain, "asdasd")
