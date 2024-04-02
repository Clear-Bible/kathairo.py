import unicodedata

def is_unicode_punctuation(char):
    category = unicodedata.category(char)
    return category.startswith("P")