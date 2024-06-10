import pytest
from test import __tsv_vrs_name_files__
import pandas as pd
from machine.scripture import Versification
import os
import csv

#Do the IDs only contain numbers?
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_source_verse_numeric(tsv_vrs_files):
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['source_verse']:
        assert id.isnumeric()

#Are the IDs valid length?
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_source_verse_length(tsv_vrs_files):
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['source_verse']:
        assert len(str(id)) == 8

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
    
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['source_verse']:
        book_id = int(str(id)[:2])
        assert (book_id > 0 and book_id in present_book_id_list)

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
                
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['source_verse']:
        chapter_id = int(str(id)[2:5])
        assert (chapter_id > 0 and chapter_id <= max_chapter_number)

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
                
    data_frame = pd.read_csv(tsv_vrs_files[0], sep='\t',dtype=str)
    for id in data_frame['source_verse']:
        verse_id = int(str(id)[5:8])
        assert (verse_id >= 0 and verse_id <= max_verse_number)
          
#Is each verse in the mapping present in the TSV (requires versification file)
@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
def test_mapped_verses_are_present(tsv_vrs_name_files):
    
    output_file = tsv_vrs_name_files[4]
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        
        targetVersification = Versification.load(tsv_vrs_name_files[1], fallback_name="web")
        mapping_sources = targetVersification.mappings._versification_to_standard.values()
        
        tsv_source_verses = []
        data_frame = pd.read_csv(tsv_vrs_name_files[0], sep='\t',dtype=str)
        for source_verse in data_frame['source_verse'].values:
            tsv_source_verses.append(str(source_verse)[:8])#TODO use bible-lib
        
        for source in mapping_sources:
            if (str(source.bbbcccvvvs)[1:] not in tsv_source_verses):
                if(
                    #(target.bbbcccvvvs)[-3:] != "000" #exclude superscriptions
                #and 
                int((source.bbbcccvvvs)[:3]) < 67 #exclude apocrypha
                ):
                    print("Mapping - Missing Verse - "+tsv_vrs_name_files[2] + " " + (source.bbbcccvvvs))
            
                    tsv_writer.writerow(["source_verse", "mapping", "missing_verse", tsv_vrs_name_files[2], source.bbbcccvvvs]) #OLD WAY

#Does each chapter possess the number of verses listed in the versification (requires versification file)
@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
def test_source_chapter_size(tsv_vrs_name_files):
    output_file = tsv_vrs_name_files[4]
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'a', newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
    
        print(tsv_vrs_name_files[0])
        originalVersification = Versification.load("./resources/versification/org.vrs", fallback_name="web")
        
        book_list = []
        chapter_list = []
        current_verse_count = 1
        previous_id = "01001001001"
        
        data_frame = pd.read_csv(tsv_vrs_name_files[0], sep='\t',dtype=str)
        for id in data_frame['source_verse']:
            
            previous_book_id = int(str(previous_id)[:2])
            previous_chapter_id = int(str(previous_id)[2:5])
            previous_verse_id = int(str(previous_id)[5:8])
            
            current_book_id = int(str(id)[:2])
            current_chapter_id = int(str(id)[2:5])
            current_verse_id = int(str(id)[5:8])
            
            if(current_book_id == 2 and current_chapter_id == 8 ):
                Holdup = True

            if(current_verse_id > previous_verse_id):#verse changes
                #increment verse count
                current_verse_count += 1
            
            if(current_verse_id < previous_verse_id or previous_chapter_id < current_chapter_id):#chapter changes
                #add chapter to chapter_list
                chapter_list.append(current_verse_count)
                current_verse_count = 1
            
            if(current_book_id > previous_book_id):#book changes
                #add book to book_list
                chapter_list.append(current_verse_count)
                book_list.append(chapter_list)
                chapter_list = []
                
            previous_id = id    
        
        chapter_list.append(current_verse_count)
        book_list.append(chapter_list)  
        
        for bookIndex in range(len(originalVersification.book_list)):
            
            try:
                bookExists = book_list[bookIndex]
                
                for chapterIndex in range(len(originalVersification.book_list[bookIndex])):
            
                    try:
                        chapterExists = book_list[bookIndex][chapterIndex]
                        
                        if(bookIndex==18 and chapterIndex==116):
                            holdup=True
                        
                        if (book_list[bookIndex][chapterIndex] > originalVersification.book_list[bookIndex][chapterIndex]): 
                            print("source_verse - Extra Verse - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                            tsv_writer.writerow(["target_verse", "size", "extra_verse", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(3)+str(chapterIndex + 1).zfill(3)])
                        elif(book_list[bookIndex][chapterIndex] < originalVersification.book_list[bookIndex][chapterIndex]):
                            print("source_verse - Missing Verse - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                            tsv_writer.writerow(["target_verse", "size", "missing_verse", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(3)+str(chapterIndex + 1).zfill(3)])
                    except:
                        print("source_verse - Missing Chapter - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                        tsv_writer.writerow(["target_verse", "size", "missing_chapter", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(3)+str(chapterIndex + 1).zfill(3)])
                
            except:
                if(bookIndex + 1 <= 66):#Exclude apocrypha
                    print("source_verse - Missing Book - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1))
                    tsv_writer.writerow(["target_verse", "size", "missing_book", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(3)])