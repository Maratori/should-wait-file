from match import ChildMatch
from should import Should


class Int(int):
    @property
    def should(self) -> 'IntShould':
        return IntShould(lambda: self)


class IntShould(Should[int, 'IntShould']):
    @property
    def be(self) -> 'IntShouldBe':
        return IntShouldBe(self)


class IntShouldBe(ChildMatch[int]):
    def equal(self, other: int) -> int:
        return self.match(lambda it: it == other)

    def greater(self, other: int) -> int:
        return self.match(lambda it: it > other)

    def greater_or_equal(self, other: int) -> int:
        return self.match(lambda it: it >= other)

    def less(self, other: int) -> int:
        return self.match(lambda it: it < other)

    def less_or_equal(self, other: int) -> int:
        return self.match(lambda it: it <= other)
