import unicodedata

def is_unicode_punctuation(char):
    category = unicodedata.category(char)
    return category.startswith("P")

def contains_number(string):
    return any(char.isdigit() for char in string)

zwsp = "​"
zwj = "‍"
zwnj = "‌"
empty_string = ""
nbsp = "\xa0"