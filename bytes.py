from match import ChildMatch
from should import Should


class Bytes(bytes):
    @property
    def should(self) -> 'BytesShould':
        return BytesShould(lambda: self)


class BytesShould(Should[bytes, 'BytesShould']):
    @property
    def be(self) -> 'BytesShouldBe':
        return BytesShouldBe(self)


class BytesShouldBe(ChildMatch[bytes]):
    def equal(self, other: bytes) -> bytes:
        return self.match(lambda it: it == other)
