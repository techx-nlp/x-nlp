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
        return Either(False, error, None)

    def __init__(self, succ: bool, a: ErrorT, b: SourceT):
        self.succ = succ
        if self.succ:
            self.right = b
        else:
            self.left = a

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Either):
            return False

        if self.succ == other.succ == True:
            return self.right == other.right

        if self.succ == other.succ == False:
            return self.left == other.left

        return False

    def fmap(self, f: Callable[[SourceT], TargetT]) -> Functor[TargetT]:
        if not self.succ:
            return Either.fail(self.left)

        return Either.pure(f(self.right))