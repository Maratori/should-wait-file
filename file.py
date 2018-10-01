from condition import Condition
from should import BaseShould


class File:
    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def should(self) -> 'FileShould':
        return FileShould(self)

    @property
    def exists(self) -> bool:
        return True


class FileShould(BaseShould['FileShould']):
    def __init__(self, file: File) -> None:
        self._file = file

    @property
    def exist(self) -> Condition:
        return Condition(lambda: self._file.exists)

    def meet(self, condition: Condition) -> None:
        condition(self._file)
