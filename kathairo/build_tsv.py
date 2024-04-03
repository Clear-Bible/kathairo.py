import csv
from Tokenization import MaximalMatchingTokenizer, ChineseBibleWordTokenizer
from Tokenization.latin_whitespace_included_tokenizer import LatinWhitespaceIncludedWordTokenizer
from machine.tokenization import LatinWordTokenizer, WhitespaceTokenizer
from machine.corpora import UsfmFileTextCorpus, UsxFileTextCorpus, ScriptureTextCorpus
from machine.scripture import (
    ENGLISH_VERSIFICATION,
    ORIGINAL_VERSIFICATION,
    RUSSIAN_ORTHODOX_VERSIFICATION,
    RUSSIAN_PROTESTANT_VERSIFICATION,
    SEPTUAGINT_VERSIFICATION,
    VULGATE_VERSIFICATION,
    VerseRef,
    Versification,
)
from biblelib.word import fromubs
import re
from helpers.strings import is_unicode_punctuation

def corpus_to_verse_level_tsv(targetVersification:Versification, sourceVersification:Versification, corpus:ScriptureTextCorpus, tokenizer:WhitespaceTokenizer, 
                              project_name:str, use_old_tsv_format:bool = False, excludeBracketedText:bool = False):

    tsvFormatString = "new"
    if(use_old_tsv_format):
        tsvFormatString = "old"
        
    outputFileName = "VerseText/target_"+project_name+"_"+tsvFormatString+".tsv"

    with open(outputFileName, 'w', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        if(use_old_tsv_format):
            tsv_writer.writerow(["id", "target_verse", "text"]) #OLD WAY
        else:
            tsv_writer.writerow(["id", "source_verse", "text"]) #NEXT GEN

        for row in corpus:#.tokenize(tokenizer).nfc_normalize()    

            targetVref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, targetVersification) #dependent on which .vrs is being used
            targetVref.change_versification(sourceVersification)
            
            sourceVref = targetVref

            sourceBcv = fromubs(f"{re.sub(r'[^0-9]', '', sourceVref.bbbcccvvvs)}00000").to_bcvid
            rowBcv= fromubs(f"{re.sub(r'[^0-9]', '', row.ref.bbbcccvvvs)}00000").to_bcvid
            
            if(use_old_tsv_format):
                tsv_writer.writerow([f"{sourceBcv}", f"{rowBcv}", row.text ]) #OLD WAY
            else:
                tsv_writer.writerow([f"{rowBcv}", f"{sourceBcv}", row.text ]) #NEXT GEN

def corpus_to_word_level_tsv(targetVersification:Versification, sourceVersification:Versification, corpus:ScriptureTextCorpus, tokenizer:WhitespaceTokenizer, 
                  project_name:str, use_old_tsv_format:bool = False, excludeBracketedText:bool = False):

    tsvFormatString = "new"
    if(use_old_tsv_format):
        tsvFormatString = "old"

    outputFileName = "TSVs/target_"+project_name+"_"+tsvFormatString+".tsv"

    with open(outputFileName, 'w', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        if(use_old_tsv_format):
            tsv_writer.writerow(["id", "target_verse", "text", "skip_space_after", "exclude"]) #OLD WAY
        else:
            tsv_writer.writerow(["id", "source_verse", "text", "skip_space_after", "exclude"]) #NEXT GEN

        in_brackets = False
        for row in corpus.tokenize(tokenizer):#.tokenize(tokenizer).nfc_normalize() #Include for Double Tokenization    

            #if(row.is_in_range and row.text == ''):
            #    tokenized_row = tokenizer.tokenize((row.text + " <RANGE>"))
            #else:
            #    tokenized_row = tokenizer.tokenize(row.text) # Include for Double Tokenization
            
            #print(f"{row.ref}: {row.text}")

            targetVref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, targetVersification) #dependent on which .vrs is being used
            targetVref.change_versification(sourceVersification)
            
            sourceVref = targetVref

            wordIndex = 1
            
            for index in range(len(row.segment)):
            #for token in row.segment:#row.segment, tokenized_row:
            
                skip_space_after = ""
                
                if(not in_brackets):
                    exclude = ""
                else:
                    exclude = "y"
                    
                token = row.segment[index]
                
                next_token = None
                max_segment_index = len(row.segment) - 1
                if(index + 1 <= max_segment_index):
                    next_token = row.segment[index + 1]
                else:
                    next_token = ' ' #assume a space between verses
                    
                if(token==' '):
                    continue
                else:
                    if(not next_token==' '):
                        skip_space_after = "y"
        
                if(is_unicode_punctuation(token[0])):
                    exclude = "y"
                    
                if(token[0] == '[' and excludeBracketedText):
                    in_brackets = True
                    exclude = "y"
                
                wordIndexStr = str(wordIndex).zfill(3)

                sourceBcv = fromubs(f"{re.sub(r'[^0-9]', '', sourceVref.bbbcccvvvs)}00000").to_bcvid
                rowBcv= fromubs(f"{re.sub(r'[^0-9]', '', row.ref.bbbcccvvvs)}00000").to_bcvid
                
                #if(f"{rowBcv}{wordIndexStr}" == "43005003017"):
                #    something = True
                
                if(use_old_tsv_format):
                    tsv_writer.writerow([f"{sourceBcv}{wordIndexStr}", f"{rowBcv}", token, skip_space_after, exclude ]) #OLD WAY
                else:
                    tsv_writer.writerow([f"{rowBcv}{wordIndexStr}", f"{sourceBcv}", token, skip_space_after, exclude ]) #NEXT GEN
                
                wordIndex += 1
                
                if(token[0] ==']'):
                    in_brackets = False

