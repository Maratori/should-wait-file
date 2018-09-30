from typing import TypeVar, Callable, Generic


class File:
    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def should(self) -> 'FileShould':
        return FileShould(self)

    @property
    def exists(self) -> bool:
        return True


class Condition:
    def __init__(self,
                 predicate: Callable[..., bool],
                 *args,
                 **kwargs) -> None:
        self._predicate = predicate
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs) -> None:
        assert self._predicate(*args, *self._args, **kwargs, **self._kwargs)


class NotCondition(Condition):
    def __init__(self, base: Condition) -> None:
        super().__init__(lambda: not base._predicate(*base._args, **base._kwargs))


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


class FileShould(BaseShould['FileShould']):
    def __init__(self, file: File) -> None:
        self._file = file

    @property
    def exist(self) -> Condition:
        return Condition(lambda: self._file.exists)

    def meet(self, condition: Condition) -> None:
        condition(self._file)


file = File("aaa")
print(file.should)
print(file.should.exist)
print(file.should.Not)
print(file.should.Not.Not)
print(file.should.Not.Not.Not)
print(file.should.Not.exist)

file.should.exist()
file.should.Not.Not.exist()
# file.should.Not.exist()

file.should.exist()
