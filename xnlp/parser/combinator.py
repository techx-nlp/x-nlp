from __future__ import annotations

from typing import List, Generic, TypeVar, Callable, Union, Any

from .monad import Monad, Either


TokenT = TypeVar('TokenT')
class Reader(Generic[TokenT]):

    def __init__(self, content: List[TokenT]):
        self.content = content
        self.counter = 0


OutT = TypeVar('OutT')
MapT = TypeVar('MapT')
class Parser(Generic[TokenT, OutT], Monad[OutT]):
    """
    An interface for all parser combinators.
    """

    def __init__(self, f: Callable[[Reader[TokenT]], OutT]):
        self.func = f

    def parse(self, reader: Reader[TokenT]) -> OutT:
        return self.func(reader)

    def __add__(self, other: Parser[TokenT, OutT]) -> Parser[TokenT, OutT]:
        return Join(self, other)

    def __or__(self, other: Parser[TokenT, OutT]) -> Parser[TokenT, OutT]:
        return Or(self, other)

    def fmap(self, f: Callable[[OutT], MapT]) -> Parser[TokenT, MapT]:
        return FunctorialParser(f, self)


MidT = TypeVar('MidT')
class FunctorialParser(Parser[TokenT, OutT]):

    def __init__(self, f: Callable[[MidT], OutT], old: Parser[TokenT, MidT]):
        self.f = f
        self.inner = old

    def parse(self, reader: Reader[TokenT]) -> OutT:
        return self.f(self.inner.parse(reader))


class Join(Parser[TokenT, OutT]):

    def __init__(self, a: Parser[TokenT, OutT], b: Parser[TokenT, OutT]):
        pass


class Or(Parser[TokenT, OutT]):

    def __init__(self, a: Parser[TokenT, OutT], b: Parser[TokenT, OutT]):
        pass
