from __future__ import annotations

from typing import List, Generic, TypeVar, Callable, Union, Any, Type, Optional

from .monad import Functor, Either


TokT = TypeVar('TokT')
class Reader(Generic[TokT]):

    def __init__(self, content: List[TokT]):
        self.content = content
        self.counter = 0

    def expect(self, predicate: Callable[[TokT], bool]) -> Optional[TokT]:
        token = self.content[self.counter]
        self.counter += 1

        if predicate(token):
            return token

        return None

    def load_counter(self, update: int) -> None:
        self.counter = update

    def get_counter(self) -> int:
        return self.counter


S = TypeVar('S')
T = TypeVar('T')
E = TypeVar('E')
class Parser(Generic[TokT, S, E], Functor[S]):
    """
    An interface for all parser combinators.
    """

    def __init__(self, f: Callable[[Reader[TokT]], Either[E, List[S]]]):
        self.func = f

    def parse(self, reader: Reader[TokT]) -> Either[E, List[S]]:
        return self.func(reader)

    def __add__(self, p: Parser[TokT, S, E]) -> Parser[TokT, S, E]:
        return Join(self, p)

    def __or__(self, p: Parser[TokT, S, E]) -> Parser[TokT, S, E]:
        return Or(self, p)

    def fmap(self, f: Callable[[S], T]) -> Parser[TokT, T, E]:
        return FunctorialParser(f, self)


U = TypeVar('U')
class FunctorialParser(Parser[TokT, S, E]):

    def __init__(self, f: Callable[[U], S], a: Parser[TokT, U, E]):
        self.f = f
        self.inner = a

    def parse(self, reader: Reader[TokT]) -> Either[E, List[S]]:
        return self.inner.parse(reader).fmap( # type: ignore
            lambda a: [self.f(i) for i in a]
        )


class Join(Parser[TokT, S, E]):

    def __init__(self, a: Parser[TokT, S, E], b: Parser[TokT, S, E]):
        self.a = a
        self.b = b

    def parse(self, reader: Reader[TokT]) -> Either[E, List[S]]:
        # mypy doesn't support lambdas...

        def outer(a: List[S]):

            def inner(b: List[S]):
                return a + b

            return self.b.parse(reader).fmap(inner) # type: ignore

        return self.a.parse(reader).fmap(outer) # type: ignore


class Or(Parser[TokT, S, E]):

    def __init__(self, a: Parser[TokT, S, E], b: Parser[TokT, S, E]):
        self.a = a
        self.b = b

    def parse(self, reader: Reader[TokT]) -> Either[E, List[S]]:
        counter = reader.get_counter()

        result = self.a.parse(reader)
        if (result.success()):
            return result

        reader.load_counter(counter)
        return self.b.parse(reader)