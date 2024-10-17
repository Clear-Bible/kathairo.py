import regex as re
from kathairo.Tokenization.regex_rules import DefaultRegexRules

class CustomRegexRules(DefaultRegexRules):
    #Get Rid of Extra Variables
    INNER_WORD_PUNCT_REGEX = re.compile(
        r"[&\-:=@\xAD\xB7\u2010\u2011\u2027]+|[_]+"
    )
    
    def get_regex_rules(self):
        regex_rules = [
            self.INNER_WORD_PUNCT_REGEX,
            super().NUMBER_COMMA_REGEX,
            super().NUMBER_PERIOD_REGEX,
            super().RIGHT_SINGLE_QUOTE_AS_APOSTROPHE_REGEX
        ]
        
        return regex_rules