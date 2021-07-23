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


ErrorT = TypeVar('ErrorT')
class Either(Generic[ErrorT, FromT], Monad[FromT]):

    @staticmethod
    def fail(error: ErrorT) -> Either[ErrorT, FromT]:
        return Left(error)

    @classmethod
    def pure(
            cls: Type[Either[ErrorT, FromT]],
            a: FromT) -> Either[ErrorT, FromT]:

        return Right(a)


class Left(Either[ErrorT, FromT]):

    def __init__(self, error: ErrorT):
        self.left = error

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Left):
            return False

        return self.left == other.left

    def fmap(self, f: Callable[[FromT], ToT]) -> Either[ErrorT, ToT]:
        return Either.fail(self.left)

    def bind(self, f: Callable[[FromT], Monad[ToT]]) -> Monad[ToT]:
        return Either.fail(self.left)


class Right(Either[ErrorT, FromT]):

    def __init__(self, value: FromT):
        self.right = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Right):
            return False

        return self.right == other.right

    def fmap(self, f: Callable[[FromT], ToT]) -> Either[ErrorT, ToT]:
        return Either.pure(f(self.right))

    def bind(self, f: Callable[[FromT], Monad[ToT]]) -> Monad[ToT]:
        return f(self.right)