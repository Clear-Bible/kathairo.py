from typing import Optional

from machine.scripture.verse_ref import Versification
from machine.utils.typeshed import StrPath
from machine.corpora.usx_file_text_corpus import UsxFileTextCorpus as _UsxFileTextCorpus
from kathairo.parsing.usx.usx_verse_parser import ModifiedUsxVerseParser


class UsxFileTextCorpus(_UsxFileTextCorpus):
    def __init__(
        self,
        project_dir: StrPath,
        versification: Optional[Versification] = None,
    ) -> None:
        super().__init__(project_dir, versification)
        for text in self.texts:
            text._parser = ModifiedUsxVerseParser()
