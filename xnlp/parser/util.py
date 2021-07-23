from typing import List, Generic, TypeVar, Callable, Union, Any, Type, Optional

from .combinator import Reader, Parser
from .monad import Either

S = TypeVar('S')
TokT = TypeVar('TokT')
def satisfy(predicate: Callable[[TokT], bool]) -> Parser[TokT, S, str]:

    def inner(reader: Reader[TokT, str]) -> Either[str, List[S]]:
        return reader.expect( # type: ignore
            predicate, f'Parsing failed at token {reader.get_counter() - 1}'
        ).fmap(lambda a: [a])

    return Parser(inner)


E = TypeVar('E')
def optional(parser: Parser[TokT, S, E]) -> Parser[TokT, S, E]:

    def inner(reader: Reader[TokT, E]) -> Either[E, List[S]]:
        counter = reader.get_counter()

        result = parser.parse(reader)
        if result.success():
            return result

        reader.load_counter(counter)
        return Either.pure([])

    return Parser(inner)


def zeroOrMore(parser: Parser[TokT, S, E]) -> Parser[TokT, S, E]:

    def outer(reader: Reader[TokT, E]) -> Either[E, List[S]]:
        out: Either[E, List[S]] = Either.pure([])
        counter = reader.get_counter()
        parse = parser.parse(reader)

        def middle(a: List[S]) -> List[S]:

            def inner(b: List[S]) -> List[S]:
                return a + b

            return parse.fmap(inner) # type: ignore

        while parse.success():
            out = out.fmap(middle) # type: ignore
            counter = reader.get_counter()

        reader.load_counter(counter)

        return out

    return Parser(outer)


def oneOrMore(parser: Parser[TokT, S, E]) -> Parser[TokT, S, E]:
    return parser + zeroOrMore(parser)