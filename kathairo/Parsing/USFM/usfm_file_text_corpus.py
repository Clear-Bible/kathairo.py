from pathlib import Path
from typing import List, Optional

from machine.scripture.verse_ref import Versification, VersificationType
from machine.utils.typeshed import StrPath
from machine.corpora.scripture_text_corpus import ScriptureTextCorpus
from .usfm_file_text import UsfmFileText
from machine.corpora.usfm_stylesheet import UsfmStylesheet
from machine.corpora.usfm_parser_handler import UsfmParserHandler

class UsfmFileTextCorpus(ScriptureTextCorpus):
    def __init__(
        self,
        project_dir: StrPath,
        handler:UsfmParserHandler,
        stylesheet_filename: StrPath = "usfm.sty",
        encoding: str = "utf-8-sig",
        versification: Optional[Versification] = None,
        include_markers: bool = False,
        file_pattern: str = "*.SFM",
    ) -> None:
        if versification is None:
            versification = Versification.get_builtin(VersificationType.ENGLISH)
        stylesheet = UsfmStylesheet(stylesheet_filename)
        texts: List[UsfmFileText] = []
        for sfm_filename in Path(project_dir).glob(file_pattern):
            texts.append(UsfmFileText(stylesheet, encoding, sfm_filename, handler, versification, include_markers))
        super().__init__(versification, texts)
