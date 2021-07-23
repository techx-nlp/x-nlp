from typing import List, Generic, TypeVar, Callable, Optional, Union, Type, Any


FromT = TypeVar('FromT')
ToT = TypeVar('ToT')
class Functor(Generic[FromT]):

    def fmap(self, f: Callable[[FromT], ToT]) -> Functor[ToT]:
        raise NotImplementedError


class Monad(Functor[FromT]):

    @staticmethod
    def join(m: Monad[Monad[FromT]]) -> Monad[FromT]:
        return m.bind(lambda x: x)

    @classmethod
    def pure(cls: Type[Monad[FromT]], a: FromT) -> Monad[FromT]:
        if cls == Monad:
            raise NotImplementedError

        return cls.pure(a)

    def bind(self, f: Callable[[FromT], Monad[ToT]]) -> Monad[ToT]:
        raise NotImplementedError