from __future__ import annotations

from typing import List, Generic, TypeVar, Callable, Union, Any

from .monad import Functor, Either


TokenT = TypeVar('TokenT')
class Reader(Generic[TokenT]):

    def __init__(self, content: List[TokenT]):
        self.content = content
        self.counter = 0


SourceT = TypeVar('SourceT')
TargetT = TypeVar('TargetT')
class Parser(Generic[TokenT, SourceT], Functor[SourceT]):
    """
    An interface for all parser combinators.
    """

    def __init__(self, f: Callable[[Reader[TokenT]], List[SourceT]]):
        self.func = f

    def parse(self, reader: Reader[TokenT]) -> List[SourceT]:
        return self.func(reader)

    def __add__(self, p: Parser[TokenT, SourceT]) -> Parser[TokenT, SourceT]:
        return Join(self, p)

    def __or__(self, p: Parser[TokenT, SourceT]) -> Parser[TokenT, SourceT]:
        return Or(self, p)

    def fmap(self, f: Callable[[SourceT], TargetT]) -> Parser[TokenT, TargetT]:
        return FunctorialParser(f, self)


MidT = TypeVar('MidT')
class FunctorialParser(Parser[TokenT, SourceT]):

    def __init__(self, f: Callable[[MidT], SourceT], a: Parser[TokenT, MidT]):
        self.f = f
        self.inner = a

    def parse(self, reader: Reader[TokenT]) -> List[SourceT]:
        return [self.f(i) for i in self.inner.parse(reader)]


class Join(Parser[TokenT, SourceT]):

    def __init__(self, a: Parser[TokenT, SourceT], b: Parser[TokenT, SourceT]):
        pass


class Or(Parser[TokenT, SourceT]):

    def __init__(self, a: Parser[TokenT, SourceT], b: Parser[TokenT, SourceT]):
        pass
