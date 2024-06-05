from Tokenization import ChineseBibleWordTokenizer
from machine.corpora import UsxFileTextCorpus
from machine.corpora import UsfmFileTextCorpus, UsxFileTextCorpus
from machine.tokenization import LatinWordTokenizer
from machine.scripture import (
    ENGLISH_VERSIFICATION,
    Versification
)
from Tokenization.latin_whitespace_included_tokenizer import LatinWhitespaceIncludedWordTokenizer
from machine.corpora import UsfmStylesheet
from machine.corpora import UsfmTokenizer, UsfmTokenType
from machine.corpora import UsfmParser
from machine.corpora import UsfmParserHandler
import os
import csv

targetVersification = Versification.load("./resources/arb/onav_usx/release/versification.vrs", fallback_name="web")
corpus = UsxFileTextCorpus("./resources/arb/onav_usx/release/USX_1", versification = targetVersification)
tokenizer = LatinWhitespaceIncludedWordTokenizer()

with open("arabic-tokenization", 'w', newline='', encoding='utf-8') as out_file:
  tsv_writer = csv.writer(out_file, delimiter='\t')

  for row in corpus:
      tokenized_row = tokenizer.tokenize(row.text)
      for token in tokenized_row:
        tsv_writer.writerow([token])