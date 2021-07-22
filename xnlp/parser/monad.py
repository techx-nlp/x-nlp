from typing import List, Generic, TypeVar, Callable, Optional, Union, Type, Any


SourceT = TypeVar('SourceT')
TargetT = TypeVar('TargetT')
class Functor(Generic[SourceT]):

    def fmap(self, f: Callable[[SourceT], TargetT]) -> Functor[TargetT]:
        raise NotImplementedError


#MChildT = TypeVar('MChildT', bound=Monad[SourceT])
class Monad(Functor[SourceT]):

    @staticmethod
    def join(m: Monad[Monad[SourceT]]) -> Monad[SourceT]:
        return m.bind(lambda x: x)

    @classmethod
    def pure(cls, a: SourceT) -> Monad[SourceT]:
        if cls == Monad:
            raise NotImplementedError

        return cls.pure(a)

    def bind(self, f: Callable[[SourceT], Monad[TargetT]]) -> Monad[TargetT]:
        raise NotImplementedError


ErrorT = TypeVar('ErrorT')
class Either(Generic[ErrorT, SourceT], Monad[SourceT]):

    @staticmethod
    def fail(error: ErrorT):
        return Left(error)

    @classmethod
    def pure(cls, a: SourceT) -> Either[ErrorT, SourceT]:
        return Right(a)


class Left(Either[ErrorT, SourceT]):

    def __init__(self, error: ErrorT):
        self.left = error

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Left):
            return False

        return self.left == other.left

    def fmap(self, f: Callable[[SourceT], TargetT]) -> Either[ErrorT, TargetT]:
        return Either.fail(self.left)


class Right(Either[ErrorT, SourceT]):

    def __init__(self, value: SourceT):
        self.right = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Right):
            return False

        return self.right == other.right

    def fmap(self, f: Callable[[SourceT], TargetT]) -> Either[ErrorT, TargetT]:
        return Either.pure(f(self.right))