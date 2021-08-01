# dependencies


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


class T(enum.Enum):
    """
    Some simple tokens. Very inconclusive, but simple.
    """

    ADJ = 'Adjective'
    ADV = 'Adverb'
    NOUN = 'Noun'
    PUNCT = 'Punctuation'
    VERB = 'Verb'
    CCONJ = 'Coordinating Conjunction'


def log_func(code):
    return lambda x: print(f'\033[{code}m{x}\033[0m')


wrapped_satisfy = lambda p: satisfy(p).fmap(lambda t: t[0])
word = lambda w: wrapped_satisfy(lambda x: x[0] == w)
tok = lambda t: wrapped_satisfy(lambda x: x[1] == t)
end = expect_end('Expecting end of input')

good = log_func('32')
bad = log_func('91')


SIMPLE = [
    ('Elephant', T.NOUN),
    ('eat', T.VERB),
    ('banana', T.NOUN),
    ('.', T.PUNCT)
]

SENTS = [
    #SIMPLE,
    [
        ('Big', T.ADJ),
        ('elephant', T.NOUN),
        ('quickly', T.ADV),
        ('eat', T.VERB),
        ('big', T.ADJ),
        ('banana', T.NOUN),
        ('.', T.PUNCT)
    ], [
        ('Quick', T.ADJ),
        ('brown', T.ADJ),
        ('fox', T.NOUN),
        ('gracefully', T.ADV),
        ('stabbed', T.VERB),
        ('lazy', T.ADJ),
        ('dog', T.NOUN),
        ('.', T.PUNCT)
    ], [
        ('You', T.NOUN),
        ('build', T.VERB),
        ('houses', T.NOUN),
        ('?', T.PUNCT)
    ], [
        ('You', T.NOUN),
        ('build', T.VERB),
        ('houses', T.NOUN),
        ('!', T.PUNCT),
    ], [
        ('Thomas', T.NOUN),
        ('assign', T.VERB),
        ('homework', T.NOUN),
        (',', T.PUNCT),
        ('and', T.CCONJ),
        ('George', T.NOUN),
        ('burn', T.VERB),
        ('homework', T.NOUN),
        ('!', T.PUNCT)
    ], [
        ('Small', T.ADJ),
        ('mouse', T.NOUN),
        ('eat', T.VERB),
        ('cheese', T.NOUN),
        (',', T.PUNCT),
        ('but', T.CCONJ),
        ('large', T.ADJ),
        ('cat', T.NOUN),
        ('eat', T.VERB),
        ('lettuce', T.NOUN),
        ('.', T.PUNCT)
    ]
]

# incorrect sentences
ERR_SENTS = [
    [
        ('Big', T.ADJ),
        ('elephant', T.NOUN),
        ('quickly', T.ADV),
        ('eat', T.VERB),
        ('big', T.ADJ),
        ('banana', T.NOUN),
        ('.', T.PUNCT),
        ('yay', T.PUNCT)
    ], [
        ('Thomas', T.NOUN),
        ('assign', T.VERB),
        ('homework', T.NOUN),
        ('and', T.CCONJ),
        ('George', T.NOUN),
        ('burn', T.VERB),
        ('homework', T.NOUN),
        ('!', T.PUNCT)
    ], [
        ('Small', T.ADJ),
        ('mouse', T.NOUN),
        ('eat', T.VERB),
        ('cheese', T.NOUN),
        (',', T.PUNCT),
        ('large', T.ADJ),
        ('cat', T.NOUN),
        ('eat', T.VERB),
        ('lettuce', T.NOUN),
        ('.', T.PUNCT)
    ], [
        ('You', T.NOUN),
        ('build', T.VERB),
        ('houses', T.NOUN),
        ('?', T.PUNCT),
        ('?', T.PUNCT)
    ], [
        ('Big', T.ADJ),
        ('elephant', T.NOUN),
        ('quickly', T.ADV),
        ('hastily', T.ADV),
        ('eat', T.VERB),
        ('big', T.ADJ),
        ('banana', T.NOUN),
        ('.', T.PUNCT)
    ]
]


COMP_NOUN = zero_or_more(tok(T.ADJ)) + tok(T.NOUN)
COMP_VERB = optional(tok(T.ADV)) + tok(T.VERB)
SIMPLE_SENT = COMP_NOUN + COMP_VERB + COMP_NOUN
END_SENT = (word('.') | word('!')) + end

ENGLISH_PARSER = SIMPLE_SENT


if ENGLISH_PARSER is None:
    bad('Build the parser first!')
else:
    for i, sent in enumerate(SENTS):
        runParser(ENGLISH_PARSER, sent)
        good(f'Sentence {i} Passed')

    print()
    good('Validation Tests Passed')