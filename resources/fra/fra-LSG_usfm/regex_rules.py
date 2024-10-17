import regex as re
from kathairo.Tokenization.regex_rules import DefaultRegexRules
class CustomRegexRules(DefaultRegexRules):
    #WIP
    CONTRACTION_WORD_REGEX = re.compile(
        #r"\b\w+(?:[\'\w\’]+)?\b"
        r"[\'\’]\w"
    )