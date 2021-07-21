import enum


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