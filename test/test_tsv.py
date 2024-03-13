#Based on https://github.com/Clear-Bible/macula-greek/blob/main/test/test_tsv.py
import os
import codecs
import pytest
from test import __tsv_vrs_name_files__
import pandas as pd
from machine.scripture import Versification

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
        assert (verse_id > 0 and verse_id <= max_verse_number)

#Is each verse in the mapping present in the TSV (requires versification file)
@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
def test_mapped_verses_are_present(tsv_vrs_name_files):
    
    targetVersification = Versification.load(tsv_vrs_name_files[1], fallback_name="web")
    mapping_targets = targetVersification.mappings._versification_to_standard.keys()
    
    tsv_ids = []
    data_frame = pd.read_csv(tsv_vrs_name_files[0], sep='\t',dtype=str)
    for id in data_frame['id'].values:
        tsv_ids.append(str(id)[:8])#TODO use bible-lib
    
    for target in mapping_targets:
        assert str(target.bbbcccvvvs)[1:] in tsv_ids, tsv_vrs_name_files[2] + " " + (target.bbbcccvvvs)[1:]

#Does each chapter possess the number of verses listed in the versification (requires versification file)
@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
def test_chapter_size(tsv_vrs_name_files):
    
    targetVersification = Versification.load(tsv_vrs_name_files[1], fallback_name="web")
    
    book_list = []
    chapter_list = []
    current_verse_count = 1
    previous_id = "01001001001"
    
    data_frame = pd.read_csv(tsv_vrs_name_files[0], sep='\t',dtype=str)
    for id in data_frame['id']:
        
        previous_book_id = int(str(previous_id)[:2])
        #previous_chapter_id = int(str(previous_id)[2:5])
        previous_verse_id = int(str(previous_id)[5:8])
        
        current_book_id = int(str(id)[:2])
        #current_chapter_id = int(str(id)[2:5])
        current_verse_id = int(str(id)[5:8])
        
        if(current_verse_id > previous_verse_id):#verse changes
            #increment verse count
            current_verse_count += 1
        
        if(current_verse_id < previous_verse_id):#verse changes
            #add chapter to chapter_list
            chapter_list.append(current_verse_count)
            current_verse_count = 1
        
        if(current_book_id > previous_book_id):#book changes
            #add book to book_list
            book_list.append(chapter_list)
            chapter_list = []
            
        previous_id = id    
    
    current_verse_count += 1
    chapter_list.append(current_verse_count)
    book_list.append(chapter_list)  
    
    #for book in book_list:
    #    print(book)
        
    #print("")
    
    #for book in targetVersification.book_list:
    #    print(book)
    
    for index in range(len(targetVersification.book_list)):
        assert (book_list[index] == targetVersification.book_list[index]), tsv_vrs_name_files[2] + " Book Id: " + str(index + 1)