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
from helpers.strings import is_unicode_punctuation, contains_number
from Parsing.USFM.usfm_handlers import ModifiedTextRowCollector
from helpers.paths import get_target_file_location
import os
import pandas as pd
import helpers.strings as string
import helpers.versification

def corpus_to_verse_level_tsv(targetVersification:Versification, sourceVersification:Versification, corpus:ScriptureTextCorpus, tokenizer:WhitespaceTokenizer, 
                            project_name:str, language:str, removeZwFromWordsPath:str, excludeBracketedText:bool = False, excludeCrossReferences:bool = False):
    #How do we remove ZW characters from verse text?
    
    unused_versification_mapping = helpers.versification.create_target_to_sources_dict(targetVersification)
    
    outputFileName = get_target_file_location("VerseText", project_name, language)

    os.makedirs(os.path.dirname(outputFileName), exist_ok=True)
    with open(outputFileName, 'w', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        tsv_writer.writerow(["id", "source_verse", "text","id_range_end", "source_verse_range_end"])
        verse_range_list = []

        for row in corpus:#.tokenize(tokenizer).nfc_normalize()    

            targetVref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, targetVersification) #dependent on which .vrs is being used    
            
            sourceVref, source_verse_range_end = helpers.versification.set_source_verse(targetVref, sourceVersification, unused_versification_mapping)

            if(not row.is_in_range or row.is_range_start):
                for verse_range_row in verse_range_list:
                    verse_range_row[3] = (f"{rowBcv}")
                    verse_range_row[4] = (f"{sourceBcv}")
                    tsv_writer.writerow(verse_range_row)
                verse_range_list.clear()

            sourceBcv = fromubs(f"{re.sub(r'[^0-9]', '', sourceVref.bbbcccvvvs)}00000").to_bcvid
            rowBcv= fromubs(f"{re.sub(r'[^0-9]', '', row.ref.bbbcccvvvs)}00000").to_bcvid
            
            if(row.text != "" and row.is_in_range):
                verse_range_list.append([f"{rowBcv}", f"{sourceBcv}", row.text, "", source_verse_range_end])
            elif(row.text != ""):
                tsv_writer.writerow([f"{rowBcv}", f"{sourceBcv}", row.text, "", source_verse_range_end])

