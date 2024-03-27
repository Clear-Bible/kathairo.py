#Based on https://github.com/Clear-Bible/macula-greek/blob/main/test/test_tsv.py
import os
import codecs
import pytest
from test import __tsv_vrs_name_files__
import pandas as pd
from machine.scripture import Versification

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
        if (str(target.bbbcccvvvs)[1:] not in tsv_ids):
            if(
                #(target.bbbcccvvvs)[-3:] != "000" #exclude superscriptions
               #and 
               int((target.bbbcccvvvs)[:3]) < 67 #exclude apocrypha
            ):
                print("Missing Mapped Verse - "+tsv_vrs_name_files[2] + " " + (target.bbbcccvvvs))


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
        previous_chapter_id = int(str(previous_id)[2:5])
        previous_verse_id = int(str(previous_id)[5:8])
        
        current_book_id = int(str(id)[:2])
        current_chapter_id = int(str(id)[2:5])
        current_verse_id = int(str(id)[5:8])
        
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
    
    #for book in book_list:
    #    print(book)
        
    #print("")
    
    #for book in targetVersification.book_list:
    #    print(book)
    
    for bookIndex in range(len(targetVersification.book_list)):
        
        try:
            bookExists = book_list[bookIndex]
            
            for chapterIndex in range(len(targetVersification.book_list[bookIndex])):
        
                try:
                    chapterExists = book_list[bookIndex][chapterIndex]
                    
                    if(bookIndex==18 and chapterIndex==116):
                        holdup=True
                    
                    if (book_list[bookIndex][chapterIndex] > targetVersification.book_list[bookIndex][chapterIndex]): 
                        print("Extra Verse - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1)+":"+str(chapterIndex + 1))
                    elif(book_list[bookIndex][chapterIndex] < targetVersification.book_list[bookIndex][chapterIndex]):
                        print("Missing Verse - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1)+":"+str(chapterIndex + 1))
                except:
                    print("Missing Chapter - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1)+":"+str(chapterIndex + 1))
            
        except:
            if(bookIndex + 1 <= 66):#Exclude apocrypha
                print("Missing Book - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1))