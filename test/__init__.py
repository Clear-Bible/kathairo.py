import csv
from pathlib import Path
from helpers.strings import is_unicode_punctuation
from machine.scripture import Versification
from helpers.paths import get_target_file_location
import os
import polars as pl
from helpers.verse_text import reconstitute

#__macula_greek_tsv_rows__ = []

#TODO have common method of creating TSV file name
#tsv_path = "../TSVs/target_BSB_USX_new.tsv"
__tsv_vrs_name_files__ = []#tsv_path

#vrs_path = "../resources/bsb_usx/release/versification.vrs"
#__vrs_files__ = []#vrs_path

#TODO combine with wrapper.py and abstract it to reduce duplication
import json

json_file = "kathairo/Prompts/prompts.json"

#get json dictionary and keys
with open(json_file) as json_data:
    jsonData = json.load(json_data)
    for jsonObject in jsonData:
        jsonKeys = jsonObject.keys()
    
        #TODO combine with args_parser in main and abstract out args parsing to args_manager
        targetVersificationPath = jsonObject["targetVersificationPath"]
        projectName = jsonObject["projectName"]
        language = jsonObject["language"]
        
        outputFileLocation = get_target_file_location("TSVs", projectName, language)
        
        prompt_tsv_vrs = [outputFileLocation, targetVersificationPath, projectName, language]
        __tsv_vrs_name_files__.append(prompt_tsv_vrs)


#with open(tsv_path, encoding='utf-8') as file:
#    reader = csv.DictReader(file, delimiter="\t")
#    for row in reader:
#        __macula_greek_tsv_rows__.append(row)
     
#for project in __tsv_vrs_name_files__:
#    test_source_chapter_size(project)

#for files in __tsv_vrs_name_files__:
#    reconstitute(Path(files[0]))

#for files in __tsv_vrs_name_files__:
#    test_verse_text_reconstitution(files)

#for files in __tsv_vrs_name_files__:
#    test_exclude_punctuation(files)

#for files in __tsv_vrs_name_files__:
#    test_exclude_bracketed_text(files)

#for files in __tsv_vrs_name_files__:
#    test_chinese_tokens_have_no_punctuation(files)

#for files in __tsv_vrs_name_files__:
#    test_source_chapter_size(files)

#for files in __tsv_vrs_name_files__:
#    test_mapped_verses_are_present(files)