def corpus_to_word_level_tsv(targetVersification:Versification, sourceVersification:Versification, corpus:ScriptureTextCorpus, tokenizer:WhitespaceTokenizer, 
                project_name:str, language:str, removeZwFromWordsPath:str, excludeBracketedText:bool = False, excludeCrossReferences:bool = False):
    
    unused_versification_mapping = helpers.versification.create_target_to_sources_dict(targetVersification)
    
    zw_removal_df=None
    if(removeZwFromWordsPath != None):
        zw_removal_df = pd.read_csv(removeZwFromWordsPath, sep='\t',dtype=str)

    outputFileName = get_target_file_location("TSVs", project_name, language)

    os.makedirs(os.path.dirname(outputFileName), exist_ok=True)
    with open(outputFileName, 'w', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        tsv_writer.writerow(["id", "source_verse", "text", "skip_space_after", "exclude", "id_range_end", "source_verse_range_end"])

        in_brackets = False
        unprinted_row_list = [] #rename to unprinted verse_ranges?
        
        in_parentheses = False
        is_cross_reference = False
        has_number = False
        unprinted_parenthetical_tokens = []
        
        is_verse_range = False
        
        targetVref = None
        previous_verse_num = 0
        
        for row in corpus.tokenize(tokenizer):#.tokenize(tokenizer).nfc_normalize() #Include for Double Tokenization    

            #if(row.is_in_range and row.text == ''):
            #    tokenized_row = tokenizer.tokenize((row.text + " <RANGE>"))
            #else:
            #    tokenized_row = tokenizer.tokenize(row.text) # Include for Double Tokenization
            
            #print(f"{row.ref}: {row.text}")

            if(targetVref != None):
                previous_verse_num = targetVref.verse_num
            targetVref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, targetVersification) #dependent on which .vrs is being used    
            
            sourceVref, source_verse_range_end = helpers.versification.set_source_verse(targetVref, sourceVersification, unused_versification_mapping)
            
            if(targetVref.bbbcccvvvs == "043008001"):
                stop = True
            
            if(targetVref.verse_num != previous_verse_num):
                wordIndex = 1
            
            if(not in_parentheses):    
                for unprinted_cross_reference_token in unprinted_parenthetical_tokens:
                    if(excludeCrossReferences and is_cross_reference):
                        unprinted_cross_reference_token[4] = 'y' #exclude if is_cross_reference
                    if(is_verse_range):
                        unprinted_row_list.append(unprinted_cross_reference_token)
                    else:
                        tsv_writer.writerow(unprinted_cross_reference_token)
                has_number = False
                is_cross_reference = False
                unprinted_parenthetical_tokens.clear()

            if(not row.is_in_range or row.is_range_start):    
                for unprinted_row in unprinted_row_list:
                    if(is_verse_range):
                        unprinted_row[5] = (f"{rowBcv}")
                        unprinted_row[6] = (f"{sourceBcv}")
                    tsv_writer.writerow(unprinted_row)
                is_verse_range = False
                unprinted_row_list.clear()
            
            sourceBcv = fromubs(f"{re.sub(r'[^0-9]', '', sourceVref.bbbcccvvvs)}00000").to_bcvid
            rowBcv= fromubs(f"{re.sub(r'[^0-9]', '', row.ref.bbbcccvvvs)}00000").to_bcvid
            
            for index in range(len(row.segment)):
            #for token in row.segment:#row.segment, tokenized_row:
            
                if(not in_parentheses):    
                    for unprinted_cross_reference_token in unprinted_parenthetical_tokens:
                        if(excludeCrossReferences and is_cross_reference):
                            unprinted_cross_reference_token[4] = 'y' #exclude if is_cross_reference
                        if(is_verse_range):
                            unprinted_row_list.append(unprinted_cross_reference_token)
                        else:
                            tsv_writer.writerow(unprinted_cross_reference_token)
                    has_number = False
                    is_cross_reference = False
                    unprinted_parenthetical_tokens.clear()
            
                token = row.segment[index]
                
                if(removeZwFromWordsPath != None and token != " "):
                    if token in zw_removal_df["words"].values:    
                        token = token.replace(string.zwsp, string.empty_string).replace(string.zwj, string.empty_string).replace(string.zwnj, string.empty_string)
                
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

                exclude = "y"
                for char in token:
                    if(not in_brackets and not is_unicode_punctuation(char)):
                        exclude = ""
                        break
                    
                if(excludeBracketedText and '[' in token):
                    in_brackets = True
                    exclude = "y"
                if(']' in token):
                    in_brackets = False
                    
                if(excludeCrossReferences and '(' in token): #add to unit test to look for that all things marked as cross references are indeed cross-references and no token has a colon and a parentheses
                    in_parentheses = True
                if(excludeCrossReferences and in_parentheses and contains_number(token)):#add this change to the unit test
                    has_number = True
                if(excludeCrossReferences and in_parentheses and has_number and ':' in token):
                    is_cross_reference = True
                
                wordIndexStr = str(wordIndex).zfill(3)
                
                if(row.text != ""):
                    if(in_parentheses):
                        unprinted_parenthetical_tokens.append(([f"{rowBcv}{wordIndexStr}", f"{sourceBcv}", token, skip_space_after, exclude, "", source_verse_range_end]))
                    elif(row.is_in_range):
                        is_verse_range = True
                        unprinted_row_list.append([f"{rowBcv}{wordIndexStr}", f"{sourceBcv}", token, skip_space_after, exclude, "", source_verse_range_end])
                    else:
                        tsv_writer.writerow([f"{rowBcv}{wordIndexStr}", f"{sourceBcv}", token, skip_space_after, exclude, "", source_verse_range_end])
                
                if(')' in token):
                    in_parentheses = False
                
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
    targetVersification = Versification.load("./resources/man/occb_simplified_usx/release/versification.vrs", fallback_name="web")
    sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    corpus = UsxFileTextCorpus("./resources/man/occb_simplified_usx/release/USX_1", versification = targetVersification)
    tokenizer = ChineseBibleWordTokenizer.ChineseBibleWordTokenizer()
    project_name = "OCCB-simplified"
    excludeBracketedText = False
    language="man"
    removeZwFromWordsPath = None

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
    #targetVersification = Versification.load("./resources/hin/IRVHin/versification.vrs", fallback_name="web")
    #sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #language="hin"
    #corpus = UsxFileTextCorpus("./resources/hin/IRVHin", versification = targetVersification)
    #tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    #project_name="IRVHin"
    #excludeBracketedText = False
    #removeZwFromWordsPath = "./resources/hin/zw-removal-words.tsv"
    
    
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
    #corpus = UsfmFileTextCorpus("./resources/ben/IRVBen/release/USX_1", versification = targetVersification, handler=ModifiedTextRowCollector, psalmSuperscriptionTag = "s")
    #language="ben"
    #tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    #project_name = "IRVBen"
    #excludeBracketedText = False
    
    #RV09
    # targetVersification = Versification.load("./resources/spa/RV09/versification.vrs", fallback_name="web")
    # sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    # language="spa"
    # corpus = UsfmFileTextCorpus("./resources/spa/RV09", versification = targetVersification, handler=ModifiedTextRowCollector, psalmSuperscriptionTag = "d")
    # tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    # project_name="RV09"
    # excludeBracketedText = False
    # removeZwFromWordsPath = None

    #TBI
    # targetVersification = Versification.load("./resources/ind/TBI/custom.vrs", fallback_name="web")
    # sourceVersification = Versification(name="sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    # language = "ind"
    # corpus = UsfmFileTextCorpus("./resources/ind/TBI", versification=targetVersification, handler=ModifiedTextRowCollector, psalmSuperscriptionTag="s")
    # tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    # project_name = "TBI"
    # excludeBracketedText = False
    # removeZwFromWordsPath = None

    # JFA11
    # targetVersification = Versification.load("./resources/por/JFA11/JFA11.vrs", fallback_name="web")
    # sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    # language="por"
    # corpus = UsfmFileTextCorpus("./resources/por/JFA11/usfm", versification = targetVersification, handler=ModifiedTextRowCollector, psalmSuperscriptionTag = "d")
    # tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    # project_name="JFA11"
    # excludeBracketedText = False
    # removeZwFromWordsPath = None

    # SRUV06
    #usfm_language = "ind"
    #usfm_abbrev = "TBI"
    #targetVersification = Versification.load(f"./resources/{usfm_language}/{usfm_abbrev}/custom.vrs", fallback_name="web")
    #sourceVersification = Versification(name="sourceVersification", base_versification=ORIGINAL_VERSIFICATION)
    #language = usfm_language
    #corpus = UsfmFileTextCorpus(f"./resources/{usfm_language}/{usfm_abbrev}", versification=targetVersification, handler=ModifiedTextRowCollector, psalmSuperscriptionTag="s")
    # corpus = UsxFileTextCorpus(f"./resources/{usfm_language}/{usfm_abbrev}", versification = targetVersification)
    #tokenizer = LatinWhitespaceIncludedWordTokenizer(language=language)
    #project_name = usfm_abbrev
    #excludeBracketedText = False
    #removeZwFromWordsPath = None

    corpus_to_word_level_tsv(targetVersification, sourceVersification, corpus, tokenizer, project_name, excludeBracketedText=excludeBracketedText, language=language, removeZwFromWordsPath=removeZwFromWordsPath)
    # corpus_to_verse_level_tsv(targetVersification, sourceVersification, corpus, tokenizer, project_name, language=language, removeZwFromWordsPath=None)