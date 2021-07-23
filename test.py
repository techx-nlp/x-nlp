import enum

from xnlp.parser import (
    Parser,
    runParser,
    satisfy,
    optional,
    zero_or_more,
    one_or_more,
    expect_end
)


class Token(enum.Enum):
    """
    Some simple tokens. Very inconclusive, but simple.
    """

    ADJ = 'Adjective'
    ADV = 'Adverb'
    NOUN = 'Noun'
    PUNCT = 'Punctuation'
    VERB = 'Verb'
    CCONJ = 'Coordinating Conjunction'


SIMPLE = [
    ('Elephant', Token.NOUN),
    ('eat', Token.VERB),
    ('banana', Token.NOUN),
    ('?', Token.PUNCT)
]

wrapped_satisfy = lambda p: satisfy(p).fmap(lambda t: t[0])
word = lambda w: wrapped_satisfy(lambda x: x[0] == w)
tok = lambda t: wrapped_satisfy(lambda x: x[1] == t)
end = expect_end('Expecting end of input')

N_V_N = tok(Token.NOUN) + tok(Token.VERB) + tok(Token.NOUN) + word('.')
QUESTION = tok(Token.NOUN) + tok(Token.VERB) + tok(Token.NOUN) + word('?')
parser = (N_V_N | QUESTION) + end

print('Result: ', runParser(parser, SIMPLE))