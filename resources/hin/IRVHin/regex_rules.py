import regex as re
from kathairo.Tokenization.regex_rules import DefaultRegexRules

class CustomRegexRules(DefaultRegexRules):
    #NON_JOINING_PUNCT =r"[.،«?।!।၊–…{}—《》（）‘’“”;？：；。！，、,\[\]]"
    NON_JOINING_PUNCT = r"[.،«?!।…{}《》（）‘’“”;？：；。！，、,\[\]]"
    #does nothing, oddly        ।   ၊ 
    # is joining in some cases  –   —

    WORD_LEVEL_PUNCT_REGEX = re.compile(
        fr"(?<=\w)(\p{{P}}(?<!{NON_JOINING_PUNCT}))(?=\w)"
    )