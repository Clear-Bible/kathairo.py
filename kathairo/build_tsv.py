import csv
from Tokenization import MaximalMatchingTokenizer, ChineseBibleWordTokenizer
from Tokenization.latin_whitespace_included_tokenizer import LatinWhitespaceIncludedWordTokenizer
from machine.tokenization import LatinWordTokenizer, WhitespaceTokenizer
from machine.corpora import ScriptureTextCorpus
from Parsing.USX.usx_file_text_corpus import UsxFileTextCorpus
from Parsing.USFM.usfm_file_text_corpus import UsfmFileTextCorpus
#from machine.corpora import UsfmFileTextCorpus, UsxFileTextCorpus, ScriptureTextCorpus
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
from Parsing.USFM.usfm_handlers import ModifiedTextRowCollector
from helpers.paths import get_target_file_location
import os

def corpus_to_verse_level_tsv(targetVersification:Versification, sourceVersification:Versification, corpus:ScriptureTextCorpus, tokenizer:WhitespaceTokenizer, 
                              project_name:str, language:str, excludeBracketedText:bool = False):

    outputFileName = get_target_file_location("VerseText", project_name, language)

    os.makedirs(os.path.dirname(outputFileName), exist_ok=True)
    with open(outputFileName, 'w', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        tsv_writer.writerow(["id", "source_verse", "text","id_range_end", "source_verse_range_end"])
        verse_range_list = []

        for row in corpus:#.tokenize(tokenizer).nfc_normalize()    

            targetVref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, targetVersification) #dependent on which .vrs is being used
            targetVref.change_versification(sourceVersification)
            
            sourceVref = targetVref

            if(not row.is_in_range or row.is_range_start):
                for verse_range_row in verse_range_list:
                    verse_range_row.append(f"{rowBcv}")
                    verse_range_row.append(f"{sourceBcv}")
                    tsv_writer.writerow(verse_range_row)
                verse_range_list.clear()

            sourceBcv = fromubs(f"{re.sub(r'[^0-9]', '', sourceVref.bbbcccvvvs)}00000").to_bcvid
            rowBcv= fromubs(f"{re.sub(r'[^0-9]', '', row.ref.bbbcccvvvs)}00000").to_bcvid
            
            if(row.text != "" and row.is_in_range):
                verse_range_list.append([f"{rowBcv}", f"{sourceBcv}", row.text])
            elif(row.text != ""):
                tsv_writer.writerow([f"{rowBcv}", f"{sourceBcv}", row.text, "", ""])

def corpus_to_word_level_tsv(targetVersification:Versification, sourceVersification:Versification, corpus:ScriptureTextCorpus, tokenizer:WhitespaceTokenizer, 
                  project_name:str, language:str, excludeBracketedText:bool = False):

    outputFileName = get_target_file_location("TSVs", project_name, language)

    os.makedirs(os.path.dirname(outputFileName), exist_ok=True)
    with open(outputFileName, 'w', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        tsv_writer.writerow(["id", "source_verse", "text", "skip_space_after", "exclude", "id_range_end", "source_verse_range_end"])

        in_brackets = False
        verse_range_list = []
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
            
            if(not row.is_in_range or row.is_range_start):
                for verse_range_row in verse_range_list:
                    verse_range_row.append(f"{rowBcv}")
                    verse_range_row.append(f"{sourceBcv}")
                    tsv_writer.writerow(verse_range_row)
                verse_range_list.clear()
            
            sourceBcv = fromubs(f"{re.sub(r'[^0-9]', '', sourceVref.bbbcccvvvs)}00000").to_bcvid
            rowBcv= fromubs(f"{re.sub(r'[^0-9]', '', row.ref.bbbcccvvvs)}00000").to_bcvid
            
            for index in range(len(row.segment)):
            #for token in row.segment:#row.segment, tokenized_row:
            
                token = row.segment[index]
                
                next_token = None
                max_segment_index = len(row.segment) - 1
                if(index + 1 <= max_segment_index):
                    next_token = row.segment[index + 1]
                else:
                    next_token = ' ' #assume a space between verses
                    
                skip_space_after = ""
                    
                if(token==' '):
                    continue
                else:
                    if(not next_token==' '):
                        skip_space_after = "y"

                if(not in_brackets):
                    exclude = ""
                else:
                    exclude = "y"
                    
                exclude = "y"
                for char in token:
                    if(not in_brackets and not is_unicode_punctuation(char)):
                        exclude = ""
                        break
                
                if(token == '[' and excludeBracketedText): #we are trusting that all brackets get their own row
                    in_brackets = True
                    exclude = "y"
                
                if(token ==']'): #we are trusting that all brackets get their own row
                    in_brackets = False

                wordIndexStr = str(wordIndex).zfill(3)
                
                if(row.text != "" and row.is_in_range):
                    verse_range_list.append([f"{rowBcv}{wordIndexStr}", f"{sourceBcv}", token, skip_space_after, exclude])
                elif(row.text != ""):
                        tsv_writer.writerow([f"{rowBcv}{wordIndexStr}", f"{sourceBcv}", token, skip_space_after, exclude, "", ""])
                
                wordIndex += 1
                

if(__name__ == "__main__"):
    #BSB
    #targetVersification = Versification.load("./resources/eng/bsb_usfm/versification.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsfmFileTextCorpus("./resources/eng/bsb_usfm", handler=ModifiedTextRowCollector, versification = targetVersification)
    #language = "eng"
    #tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    #project_name = "BSB"
    #excludeBracketedText = False

    #OCCB-Simplified
    #targetVersification = Versification.load("./resources/man/occb_simplified_usx/release/versification.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsxFileTextCorpus("./resources/man/occb_simplified_usx/release/USX_1", versification = targetVersification)
    #tokenizer = ChineseBibleWordTokenizer.ChineseBibleWordTokenizer()
    #project_name = "OCCB-simplified"
    #excludeBracketedText = False
    #language="man"

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
    
    #IRV
    targetVersification = Versification.load("./resources/hin/IRVHin/versification.vrs", fallback_name="web")
    sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    corpus = UsfmFileTextCorpus("./resources/hin/IRVHin", versification = targetVersification, handler=ModifiedTextRowCollector)
    language="hin"
    tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    project_name="IRVHin"
    excludeBracketedText = False
    
    #LSG
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #project_name="LSG"
    #targetVersification = Versification.load("./resources/fra/fra-LSG_usfm/versification.vrs", fallback_name="web")
    #corpus = UsfmFileTextCorpus("./resources/fra/fra-LSG_usfm", versification = targetVersification, handler=ModifiedTextRowCollector)
    #language = "fra"
    #tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    #excludeBracketedText = False
    
    #IRVBen
    #targetVersification = Versification.load("./resources/ben/IRVBen/release/versification.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #corpus = UsfmFileTextCorpus("./resources/ben/IRVBen/release/USX_1", versification = targetVersification, handler=ModifiedTextRowCollector)
    #language="ben"
    #tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    #project_name = "IRVBen"
    #excludeBracketedText = False
    

    corpus_to_word_level_tsv(targetVersification, sourceVersification, corpus, tokenizer, project_name, excludeBracketedText=excludeBracketedText, language=language)
    #corpus_to_verse_level_tsv(targetVersification, sourceVersification, corpus, tokenizer, project_name, language=language)