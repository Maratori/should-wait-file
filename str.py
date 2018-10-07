import re

from match import ChildMatch
from should import Should


class Str(str):
    @property
    def should(self) -> 'StrShould':
        return StrShould(lambda: self)


class StrShould(Should[str, 'StrShould']):
    @property
    def be(self) -> 'StrShouldBe':
        return StrShouldBe(self)

    def start_with(self, other: str) -> str:
        return self.match(lambda it: it.startswith(other))

    def end_with(self, other: str) -> str:
        return self.match(lambda it: it.endswith(other))

    def contain(self, other: str) -> str:
        return self.match(lambda it: other in it)

    def match_regex(self, pattern: str) -> str:
        return self.match(lambda it: bool(re.match(pattern, it)))


class StrShouldBe(ChildMatch[str]):
    def equal(self, other: str) -> str:
        return self.match(lambda it: it == other)
