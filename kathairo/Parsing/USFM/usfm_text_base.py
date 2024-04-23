from abc import abstractmethod
from io import TextIOWrapper
from typing import Generator, Iterable, List, Optional, Sequence

from machine.scripture.verse_ref import Versification
from machine.corpora.corpora_utils import gen
from machine.corpora.scripture_text import ScriptureText
from machine.corpora.stream_container import StreamContainer
from machine.corpora.text_row import TextRow
from machine.corpora.usfm_parser import parse_usfm
from machine.corpora.usfm_parser_handler import UsfmParserHandler
from machine.corpora.usfm_stylesheet import UsfmStylesheet
from machine.corpora.usfm_parser_handler import UsfmParserHandler
from machine.corpora.usfm_text_base import _TextRowCollector

class UsfmTextBase(ScriptureText):
    def __init__(
        self,
        id: str,
        stylesheet: UsfmStylesheet,
        encoding: str,
        handler: UsfmParserHandler,
        versification: Optional[Versification],
        include_markers: bool,
    ) -> None:
        super().__init__(id, versification)

        self._stylesheet = stylesheet
        self._encoding = encoding
        self.handler = handler
        self._include_markers = include_markers

    @abstractmethod
    def _create_stream_container(self) -> StreamContainer:
        ...

    def _get_rows(self) -> Generator[TextRow, None, None]:
        usfm = self._read_usfm()
        row_collector = _TextRowCollector(self)
        if(self.handler is not None):
            row_collector = self.handler(self)
        parse_usfm(usfm, row_collector, self._stylesheet, self.versification, preserve_whitespace=self._include_markers)
        return gen(row_collector.rows)

    def _read_usfm(self) -> str:
        with self._create_stream_container() as stream_container, TextIOWrapper(
            stream_container.open_stream(), encoding=self._encoding, errors="replace"
        ) as reader:
            return reader.read()