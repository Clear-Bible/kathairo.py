#Based on https://github.com/Clear-Bible/macula-greek/blob/main/test/test_tsv.py
import pytest
from test import __tsv_vrs_name_files__
import polars as pl
from machine.scripture import Versification
import os
import csv
from helpers.paths import get_target_file_location

@pytest.mark.parametrize("tsv_vrs_name_files", __tsv_vrs_name_files__)
class TestVersification:
    
    #Is each verse in the mapping present in the TSV (requires versification file)
    def test_source_mapped_verses_are_present(self, tsv_vrs_name_files):
        
        project_name = tsv_vrs_name_files[2]
        language = tsv_vrs_name_files[3]
        
        output_file = get_target_file_location("versification_issues", project_name+"_source_mapping_issues", language)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=None)
            
            targetVersification = Versification.load(tsv_vrs_name_files[1], fallback_name="web")
            mapping_sources = targetVersification.mappings._versification_to_standard.values()
            
            tsv_source_verses = []
            data_frame = pl.read_csv(tsv_vrs_name_files[0], separator='\t', infer_schema_length=0)
            
            for row in data_frame.iter_rows(named=True):
                source_verse = int(row["source_verse"])      
                if(isinstance(row["source_verse_range_end"], str)):
                    source_verse_range_end = int(row["source_verse_range_end"]) + 1
                else:
                    source_verse_range_end = source_verse + 1 
                
                while(source_verse != source_verse_range_end):#<=
                    tsv_source_verses.append(str(source_verse).zfill(8))#TODO use bible-lib
                    source_verse += 1
        
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
    def test_source_chapter_size(self, tsv_vrs_name_files):
        
        project_name = tsv_vrs_name_files[2]
        language = tsv_vrs_name_files[3]
        
        output_file = get_target_file_location("versification_issues", project_name+"_source_size_issues", language)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=None)
        
            print(tsv_vrs_name_files[0])
            originalVersification = Versification.load("./resources/versification/org.vrs", fallback_name="web")
            
            book_list = []
            chapter_list = []
            current_verse_count = 0
            previous_source_verse = "01001000000"
            previous_source_verse_range_end = "01001000000"
            
            data_frame = pl.read_csv(tsv_vrs_name_files[0], separator='\t', infer_schema_length=0)
            
            for row in data_frame.iter_rows(named=True):
                source_verse = row["source_verse"]
                
                if(isinstance(row["source_verse_range_end"], str)):
                    source_verse_range_end = row["source_verse_range_end"]
                else:
                    source_verse_range_end = source_verse
                
                previous_book_source_verse = int(str(previous_source_verse)[:2])
                previous_chapter_source_verse = int(str(previous_source_verse)[2:5])
                previous_verse_source_verse = int(str(previous_source_verse)[5:8])
                
                previous_book_source_verse_range_end = int(str(previous_source_verse_range_end)[:2])
                previous_chapter_source_verse_range_end = int(str(previous_source_verse_range_end)[2:5])
                previous_verse_source_verse_range_end = int(str(previous_source_verse_range_end)[5:8])
                
                current_book_source_verse = int(str(source_verse)[:2])
                current_chapter_source_verse = int(str(source_verse)[2:5])
                current_verse_source_verse = int(str(source_verse)[5:8])
                
                current_book_source_verse_range_end = int(str(source_verse_range_end)[:2])
                current_chapter_source_verse_range_end = int(str(source_verse_range_end)[2:5])
                current_verse_source_verse_range_end = int(str(source_verse_range_end)[5:8])
                
                if(current_chapter_source_verse == current_chapter_source_verse_range_end and 
                   current_book_source_verse == current_book_source_verse_range_end):
                    range_size = current_verse_source_verse_range_end - current_verse_source_verse
                else:
                    range_size = 0
                
                if(current_verse_source_verse > previous_verse_source_verse):#verse changes != #elif
                    #increment verse count
                    current_verse_count += 1 + range_size
                
                if(current_verse_source_verse < previous_verse_source_verse or 
                   previous_chapter_source_verse < current_chapter_source_verse):#chapter changes
                    #add chapter to chapter_list
                    chapter_list.append(current_verse_count)
                    current_verse_count = 0
                    
                    #cross-chapter verse range
                    if(previous_book_source_verse_range_end == current_book_source_verse_range_end and 
                       previous_chapter_source_verse_range_end == current_chapter_source_verse):        
                        #assume that the cross-chapter source_verse range is a single verse
                        current_verse_count += 1 
                       
                    #increment verse count
                    current_verse_count += 1 + range_size
                
                if(current_book_source_verse > previous_book_source_verse):#book changes
                    #add book to book_list
                    chapter_list.append(current_verse_count)
                    book_list.append(chapter_list)
                    chapter_list = []
                    
                previous_source_verse = source_verse
                previous_source_verse_range_end = source_verse_range_end    
            
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
                                tsv_writer.writerow(["source_verse", "size", "extra_verse", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)+str(chapterIndex + 1).zfill(3)])
                            elif(book_list[bookIndex][chapterIndex] < originalVersification.book_list[bookIndex][chapterIndex]):
                                print("source_verse - Missing Verse - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                                tsv_writer.writerow(["source_verse", "size", "missing_verse", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)+str(chapterIndex + 1).zfill(3)])
                        except:
                            print("source_verse - Missing Chapter - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                            tsv_writer.writerow(["source_verse", "size", "missing_chapter", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)+str(chapterIndex + 1).zfill(3)])
                    
                except:
                    if(bookIndex + 1 <= 66):#Exclude apocrypha
                        print("source_verse - Missing Book - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1))
                        tsv_writer.writerow(["source_verse", "size", "missing_book", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)])
                        
    #Is each verse in the mapping present in the TSV (requires versification file)                    
    def test_target_mapped_verses_are_present(self, tsv_vrs_name_files):
        
        project_name = tsv_vrs_name_files[2]
        language = tsv_vrs_name_files[3]
        
        output_file = get_target_file_location("versification_issues", project_name+"_target_mapping_issues", language)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=None)
        
            targetVersification = Versification.load(tsv_vrs_name_files[1], fallback_name="web")
            mapping_targets = targetVersification.mappings._versification_to_standard.keys()
            
            tsv_ids = []
            data_frame = pl.read_csv(tsv_vrs_name_files[0], separator='\t', infer_schema_length=0)
                    
            for row in data_frame.iter_rows(named=True):
                id = int(row["id"][:8])      
                if(isinstance(row["id_range_end"], str)):
                    id_range_end = int(row["id_range_end"][:8]) + 1 
                else:
                    id_range_end = id + 1 
                
                while(id != id_range_end): #<=
                    tsv_ids.append(str(id).zfill(8))#TODO use bible-lib
                    id += 1
            
            for target in mapping_targets:
                if (str(target.bbbcccvvvs)[1:] not in tsv_ids):
                    if(
                        #(target.bbbcccvvvs)[-3:] != "000" #exclude superscriptions
                    #and 
                    int((target.bbbcccvvvs)[:3]) < 67 #exclude apocrypha
                    ):
                        print("Mapping - Missing Verse - "+tsv_vrs_name_files[2] + " " + (target.bbbcccvvvs))
                        
                        tsv_writer.writerow(["target_verse", "mapping", "missing_verse", tsv_vrs_name_files[2], target.bbbcccvvvs]) #OLD WAY

    #Does each chapter possess the number of verses listed in the versification (requires versification file)
    def test_target_chapter_size(self, tsv_vrs_name_files):
        
        project_name = tsv_vrs_name_files[2]
        language = tsv_vrs_name_files[3]
        
        output_file = get_target_file_location("versification_issues", project_name+"_target_size_issues", language)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=None)
        
            targetVersification = Versification.load(tsv_vrs_name_files[1], fallback_name="web")
            
            book_list = []
            chapter_list = []
            current_verse_count = 0
            previous_id = "01001000000"
            
            data_frame = pl.read_csv(tsv_vrs_name_files[0], separator='\t', infer_schema_length=0)
            
            for row in data_frame.iter_rows(named=True):
                id = row["id"]   
                
                if(isinstance(row["id_range_end"], str)):
                    id_range_end = row["id_range_end"]
                else:
                    id_range_end = id
                
                previous_book_id = int(str(previous_id)[:2])
                previous_chapter_id = int(str(previous_id)[2:5])
                previous_verse_id = int(str(previous_id)[5:8])
                
                current_book_id = int(str(id)[:2])
                current_chapter_id = int(str(id)[2:5])
                current_verse_id = int(str(id)[5:8])
                
                current_book_id_range_end = int(str(id_range_end)[:2])
                current_chapter_id_range_end = int(str(id_range_end)[2:5])
                current_verse_id_range_end = int(str(id_range_end)[5:8])
                
                range_size = current_verse_id_range_end - current_verse_id
                
                if(current_verse_id > previous_verse_id):#verse changes !=
                    #increment verse count
                    current_verse_count += 1 + range_size
                
                if(current_verse_id < previous_verse_id or 
                   previous_chapter_id < current_chapter_id):#chapter changes
                    #add chapter to chapter_list
                    chapter_list.append(current_verse_count)
                    current_verse_count = 0
                    if(current_verse_id == 0):
                        current_verse_count = -1
                    #increment verse count
                    current_verse_count += 1 + range_size
                
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
                                print("Chapter Size - Extra Verse - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                                tsv_writer.writerow(["target_verse", "size", "extra_verse", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)+str(chapterIndex + 1).zfill(3)]) #OLD WAY
                            elif(book_list[bookIndex][chapterIndex] < targetVersification.book_list[bookIndex][chapterIndex]):
                                print("Chapter Size - Missing Verse - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                                tsv_writer.writerow(["target_verse", "size", "missing_verse", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)+str(chapterIndex + 1).zfill(3)])
                        except:
                            print("Chapter Size - Missing Chapter - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1)+" Chapter:"+str(chapterIndex + 1))
                            tsv_writer.writerow(["target_verse", "size", "missing_chapter", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)+str(chapterIndex + 1).zfill(3)])
                    
                except:
                    if(bookIndex + 1 <= 66):#Exclude apocrypha
                        print("Chapter Size - Missing Book - "+tsv_vrs_name_files[2] + " Book: " + str(bookIndex + 1))
                        tsv_writer.writerow(["target_verse", "size", "missing_book", tsv_vrs_name_files[2], str(bookIndex + 1).zfill(2)])