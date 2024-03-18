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
from biblelib.word import fromubs
import re

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


#'''
argumentParser = argparse.ArgumentParser()

#add a parameter for source versification

argumentParser.add_argument("-n", "--projectName", type=str, required=True)

#add bunch of parameters for the default versification schemes included in machine and make target versification a mutually exclusive argument group
argumentParser.add_argument("-tv", "--targetVersificationPath", type=str, required=True)

corpusGroup = argumentParser.add_mutually_exclusive_group(required=True)
corpusGroup.add_argument("-uf", "--targetUsfmCorpusPath", type=str)
corpusGroup.add_argument("-ux", "--targetUsxCorpusPath", type=str)

tokenizerGroup = argumentParser.add_mutually_exclusive_group(required=True)
tokenizerGroup.add_argument("-zh", "--chineseTokenizer", action='store_true')
tokenizerGroup.add_argument("-lt", "--latinTokenizer", action='store_true')

argumentParser.add_argument("-of", "--oldTsvFormat", action='store_true') #optional

args = argumentParser.parse_args()

#print(args.targetVersificationPath)
#print(args.targetUsfmCorpusPath)
#print(args.targetUsxCorpusPath)
#print(args.chineseTokenizer)
#print(args.latinTokenizer)
#print(args.oldTsvFormat)

projectName = args.projectName

sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)

targetVersification = Versification.load(args.targetVersificationPath, fallback_name="web")

if(args.targetUsfmCorpusPath is not None):
    corpus = UsfmFileTextCorpus(args.targetUsfmCorpusPath, versification = targetVersification)
if(args.targetUsxCorpusPath is not None):
    corpus = UsxFileTextCorpus(args.targetUsxCorpusPath, versification = targetVersification)

if(args.chineseTokenizer == True):
    tokenizer = ChineseBibleWordTokenizer.ChineseBibleWordTokenizer()
if(args.latinTokenizer == True):
    tokenizer = LatinWordTokenizer()
    
#'''
#def CorpusToTsv(targetVersification, sourceVersification, corpus, tokenizer):

tsvFormatString = "new"
if(args.oldTsvFormat):
    tsvFormatString = "old"

outputFileName = "TSVs/target_"+projectName+"_"+tsvFormatString+".tsv"

with open(outputFileName, 'w', newline='', encoding='utf-8') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')

    if(args.oldTsvFormat):
        tsv_writer.writerow(["id", "target_verse", "text"]) #OLD WAY
    else:
        tsv_writer.writerow(["id", "source_verse", "text"]) #NEXT GEN

    for row in corpus:#.tokenize(tokenizer).nfc_normalize():    
        
        #if(row.ref.bbbcccvvvs[:6] == "003006"):
        #    vaeresTwo= True
            
        if(row.is_in_range and row.text == ''):
            tokenized_row = tokenizer.tokenize((row.text + " <RANGE>"))
        else:
            tokenized_row = tokenizer.tokenize(row.text)
        
        #print(f"{row.ref}: {row.text}")

        targetVref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, targetVersification) #dependent on which .vrs is being used
        targetVref.change_versification(sourceVersification)
        
        sourceVref = targetVref

        wordIndex = 1
        for token in tokenized_row:
            wordIndexStr = str(wordIndex).zfill(3)

            sourceBcv = fromubs(f"{re.sub(r'[^0-9]', '', sourceVref.bbbcccvvvs)}00000").to_bcvid
            rowBcv= fromubs(f"{re.sub(r'[^0-9]', '', row.ref.bbbcccvvvs)}00000").to_bcvid
            
            if(args.oldTsvFormat):
                tsv_writer.writerow([f"{sourceBcv}{wordIndexStr}", f"{rowBcv}", token ]) #OLD WAY
            else:
                tsv_writer.writerow([f"{rowBcv}{wordIndexStr}", f"{sourceBcv}", token ]) #NEXT GEN
            
            wordIndex += 1