from __future__ import annotations

from typing import List, Generic, TypeVar, Callable, Union, Any, Type

from .monad import Functor, Either


TokenT = TypeVar('TokenT')
class Reader(Generic[TokenT]):

    def __init__(self, content: List[TokenT]):
        self.content = content
        self.counter = 0


S = TypeVar('S')
T = TypeVar('T')
class Parser(Generic[TokenT, S], Functor[S]):
    """
    An interface for all parser combinators.
    """

    def __init__(self, f: Callable[[Reader[TokenT]], List[S]]):
        self.func = f

    def parse(self, reader: Reader[TokenT]) -> List[S]:
        return self.func(reader)

    def __add__(self, p: Parser[TokenT, S]) -> Parser[TokenT, S]:
        return Join(self, p)

    def __or__(self, p: Parser[TokenT, S]) -> Parser[TokenT, S]:
        return Or(self, p)

    def fmap(self, f: Callable[[S], T]) -> Parser[TokenT, T]:
        return FunctorialParser(f, self)


MidT = TypeVar('MidT')
class FunctorialParser(Parser[TokenT, S]):

    def __init__(self, f: Callable[[MidT], S], a: Parser[TokenT, MidT]):
        self.f = f
        self.inner = a

    def parse(self, reader: Reader[TokenT]) -> List[S]:
        return [self.f(i) for i in self.inner.parse(reader)]


class Join(Parser[TokenT, S]):

    def __init__(self, a: Parser[TokenT, S], b: Parser[TokenT, S]):
        pass


class Or(Parser[TokenT, S]):

    def __init__(self, a: Parser[TokenT, S], b: Parser[TokenT, S]):
        pass
