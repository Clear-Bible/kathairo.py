import regex as re

INNER_WORD_PUNCT_REGEX = re.compile(
    r"[&\-:=@\xAD\xB7\u2010\u2011\u2027]+|['_]+",#?
)

NUMBER_COMMA_REGEX = re.compile(
    r"(?<=\d),(?=\d)"
)

NUMBER_PERIOD_REGEX = re.compile(
    r"(?<=\d)\.(?=\d)"
)

RIGHT_SINGLE_QUOTE_AS_APOSTROPHE_REGEX = re.compile(
    r"(?<=\p{L})’(?=\p{L})"
)

CONTRACTION_WORD_REGEX = re.compile(
    r"\b\w+(?:[\'\w\’]+)?\b"
)

regex_rules = [
    INNER_WORD_PUNCT_REGEX,
    NUMBER_COMMA_REGEX,
    NUMBER_PERIOD_REGEX,
    RIGHT_SINGLE_QUOTE_AS_APOSTROPHE_REGEX,
    #CONTRACTION_WORD_REGEX
]