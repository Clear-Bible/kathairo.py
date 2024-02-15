import csv
from Tokenization import MaximalMatchingTokenizer
from Tokenization import ChineseBibleWordTokenizer
from machine.utils import string_utils
from machine.corpora import UsxFileTextCorpus
from machine.corpora import ParatextTextCorpus, UsfmFileTextCorpus, UsxFileTextCorpus
from machine.tokenization import LatinWordTokenizer, WhitespaceTokenizer
from machine.scripture import (
    ENGLISH_VERSIFICATION,
    ORIGINAL_VERSIFICATION,
    RUSSIAN_ORTHODOX_VERSIFICATION,
    RUSSIAN_PROTESTANT_VERSIFICATION,
    SEPTUAGINT_VERSIFICATION,
    VULGATE_VERSIFICATION,
    LAST_BOOK,
    ValidStatus,
    VerseRef,
    Versification,
    get_bbbcccvvv,
)
import argparse

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("-sv", "--sourceVersificationPath", type=str) #optional
argumentParser.add_argument("-tv", "--targetVersificationPath", type=str, required=True)

corpusGroup = argumentParser.add_mutually_exclusive_group(required=True)
corpusGroup.add_argument("-uf", "--targetUsfmCorpusPath", type=str)
corpusGroup.add_argument("-ux", "--targetUsxCorpusPath", type=str)

tokenizerGroup = argumentParser.add_mutually_exclusive_group(required=True)
tokenizerGroup.add_argument("-zh", "--chineseTokenizer", action='store_true')
tokenizerGroup.add_argument("-lt", "--latinTokenizer", action='store_true')

argumentParser.add_argument("-of", "--oldTsvFormat", action='store_true') #optional

args = argumentParser.parse_args()

print(args.sourceVersificationPath)
print(args.targetVersificationPath)
print(args.targetUsfmCorpusPath)
print(args.targetUsxCorpusPath)
print(args.chineseTokenizer)
print(args.latinTokenizer)
print(args.oldTsvFormat)

sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)

targetVersification = Versification.load(args.targetVersificationPath, fallback_name="web")

if(args.targetUsfmCorpusPath is not None):
    corpus = UsfmFileTextCorpus(args.targetUsfmCorpusPath, versification = targetVersification)
if(args.targetUsxCorpusPath is not None):
    corpus = UsxFileTextCorpus(args.targetUsxCorpusPath, versification = targetVersification)

if(args.chineseTokenizer is not None):
    tokenizer = ChineseBibleWordTokenizer.ChineseBibleWordTokenizer()
if(args.latinTokenizer is not None):
    tokenizer = LatinWordTokenizer()
    
#BSB
#targetVersification = Versification.load("./resources/bsb_usx/release/versification.vrs", fallback_name="web")
#sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
#corpus = UsfmFileTextCorpus("./resources/bsb_usfm", versification = targetVersification)
#corpus = UsxFileTextCorpus("./resources/bsb_usx/release/USX_1", versification = targetVersification)
#tokenizer = LatinWordTokenizer()

#OCCB-Simplified
#targetVersification = Versification.load("./resources/occb_simplified_usx/release/versification.vrs", fallback_name="web")
#sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
#corpus = UsxFileTextCorpus("./resources/occb_simplified_usx/release/USX_1", versification = targetVersification)
#tokenizer = ChineseBibleWordTokenizer.ChineseBibleWordTokenizer()

#ONAV
#targetVersification = Versification.load("./resources/onav_usx/release/versification.vrs", fallback_name="web")
#sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
#corpus = UsxFileTextCorpus("./resources/onav_usx/release/USX_1", versification = targetVersification)
#tokenizer = LatinWordTokenizer()

#VanDyck
#targetVersification = Versification(name = "targetVersification", base_versification=ENGLISH_VERSIFICATION)
#sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
#corpus = UsfmFileTextCorpus("./resources/arb-vd_usfm", versification = targetVersification)
#tokenizer = LatinWordTokenizer()

#YLT
#targetVersification = Versification(name = "targetVersification", base_versification=ENGLISH_VERSIFICATION)
#sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
#corpus = UsfmFileTextCorpus("./resources/engylt_usfm", versification = targetVersification)
#tokenizer = LatinWordTokenizer()

with open('output.tsv', 'w', newline='', encoding='utf-8') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')

    if(args.oldTsvFormat):
        tsv_writer.writerow(["id", "target_verse", "token"]) #OLD WAY
    else:
        tsv_writer.writerow(["id", "source_verse", "token"]) #NEXT GEN

    for row in corpus.tokenize(tokenizer).nfc_normalize():    
        
        #print(f"{row.ref}: {row.text}")

        targetVref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, targetVersification) #dependent on which .vrs is being used
        targetVref.change_versification(sourceVersification)
        
        sourceVref = targetVref

        wordIndex = 1
        for token in row.segment:
            wordIndexStr = str(wordIndex).zfill(3)

            if(args.oldTsvFormat):
                tsv_writer.writerow([f"{sourceVref.bbbcccvvvs}{wordIndexStr}", f"{row.ref.bbbcccvvvs}", token ]) #OLD WAY
            else:
                tsv_writer.writerow([f"{row.ref.bbbcccvvvs}{wordIndexStr}", f"{sourceVref.bbbcccvvvs}", token ]) #NEXT GEN
            
            wordIndex += 1




















#What punctuation data can we get from machine?
    #a tokenized verse is just returned as an array so there's no accompanying data to signify that a token is punctuation. 
    #there is a is_punctuation method we could use though
#Is there USFM validation?
    #I don't seen any tools for it, and when I fed it USFM with faulty and duplicate verses it just ignored the errors
#What kind of versification data can we get to enrich the current alignment data structures?
    #VerseRef.change_versification, which translates a verse ref into it's equivalent in another versification scheme
    #various tools of comparing verses from different versification (equality, >, <)
            

#rename Project
#publish to GitHub
#scripture burrito alignment format

"""

for text in corpus.texts:
    print(text.id)
    print("======")
    for row in text.take(3):
        verse_ref = row.ref
        chapter_verse = f"{verse_ref.chapter}:{verse_ref.verse}"
        print(f"{chapter_verse}: {row.text}")
    print()

"""