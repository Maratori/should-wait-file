from pathlib import Path
from pprint import pprint

from int import Int
from should import Should
from str import Str


class File:
    def __init__(self, *segments: str) -> None:
        self._path = Path(*segments)

    @property
    def should(self) -> 'FileShould':
        return FileShould(lambda: self)

    @property
    def size(self) -> Int:
        return Int(10)

    @property
    def text(self) -> Str:
        return Str("abc")


class FileShould(Should[File, 'FileShould']):
    def exist(self) -> File:
        return self.match(lambda it: True)


if __name__ == '__main__':
    File().should.exist()
    File().should.Not.Not.exist()
    # File().should.Not.exist()

    File().size.should.be.equal(10)
    File().size.should.Not.be.equal(11)
    # File().size.should.Not.be.equal(10)

    pprint(File().size.should)
    pprint(File().size.should.Not)
    pprint(File().size.should.Not.Not)
