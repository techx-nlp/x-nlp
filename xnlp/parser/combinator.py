from __future__ import annotations

from typing import List, Generic, TypeVar, Callable

#from .token import Token


TokenT = TypeVar('TokenT')
class Reader(Generic[TokenT]):
    pass


OutT = TypeVar('OutT')
class Parser(Generic[TokenT, OutT]):
    """
    An interface for all parser combinators.
    """

    def __init__(self, f: Callable[[Reader[TokenT]], OutT]):
        self.func = f

    def parse(self, reader: Reader[TokenT]) -> OutT:
        return self.func(reader)

    def __add__(self, other: Parser) -> Parser:
        return Join(self, other)

    def __or__(self, other: Parser) -> Parser:
        return Or(self, other)

