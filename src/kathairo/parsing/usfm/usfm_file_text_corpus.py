from pathlib import Path
from typing import List, Optional

from machine.scripture import ENGLISH_VERSIFICATION
from machine.scripture.verse_ref import Versification
from machine.utils.typeshed import StrPath
from machine.corpora.scripture_text_corpus import ScriptureTextCorpus
from machine.corpora.usfm_file_text import UsfmFileText
from machine.corpora.usfm_file_text_corpus import _get_id
from machine.corpora.usfm_parser_handler import UsfmParserHandler
from machine.corpora.usfm_stylesheet import UsfmStylesheet
from kathairo.parsing.usfm.usfm_text_base import ModifiedUsfmTextMixin


class ModifiedUsfmFileText(ModifiedUsfmTextMixin, UsfmFileText):
    def __init__(self, *args, handler: UsfmParserHandler, psalm_superscription_tag: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.handler = handler
        self.psalm_superscription_tag = psalm_superscription_tag


class UsfmFileTextCorpus(ScriptureTextCorpus):
    def __init__(
        self,
        project_dir: StrPath,
        handler: UsfmParserHandler,
        psalmSuperscriptionTag: str,
        stylesheet_filename: StrPath = "usfm.sty",
        encoding: str = "utf-8-sig",
        versification: Optional[Versification] = None,
        include_markers: bool = False,
        file_pattern: str = "*.SFM",
    ) -> None:
        if versification is None:
            versification = ENGLISH_VERSIFICATION
        stylesheet = UsfmStylesheet(stylesheet_filename)
        texts: List[ModifiedUsfmFileText] = []
        for sfm_filename in Path(project_dir).glob(file_pattern):
            id = _get_id(sfm_filename, encoding)
            if id:
                texts.append(
                    ModifiedUsfmFileText(
                        stylesheet,
                        encoding,
                        id,
                        sfm_filename,
                        versification,
                        include_markers,
                        handler=handler,
                        psalm_superscription_tag=psalmSuperscriptionTag,
                    )
                )
        super().__init__(versification, texts)
