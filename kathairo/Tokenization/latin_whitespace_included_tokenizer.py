from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple, cast

import regex as re

from machine.annotations.range import Range
from machine.utils.string_utils import is_control, is_punctuation, is_symbol
from .whitespace_included_tokenizer import WhitespaceIncludedTokenizer
from spacy.lang.fr.tokenizer_exceptions import FR_BASE_EXCEPTIONS

INNER_WORD_PUNCT_REGEX = re.compile(
    r"[&\-:=?@\xAD\xB7\u2010\u2011\u2027]+|['_]+",
)
URL_REGEX = re.compile(r"(?:[\w-]+://?|www[.])[^\s()<>]+(?:[\w\d]+|(?:[^\p{P}\s]|/))", re.IGNORECASE)

#kathairo manually handles periods, commas, and right single quotes as opposed to having them be part of INNER_WORD_PUNCT_REGEX
NUMBER_COMMA_REGEX = re.compile(
    r"[(?<=\d),(?=\d)]"
)

NUMBER_PERIOD_REGEX = re.compile(
    r"[(?<=\d).(?=\d)]"
)

RIGHT_SINGLE_QUOTE_AS_APOSTROPHE_REGEX = re.compile(
    r"(?<=\p{L})’(?=\p{L})"
)

CONTRACTION_WORD_REGEX = re.compile(
    r"\b\w+(?:[\'\w\’]+)?\b"
)

class LatinWhitespaceIncludedWordTokenizer(WhitespaceIncludedTokenizer): #uses WhitepspaceIncludedTokenizer
    def __init__(self, abbreviations: Iterable[str] = [], treat_apostrophe_as_single_quote: bool = False, language:str = None) -> None:
        self._abbreviations = {a.lower() for a in abbreviations}
        self.treat_apostrophe_as_single_quote = treat_apostrophe_as_single_quote
        self.language = language

    def tokenize_as_ranges(self, data: str, data_range: Optional[Range[int]] = None) -> Iterable[Range[int]]:
        if data_range is None:
            data_range = Range.create(0, len(data))
        ctxt = LatinWhitespaceIncludedWordTokenizer._TokenizeContext()
        for char_range in super().tokenize_as_ranges(data, data_range):
            url_match = URL_REGEX.match(data[char_range.start : char_range.end])
            if url_match is not None:
                url_len = len(url_match.group())
                yield Range.create(char_range.start, char_range.start + url_len)
                ctxt.index = char_range.start + url_len
            else:
                ctxt.index = char_range.start

            ctxt.word_start = -1
            ctxt.inner_word_punct = -1

            while ctxt.index < char_range.end:
                token_range1, token_range2 = self._process_character(data, data_range, ctxt)
                if token_range1 is not None:
                    yield token_range1
                if token_range2 is not None:
                    yield token_range2

            if ctxt.word_start != -1:
                if ctxt.inner_word_punct != -1:
                    inner_punct_str = data[ctxt.inner_word_punct : char_range.end]
                    if (
                        inner_punct_str == "." and self._is_abbreviation(data, ctxt.word_start, ctxt.inner_word_punct)
                    ) or (inner_punct_str == "'" and not self.treat_apostrophe_as_single_quote):
                        yield Range.create(ctxt.word_start, char_range.end)
                    else:
                        yield Range.create(cast(int, ctxt.word_start), ctxt.inner_word_punct)
                        yield Range.create(ctxt.inner_word_punct, char_range.end)
                else:
                    yield Range.create(ctxt.word_start, char_range.end)

    def _process_character(
        self, data: str, data_range: Range[int], ctxt: LatinWhitespaceIncludedWordTokenizer._TokenizeContext
    ) -> Tuple[Optional[Range[int]], Optional[Range[int]]]:
        token_ranges: Tuple[Optional[Range[int]], Optional[Range[int]]] = (None, None)
        c = data[ctxt.index]
        end_index = ctxt.index + 1

        if is_punctuation(c) or is_symbol(c) or is_control(c):
            while end_index != data_range.end and data[end_index] == c:
                end_index += 1
            if ctxt.word_start == -1:
                if c == "'" and not self.treat_apostrophe_as_single_quote:
                    ctxt.word_start = ctxt.index
                else:
                    token_ranges = (Range.create(ctxt.index, end_index), None)
            elif ctxt.inner_word_punct != -1:
                inner_punct_str = data[ctxt.inner_word_punct : ctxt.index]
                if inner_punct_str == "'" and not self.treat_apostrophe_as_single_quote:
                    token_ranges = (Range.create(ctxt.word_start, ctxt.index), None)
                else:
                    token_ranges = (
                        Range.create(ctxt.word_start, ctxt.inner_word_punct),
                        Range.create(ctxt.inner_word_punct, ctxt.index),
                    )
                ctxt.word_start = ctxt.index
            else:
                match = INNER_WORD_PUNCT_REGEX.match(data, ctxt.index)
                if match is not None:
                    ctxt.inner_word_punct = ctxt.index
                    group = match.group()
                    ctxt.index += len(group)
                    return token_ranges
                
                #start of changes: kathairo manually handles periods, commas, and right single quotes as opposed to having them be part of INNER_WORD_PUNCT_REGEX
                substring = data[ctxt.index-1:ctxt.index+2]
                is_number_comma_match = NUMBER_COMMA_REGEX.match(substring)

                if is_number_comma_match is not None:
                    ctxt.inner_word_punct = ctxt.index
                    group = is_number_comma_match.group()
                    ctxt.index += len(group)
                    return token_ranges

                is_number_period_match = NUMBER_PERIOD_REGEX.match(substring)

                if is_number_period_match is not None:# and not match_is_number_comma:
                    ctxt.inner_word_punct = ctxt.index
                    group = is_number_period_match.group()
                    ctxt.index += len(group)
                    return token_ranges
                
                is_right_single_quote_apostrophe = RIGHT_SINGLE_QUOTE_AS_APOSTROPHE_REGEX.search(substring)

                if is_right_single_quote_apostrophe is not None:
                    group = is_right_single_quote_apostrophe.group()
                    ctxt.inner_word_punct = ctxt.index
                    ctxt.index += len(group)
                    if(self.language == "fra"):
                        contraction_token = CONTRACTION_WORD_REGEX.match(data, ctxt.word_start).group().replace("’","'")
                        if(contraction_token not in FR_BASE_EXCEPTIONS):
                            token_ranges = (Range.create(ctxt.word_start, ctxt.index),None)
                            ctxt.word_start = -1
                    return token_ranges
                #end of changes

                token_ranges = (Range.create(ctxt.word_start, ctxt.index), Range.create(ctxt.index, end_index))
                ctxt.word_start = -1
        elif ctxt.word_start == -1:
            ctxt.word_start = ctxt.index

        ctxt.inner_word_punct = -1
        ctxt.index = end_index
        return token_ranges

    def _is_abbreviation(self, data: str, start: int, end: int) -> bool:
        substr = data[start:end].lower()
        return substr in self._abbreviations

    @dataclass
    class _TokenizeContext:
        index: int = 0
        word_start: int = 0
        inner_word_punct: int = 0
