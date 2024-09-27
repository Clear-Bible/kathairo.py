#Based on https://github.com/Clear-Bible/macula-greek/blob/main/test/test_tsv.py
import pytest
from test import __tsv_vrs_name_files__
import polars as pl
from helpers.strings import is_unicode_punctuation

@pytest.mark.skip(reason="Passing this test isn't necessary")
@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
def test_tokens_contain_no_punctuation(tsv_vrs_name_files):
    #if ("OCCB" in tsv_vrs_name_files[0]):
    data_frame = pl.read_csv(tsv_vrs_name_files[0], separator='\t', infer_schema_length=0, quote_char=None)
    for row in data_frame.iter_rows(named=True):
        token = str(row["text"])
        for char in token:
            if(is_unicode_punctuation(char) and len(token)>1):
                id = row["id"]
                print(id, token)#, row.verse_text)
                break                

@pytest.mark.skip(reason="Passing this test isn't necessary")
@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
def test_tokens_start_and_end_with_no_punctuation(tsv_vrs_name_files):
    print(tsv_vrs_name_files[0])
    #if ("OCCB" not in tsv_vrs_name_files[0]):
    data_frame = pl.read_csv(tsv_vrs_name_files[0], separator='\t', infer_schema_length=0, quote_char=None)
    for row in data_frame.iter_rows(named=True):
        token = row["text"]
        #for char in token:
        if(len(str(token))>1 and 
            (
                is_unicode_punctuation(str(token)[0])
                or
                is_unicode_punctuation(str(token)[len(str(token))-1])
                )
            
            ):
            id = row["id"]
            print(id, token)#, row.verse_text)
     
@pytest.mark.skip(reason="Passing this test isn't necessary")       
@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
def test_consecutive_punctuation(tsv_vrs_name_files):
    print(tsv_vrs_name_files[0])
    data_frame = pl.read_csv(tsv_vrs_name_files[0], separator='\t', infer_schema_length=0, quote_char=None)
    
    previous_id = "none"
    previous_character = "none"
    
    for row in data_frame.iter_rows(named=True):
        token = str(row["text"])
        for character in token:
            if(is_unicode_punctuation(str(character)) and 
               is_unicode_punctuation(str(previous_character)) and 
               str(character) == str(previous_character) and 
               row["id"] != previous_id and
               previous_skip_space_after == "y"):
                print(previous_id, previous_character, row["id"], character)
            previous_character = character
            previous_id = row["id"]
            previous_skip_space_after = row["skip_space_after"]