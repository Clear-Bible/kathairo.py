import pytest
from test import __tsv_vrs_name_files__
import polars as pl
from machine.scripture import Versification

#Do the IDs only contain numbers?
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_source_verse_numeric(tsv_vrs_files):
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0)
    for id in data_frame['source_verse']:
        assert id.isnumeric(), tsv_vrs_files[2] + " {} ".format(id) + "is not numeric."

#Are the IDs valid length?
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_source_verse_length(tsv_vrs_files):
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0)
    for id in data_frame['source_verse']:
        assert len(str(id)) == 8, tsv_vrs_files[2] + " {} ".format(id) + "!= 8"

#Is the Book ID a valid value? (requires versification file)
#Is the Book in the Versification file? 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_source_verse_book_value(tsv_vrs_files):
    present_book_id_list = []
    current_book_number = 0
    
    originalVersification = Versification.load("./resources/versification/org.vrs", fallback_name="web")
    for book in originalVersification.book_list:
        current_book_number+=1
        if(len(book) > 1 or book[0] > 1):
            present_book_id_list.append(current_book_number)
    
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0)
    for id in data_frame['source_verse']:
        book_id = int(str(id)[:2])
        assert (book_id > 0 and book_id in present_book_id_list), tsv_vrs_files[2] + " {} ".format(id) + "invalid book ID"

#Is the Chapter ID a valid value? (requires versification file)
#Are the 3rd through 5th digits between 1 and the max chapter value in the versification
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_source_verse_chapter_value(tsv_vrs_files):    
    max_chapter_number = 0
    
    originalVersification = Versification.load("./resources/versification/org.vrs", fallback_name="web")
    for book in originalVersification.book_list:
        book_size = len(book)
        if(book_size > max_chapter_number):
                max_chapter_number = book_size
                
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0)
    for id in data_frame['source_verse']:
        chapter_id = int(str(id)[2:5])
        assert (chapter_id > 0 and chapter_id <= max_chapter_number), tsv_vrs_files[2] + " {}".format(id) + "invalid chapter ID"

#Is the verse ID a valid value? (requires versification file)
#Are the 6th-8th digits between 1 and the max verse value in the versification
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_id_verse_value(tsv_vrs_files):
    max_verse_number = 0
    
    originalVersification = Versification.load("./resources/versification/org.vrs", fallback_name="web")
    for book in originalVersification.book_list:
        for chapter_size in book:
            if(chapter_size > max_verse_number):
                max_verse_number = chapter_size
                
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0)
    for id in data_frame['source_verse']:
        verse_id = int(str(id)[5:8])
        assert (verse_id >= 0 and verse_id <= max_verse_number), tsv_vrs_files[2] + " {}".format(id) + "invalid verse ID"