if(__name__ == "__main__"):
    #BSB
    targetVersification = Versification.load("./resources/bsb_usx/release/versification.vrs", fallback_name="web")
    sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    corpus = UsfmFileTextCorpus("./resources/bsb_usfm", versification = targetVersification)
    tokenizer = LatinWhitespaceIncludedWordTokenizer()
    project_name = "BSB"
    excludeBracketedText = False

    #OCCB-Simplified
    #targetVersification = Versification.load("./resources/occb_simplified_usx/release/versification.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsxFileTextCorpus("./resources/occb_simplified_usx/release/USX_1", versification = targetVersification)
    #tokenizer = ChineseBibleWordTokenizer.ChineseBibleWordTokenizer()
    #project_name = "OCCB-simplified"

    #ONAV
    #targetVersification = Versification.load("./resources/onav_usx/release/versification.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsxFileTextCorpus("./resources/onav_usx/release/USX_1", versification = targetVersification)
    #tokenizer = LatinWhitespaceIncludedWordTokenizer()
    #project_name = "ONAV"

    #VanDyck
    #targetVersification = Versification(name = "targetVersification", base_versification=ENGLISH_VERSIFICATION)
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsfmFileTextCorpus("./resources/arb-vd_usfm", versification = targetVersification)
    #tokenizer = LatinWordTokenizer()

    #YLT
    #targetVersification = Versification(name = "targetVersification", base_versification=ENGLISH_VERSIFICATION)
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsfmFileTextCorpus("./resources/engylt_usfm", versification = targetVersification)
    #tokenizer = LatinWordTokenizer(treat_apostrophe_as_single_quote=True)
    #project_name = "YLT"

    #ONEN
    #targetVersification = Versification.load("./resources/onen_usx/release/versification.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsfmFileTextCorpus("./resources/onen_usfm", versification = targetVersification)
    #tokenizer = LatinWhitespaceIncludedWordTokenizer()
    #project_name = "ONEN"

    #RSB
    #targetVersification = Versification(name = "targetVersification", base_versification=RUSSIAN_PROTESTANT_VERSIFICATION)
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsfmFileTextCorpus("./resources/ru_rsb", versification = targetVersification)
    #tokenizer = LatinWhitespaceIncludedWordTokenizer()
    #project_name = "RSB"
    #excludeBracketedText = True
    
    #RSB-SYNO
    #targetVersification = Versification.load("./resources/versification/rso.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsfmFileTextCorpus("./resources/syno_ulb_ru", versification = targetVersification)
    #tokenizer = LatinWordTokenizer()
    #project_name="RSB-SYNO"

    corpus_to_word_level_tsv(targetVersification, sourceVersification, corpus, tokenizer, project_name, excludeBracketedText=excludeBracketedText)
    #corpus_to_verse_level_tsv(targetVersification, sourceVersification, corpus, tokenizer, project_name)