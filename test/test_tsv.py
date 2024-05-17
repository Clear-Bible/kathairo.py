#Based on https://github.com/Clear-Bible/macula-greek/blob/main/test/test_tsv.py
import os
import codecs
import pytest
from test import __tsv_vrs_name_files__
from helpers.verse_text import reconstitute
import pandas as pd
from machine.scripture import Versification
import csv
from pathlib import Path
from helpers.strings import is_unicode_punctuation

# Verify that the file exists.
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_files_exists(tsv_vrs_files):
    size = os.path.getsize(tsv_vrs_files[0])
    assert size > 0

# Verify that the file is in utf8 format.
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_file_is_valid_utf8(tsv_vrs_files):
    lines = codecs.open(tsv_vrs_files[0], encoding="utf-8", errors="strict").readlines()
    assert lines != ""

#Do the IDs only contain numbers?
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_id_numeric(tsv_vrs_files):
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['id']:
        assert id.isnumeric()

#Are the IDs valid length?
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_id_length(tsv_vrs_files):
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['id']:
        assert len(str(id)) == 11

#Is the Book ID a valid value? (requires versification file)
#Is the Book in the Versification file? 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_id_book_value(tsv_vrs_files):
    present_book_id_list = []
    current_book_number = 0
    
    targetVersification = Versification.load(tsv_vrs_files[1], fallback_name="web")
    for book in targetVersification.book_list:
        current_book_number+=1
        if(len(book) > 1 or book[0] > 1):
            present_book_id_list.append(current_book_number)
    
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['id']:
        book_id = int(str(id)[:2])
        assert (book_id > 0 and book_id in present_book_id_list)

#Is the Chapter ID a valid value? (requires versification file)
#Are the 3rd through 5th digits between 1 and the max chapter value in the versification
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_id_chapter_value(tsv_vrs_files):    
    max_chapter_number = 0
    
    targetVersification = Versification.load(tsv_vrs_files[1], fallback_name="web")
    for book in targetVersification.book_list:
        book_size = len(book)
        if(book_size > max_chapter_number):
                max_chapter_number = book_size
                
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['id']:
        chapter_id = int(str(id)[2:5])
        assert (chapter_id > 0 and chapter_id <= max_chapter_number)

#Is the verse ID a valid value? (requires versification file)
#Are the 6th-8th digits between 1 and the max verse value in the versification
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_id_verse_value(tsv_vrs_files):
    max_verse_number = 0
    
    targetVersification = Versification.load(tsv_vrs_files[1], fallback_name="web")
    for book in targetVersification.book_list:
        for chapter_size in book:
            if(chapter_size > max_verse_number):
                max_verse_number = chapter_size
                
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['id']:
        verse_id = int(str(id)[5:8])
        assert (verse_id >= 0 and verse_id <= max_verse_number)
          
#Is skip_space_after column accurate
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_verse_text_reconstitution(tsv_vrs_files):
    #Reconstitute VerseText File from TSV
    tsv_path = Path(tsv_vrs_files[0])
    reconstitute(tsv_path, tsv_vrs_files[3])
    
    #Compare Reconstituted File to VerseText File
    verseTextPath = tsv_path.parent.parent.parent / "VerseText"/ tsv_vrs_files[3] /f"{tsv_path.stem}.tsv"
    verseTextRows = [r for r in csv.DictReader(verseTextPath.open("r", encoding='utf-8'), delimiter="\t")]

    reconstitutedPath = tsv_path.parent.parent.parent / "test" /"reconstituted" / tsv_vrs_files[3] / f"{tsv_path.stem}_reconstitution.tsv"
    reconstitutedRows = [r for r in csv.DictReader(reconstitutedPath.open("r", encoding='utf-8'), delimiter="\t")]

    for index in range(len(verseTextRows)):
        if(index>=len(reconstitutedRows)):
            break
        if("OCCB" in tsv_path.stem):
            adjusted_verse = verseTextRows[index]['text'].strip()
            adjusted_reconstitution = reconstitutedRows[index]['text'].strip()
            assert(adjusted_verse == adjusted_reconstitution) #due to random spaces in chinese
                #print(f"MISMATCH---{adjusted_verse}")
                #print(f"MISMATCH---{adjusted_reconstitution}")
                #print(f"------------------------------")
        else: 
            adjusted_verse = verseTextRows[index]['text'].replace("  ", " ")
            adjusted_reconstitution = reconstitutedRows[index]['text'].rstrip().replace("  ", " ")
            assert(adjusted_verse == adjusted_reconstitution)
                #print(f"MISMATCH---{adjusted_verse}")
                #print(f"MISMATCH---{adjusted_reconstitution}")
                #print(f"------------------------------")

#Is punctuation excluded 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_exclude_punctuation(tsv_vrs_files):    
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for row in data_frame.itertuples():
        token = row.text
        exclude = row.exclude
        
        if(exclude == 'y'):
            exclude_bool = True
        else:
            exclude_bool = False
        
        #TODO look at more than first char
        if (isinstance(token, str) and len(token)>0):
            token_is_punct = is_unicode_punctuation(token[0])
        else:
            token_is_punct = False
        
        if(token_is_punct):
            assert(token_is_punct == exclude_bool)
        
#Is bracketed text excluded 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_exclude_bracketed_text(tsv_vrs_files):    
    
    if ("RSB" in tsv_vrs_files[0]):
        
        in_brackets = False
        
        data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
        for row in data_frame.itertuples():
            
            token = row.text
            exclude = row.exclude
            
            if(exclude == 'y'):
                    exclude_bool = True
            else:
                exclude_bool = False
            
            for char in token:
                
                if(char == '['):
                    in_brackets = True
                
                if(in_brackets):   
                    if(not exclude_bool):
                        holdup=True       
                    assert(in_brackets == exclude_bool)
                
                if(char ==']'):
                    in_brackets = False