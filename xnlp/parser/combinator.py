from __future__ import annotations

from typing import List, Generic, TypeVar, Callable, Union, Any

#from .token import Token


TokenT = TypeVar('TokenT')
class Reader(Generic[TokenT]):

    def __init__(self, content: List[TokenT]):
        self.content = content
        self.counter = 0


OutT = TypeVar('OutT')
class Parser(Generic[TokenT, OutT]):
    """
    An interface for all parser combinators.
    """

    def __init__(self, f: Callable[[Reader[TokenT]], List[OutT]]):
        self.func = f

    def parse(self, reader: Reader[TokenT]) -> List[OutT]:
        return self.func(reader)

    def __add__(self, other: Parser[TokenT, OutT]) -> Parser[TokenT, OutT]:
        return Join(self, other)

    def __or__(self, other: Parser[TokenT, OutT]) -> Parser[TokenT, OutT]:
        return Or(self, other)


class FunctorialParser(Parser[TokenT, OutT]):
    pass


class Join(Parser[TokenT, OutT]):

    def __init__(self, a: Parser[TokenT, OutT], b: Parser[TokenT, OutT]):
        pass


class Or(Parser[TokenT, OutT]):

    def __init__(self, a: Parser[TokenT, OutT], b: Parser[TokenT, OutT]):
        pass
