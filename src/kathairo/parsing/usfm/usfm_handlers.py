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
    """
    Custom text row collector that handles psalm superscriptions as verse 0.

    This extends the base _TextRowCollector to detect psalm superscription paragraphs
    (marked with the 'd' tag by default) and treat them as verse 0, allowing them
    to be included in the text output.
    """

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
        # Check if this is a psalm superscription paragraph
        is_superscription = (
            marker == self._psalm_superscription_tag
            and state.verse_ref.book == "PSA"
            and state.verse_ref.bbbcccvvvs not in ("019119000", "019107000")
        )

        if is_superscription:
            # Mark that we're in a psalm superscription
            self._in_psalm_superscription = True
            self._verse_0_created = False

        # Call parent to handle the rest
        super().start_para(state, marker, unknown, attributes)

    def end_para(self, state: UsfmParserState, marker: str) -> None:
        # Reset superscription flag when leaving the paragraph
        if marker == self._psalm_superscription_tag:
            self._in_psalm_superscription = False
            self._verse_0_created = False

        super().end_para(state, marker)

    def text(self, state: UsfmParserState, text: str) -> None:
        # If we're in a psalm superscription, handle it specially
        if self._in_psalm_superscription:
            # First time we see text in a superscription, set up verse 0
            if not self._verse_0_created and len(self._row_texts_stack) == 0:
                # Manually set up the stack and create verse 0
                self._row_texts_stack.append("")
                self.verse(state, "0", "v", None, None)
                self._verse_0_created = True

            # Now manually add the text to the stack (bypassing parent's is_verse_text check)
            if len(self._row_texts_stack) > 0 and len(text) > 0:
                row_text = self._row_texts_stack[-1]

                # Handle whitespace stripping like the parent does
                if (
                    state.prev_token is not None
                    and state.prev_token.type == UsfmTokenType.END
                    and (len(row_text) == 0 or row_text[-1].isspace())
                ):
                    text = text.lstrip()

                self._row_texts_stack[-1] += text
            return  # Don't call parent since we handled it

        # For non-superscription text, use parent's handling
        super().text(state, text)
