import os
import codecs
import pytest
from test import __tsv_vrs_name_files__
from helpers.verse_text import reconstitute
import polars as pl
from machine.scripture import Versification
import csv
from pathlib import Path
from helpers.strings import is_unicode_punctuation

@pytest.mark.skip(reason="Passing this test isn't necessary")
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_cross_references_only_on_verse_ends(tsv_vrs_files):    
    print(tsv_vrs_files[0])
    current_bcv_id = "00000000"
    in_parentheses = False
    is_cross_reference = False

    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0, quote_char=None)
    for row in data_frame.iter_rows(named=True):
        
        previous_bcv_id = current_bcv_id
        current_bcv_id = row["id"][0:8]
        token = str(row["text"])
        
        if(is_cross_reference and not in_parentheses):
            assert(previous_bcv_id != current_bcv_id), tsv_vrs_files[2] + " {} ".format(current_bcv_id) + "found a cross-reference in the middle of a verse"
            is_cross_reference = False
        
        for char in token:
            if(char == '('):
                in_parentheses = True
            if(in_parentheses and char == ':'):
                is_cross_reference = True
            elif(char ==')'):
                in_parentheses = False