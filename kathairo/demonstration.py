from Tokenization import ChineseBibleWordTokenizer
from machine.corpora import UsxFileTextCorpus
from machine.corpora import UsfmFileTextCorpus, UsxFileTextCorpus
from machine.tokenization import LatinWordTokenizer
from machine.scripture import (
    ENGLISH_VERSIFICATION,
    Versification
)

targetVersification = Versification.load("./resources/bsb_usx/release/versification.vrs", fallback_name="web")
corpus = UsfmFileTextCorpus("./resources/bsb_usfm", versification = targetVersification, include_markers=True)
tokenizer = LatinWordTokenizer()

row = corpus.get_rows

for row in corpus:
    tokenized_row = tokenizer.tokenize(row.text)
    if(row.ref.bbbcccvvvs[:6] == "019003"):
        print(row)

targetVersification = Versification.load("./resources/occb_simplified_usx/release/versification.vrs", fallback_name="web")
corpus = UsxFileTextCorpus("./resources/occb_simplified_usx/release/USX_1", versification = targetVersification)

for row in corpus:
    if(row.ref.bbbcccvvvs[:6] == "003006"):
        print(row)