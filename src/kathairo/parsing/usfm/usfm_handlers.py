from typing import Iterable, List, Optional

from machine.scripture.verse_ref import VerseRef
from machine.corpora.text_row import TextRow
from machine.corpora.usfm_parser_state import UsfmParserState
from machine.corpora.usfm_token import UsfmTokenType
from machine.corpora.scripture_ref import ScriptureRef
from machine.corpora import ScriptureTextType
from machine.utils.string_utils import has_sentence_ending

from machine.corpora.usfm_text_base import UsfmTextBase
from machine.corpora.usfm_text_base import _TextRowCollector

class ModifiedTextRowCollector(_TextRowCollector):
    def __init__(self, text: UsfmTextBase, psalm_superscription_tag: str = "d") -> None:
        super().__init__(text)
        
        self._psalm_superscription_tag = psalm_superscription_tag
        self._in_psalm_superscription = False
        self.marker = ""

    def start_para(
        self,
        state: UsfmParserState,
        marker: str,
        unknown: bool,
        attributes,
    ) -> None:        
        self.marker = marker
        is_superscription = (
            marker == self._psalm_superscription_tag
            and state.verse_ref.book == "PSA"
            and state.verse_ref.chapter not in ("119", "107")
        )

        if is_superscription:
            self._in_psalm_superscription = True

        is_in_psalm_verse_zero = (
            self._cur_verse_ref.book == "PSA"
            and self._cur_verse_ref.verse_num == 0
            and self._current_text_type == ScriptureTextType.VERSE
            and not state.is_verse_text
        )

        if is_in_psalm_verse_zero:
            self._end_verse_text_wrapper(state)

        super().start_para(state, marker, unknown, attributes)

    def verse(
        self, state: UsfmParserState, number: str, marker: str, alt_number: Optional[str], pub_number: Optional[str]
    ) -> None:
        
        is_psalm_verse_zero = (
            number == "0"
            and state.verse_ref.book == "PSA"
        )

        if is_psalm_verse_zero:
            if self._current_text_type == ScriptureTextType.NONVERSE:
                self._end_non_verse_text_wrapper(state)
            elif self._current_text_type == ScriptureTextType.VERSE:
                self._end_verse_text_wrapper(state)
            self._update_verse_ref(state.verse_ref, marker)
            self._start_verse_text_wrapper(state)
        else:
            super().verse(state, number, marker, alt_number, pub_number)

    def text(self, state: UsfmParserState, text: str) -> None:
        if (self.marker == self._psalm_superscription_tag
            and state.verse_ref.book == "PSA"
            and state.verse_ref.chapter in ("119", "107")):
            return

        if (state.verse_ref.book == "PSA" 
            and self._in_psalm_superscription 
            and state.prev_token.marker == "rq"):
            return

        is_psalm_verse_zero = (
            self._cur_verse_ref.book == "PSA"
            and self._cur_verse_ref.verse_num == 0
            and self._current_text_type == ScriptureTextType.VERSE
            and not state.is_verse_text
            and len(self._row_texts_stack) > 0
        )

        if is_psalm_verse_zero and len(text) > 0:
            row_text = self._row_texts_stack[-1]
            if (
                state.prev_token is not None
                and state.prev_token.type == UsfmTokenType.END
                and (len(row_text) == 0 or row_text[-1].isspace())
            ):
                text = text.lstrip()
            row_text += text
            self._row_texts_stack[-1] = row_text
        else:
            super().text(state, text)

    def opt_break(self, state: UsfmParserState) -> None:
        self._check_convert_verse_para_to_non_verse(state)
        if self._text._include_markers:
            self._row_texts_stack[-1] += "//"

    def _end_verse_text_wrapper(self, state: UsfmParserState) -> None:
        
        is_psalm_verse_zero = (
            self._cur_verse_ref.book == "PSA"
            and self._cur_verse_ref.verse_num == 0
        )

        if is_psalm_verse_zero:
            if self._current_text_type == ScriptureTextType.VERSE:
                if not self._duplicate_verse:
                    self._end_verse_text(state, self._create_verse_refs())
                self._cur_text_type_stack.pop()
        else:
            super()._end_verse_text_wrapper(state)

    def end_para(self, state: UsfmParserState, marker: str) -> None:
        self.marker = marker

        if marker != self._psalm_superscription_tag and marker in ("qa", "rq"):
            self._in_psalm_superscription = False

        super().end_para(state, marker)

        if marker != self._psalm_superscription_tag:
            self._in_psalm_superscription = False

    def _end_non_verse_text(self, state: UsfmParserState, scripture_ref: ScriptureRef) -> None:
        text = self._row_texts_stack.pop() if self._row_texts_stack else ""

        if self._in_psalm_superscription and text.strip():
            self._rows.append(self._text._create_scripture_row(scripture_ref, text, self._sentence_start))
            self._sentence_start = has_sentence_ending(text)
        elif self._text._include_all_text and text:
            self._rows.append(self._text._create_scripture_row(scripture_ref, text, self._sentence_start))