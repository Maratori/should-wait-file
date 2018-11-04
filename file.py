import os
import sys
# noinspection PyUnresolvedReferences,PyProtectedMember
from pathlib import Path, WindowsPath, _WindowsFlavour, _PosixFlavour  # type: ignore
from pprint import pprint

from bytes import Bytes
from int import Int
from should import Should
from str import Str


class File(Path):
    _flavour = _WindowsFlavour() if os.name == 'nt' else _PosixFlavour()
    __slots__ = ()

    if os.name == 'nt':
        if sys.version_info >= (3, 5):
            owner = WindowsPath.owner
            group = WindowsPath.group
        if sys.version_info >= (3, 7):
            # noinspection PyUnresolvedReferences
            is_mount = WindowsPath.is_mount

    @property
    def should(self) -> 'FileShould':
        return FileShould(lambda: self)

    @property
    def exists(self) -> bool:
        return self.is_file()

    @property
    def size(self) -> Int:
        return Int(10)

    def read_bytes(self) -> Bytes:
        """
        Open the file in bytes mode, read it, and close the file.
        """
        if sys.version_info >= (3, 5):
            return Bytes(super().read_bytes())
        else:
            with self.open(mode='rb') as f:
                return Bytes(f.read())

    def read_text(self, encoding: str = None, errors: str = None) -> Str:
        """
        Open the file in text mode, read it, and close the file.
        """
        if sys.version_info >= (3, 5):
            return Str(super().read_text(encoding, errors))
        else:
            with self.open(mode='r', encoding=encoding, errors=errors) as f:
                return Str(f.read())


class FileShould(Should[File, 'FileShould']):
    def exist(self) -> File:
        return self.match(lambda it: it.exists)


if __name__ == '__main__':
    File().should.exist()
    File().should.Not.Not.exist()
    # File().should.Not.exist()

    File().size.should.be.equal(10)
    File().size.should.Not.be.equal(11)
    # File().foo()
    # File().size.should.Not.be.equal(10)

    pprint(File().size.should)
    pprint(File().size.should.Not)
    pprint(File().size.should.Not.Not)
