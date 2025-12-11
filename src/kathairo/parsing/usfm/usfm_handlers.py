from typing import Iterable, List, Optional, Sequence

from machine.scripture.verse_ref import VerseRef
from machine.corpora.text_row import TextRow
from machine.corpora.usfm_parser_state import UsfmParserState
from machine.corpora.usfm_token import UsfmToken
from machine.corpora.usfm_token import UsfmTokenType
from machine.corpora.scripture_ref import ScriptureRef

from machine.corpora.usfm_text_base import UsfmTextBase
from machine.corpora.usfm_text_base import _TextRowCollector


class ModifiedTextRowCollector(_TextRowCollector):

    def __init__(self, text: UsfmTextBase, psalm_superscription_tag: str = "d") -> None:
        super().__init__(text)
        self._psalm_superscription_tag = psalm_superscription_tag
        self._in_psalm_superscription = False
        self._verse_0_created = False

    def start_para(
        self,
        state: UsfmParserState,
        marker: str,
        unknown: bool,
        attributes,
    ) -> None:
        is_superscription = (
            marker == self._psalm_superscription_tag
            and state.verse_ref.book == "PSA"
            and state.verse_ref.bbbcccvvvs not in ("019119000", "019107000")
        )

        #if self._in_psalm_superscription and not is_superscription:
        #    self.verse(state, "0", "v", None, None)
        #    self._in_psalm_superscription = False

        if is_superscription:
            self._in_psalm_superscription = True
        
        super().start_para(state, marker, unknown, attributes)

    def end_para(self, state: UsfmParserState, marker: str) -> None:
        if marker == self._psalm_superscription_tag:#
            self._in_psalm_superscription = False#

        super().end_para(state, marker)

    def text(self, state: UsfmParserState, text: str) -> None:

        if self._in_psalm_superscription and state.note_tag is None:

            self._row_texts_stack.append("")
            self._row_texts_stack[-1] += text
            self.verse(state, "0", "v", None, None)#

        super().text(state, text)
