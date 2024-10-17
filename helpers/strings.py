import unicodedata

def is_unicode_punctuation(char):
    category = unicodedata.category(char)
    return category.startswith("P")

def contains_number(string):
    return any(char.isdigit() for char in string)

empty_string = ""

zwsp = "​"#\u200b
zwj = "‍"#\u200d
zwnj = "‌"#\u200c
nbsp = "\xa0"
space = " "

stop_words = [
    space,
    zwsp,
    zwj,
    zwnj,
    nbsp
]