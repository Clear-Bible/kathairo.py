from typing import Iterable, List, Optional

from machine.scripture.verse_ref import VerseRef
from machine.corpora.text_row import TextRow
from machine.corpora.usfm_parser_state import UsfmParserState
from machine.corpora.usfm_token import UsfmToken, UsfmTokenType

from machine.corpora.usfm_text_base import UsfmTextBase
from machine.corpora.usfm_text_base import _TextRowCollector

class ModifiedTextRowCollector(_TextRowCollector):
    def __init__(self, text: UsfmTextBase) -> None:
        self._text = text
        self._rows: List[TextRow] = []
        self._verse_text = ""
        self._next_para_tokens: List[UsfmToken] = []
        self._verse_ref: Optional[VerseRef] = None
        self._sentence_start: bool = False
        self._next_para_text_started = False

    @property
    def rows(self) -> Iterable[TextRow]:
        return self._rows

    def text(self, state: UsfmParserState, text: str) -> None:
        if(state.verse_ref.book == "PSA" and state.verse_ref.chapter == "142"):
            stop = True
        
        #includes superscription text
        if(state.prev_token is not None and (state.prev_token.marker == "s" or state.prev_token.marker == "d") and state.verse_ref.book == "PSA" and state.verse_ref.bbbcccvvvs != "019119000"):
            if self is not None:
                self.verse(state, 0, "v", 0, 0)
        
        if self._verse_ref is None or not state.is_verse_para:# and state.prev_token.marker != "s"):
            return

        if self._text._include_markers:
            text = text.rstrip("\r\n")
            if len(text) > 0:
                if not text.isspace():
                    for token in self._next_para_tokens:
                        self._verse_text += str(token)
                    self._next_para_tokens.clear()
                    self._next_para_text_started = True
                self._verse_text += text
        elif state.is_verse_text and len(text) > 0:
            if (
                state.prev_token is not None
                and state.prev_token.type == UsfmTokenType.END
                and (self._verse_text == "" or self._verse_text[-1].isspace())
            ):
                text = text.lstrip()
            self._verse_text += text