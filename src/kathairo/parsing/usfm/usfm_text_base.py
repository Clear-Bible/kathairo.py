from typing import Generator, Optional

from machine.scripture.verse_ref import Versification
from machine.corpora.corpora_utils import gen
from machine.corpora.text_row import TextRow
from machine.corpora.usfm_parser import parse_usfm
from machine.corpora.usfm_parser_handler import UsfmParserHandler
from machine.corpora.usfm_stylesheet import UsfmStylesheet
from machine.corpora.usfm_parser_handler import UsfmParserHandler
from machine.corpora.usfm_text_base import _TextRowCollector
from machine.corpora.usfm_text_base import UsfmTextBase

class ModifiedUsfmTextBase(UsfmTextBase):
    def __init__(
        self,
        id: str,
        stylesheet: UsfmStylesheet,
        encoding: str,
        handler: UsfmParserHandler,
        psalmSuperscriptionTag: str,
        include_headers: bool,
        versification: Optional[Versification],
        include_markers: bool,
    ) -> None:
        super().__init__(id, stylesheet, encoding, versification, include_markers)

        self._stylesheet = stylesheet
        self._encoding = encoding
        self.handler = handler #passes in handler
        self.psalm_superscription_tag = psalmSuperscriptionTag
        self.include_headers = include_headers
        self._include_markers = include_markers

    def _get_rows(self) -> Generator[TextRow, None, None]:
        usfm = self._read_usfm()
        row_collector = _TextRowCollector(self)
        if(self.handler is not None): #uses handler if not None
            row_collector = self.handler(self, psalm_superscription_tag = self.psalm_superscription_tag, include_headers = self.include_headers)
        parse_usfm(usfm, row_collector, self._stylesheet, self.versification, preserve_whitespace=self._include_markers)
        return gen(row_collector.rows)