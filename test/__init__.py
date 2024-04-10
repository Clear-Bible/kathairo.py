import csv
from pathlib import Path
import pandas as pd
from helpers.strings import is_unicode_punctuation
from machine.scripture import Versification

def test_source_chapter_size(tsv_vrs_name_files):
    
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
    
    #for book in book_list:
    #    print(book)
        
    #print("")
    
    #for book in targetVersification.book_list:
    #    print(book)
    
    for bookIndex in range(len(originalVersification.book_list)):
        
        try:
            bookExists = book_list[bookIndex]
            
            for chapterIndex in range(len(originalVersification.book_list[bookIndex])):
        
                try:
                    chapterExists = book_list[bookIndex][chapterIndex]
                    
                    if(bookIndex==18 and chapterIndex==116):
                        holdup=True
                    
                    if (book_list[bookIndex][chapterIndex] > originalVersification.book_list[bookIndex][chapterIndex]): 
                        print("Extra ORG Verse - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1)+":"+str(chapterIndex + 1))
                    elif(book_list[bookIndex][chapterIndex] < originalVersification.book_list[bookIndex][chapterIndex]):
                        print("Missing ORG Verse - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1)+":"+str(chapterIndex + 1))
                except:
                    print("Missing ORG Chapter - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1)+":"+str(chapterIndex + 1))
            
        except:
            if(bookIndex + 1 <= 66):#Exclude apocrypha
                print("Missing ORG Book - "+tsv_vrs_name_files[2] + " Book Id: " + str(bookIndex + 1))

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
        oldTsvFormat = jsonObject.get("oldTsvFormat", False)
        
        tsvFormatString = "new"
        if(oldTsvFormat):
            tsvFormatString = "old"

        outputFileLocation = "TSVs/target_"+projectName+"_"+tsvFormatString+".tsv"
        
        prompt_tsv_vrs = [outputFileLocation, targetVersificationPath, projectName]
        __tsv_vrs_name_files__.append(prompt_tsv_vrs)


#with open(tsv_path, encoding='utf-8') as file:
#    reader = csv.DictReader(file, delimiter="\t")
#    for row in reader:
#        __macula_greek_tsv_rows__.append(row)
     
#for project in __tsv_vrs_name_files__:
#    test_chapter_size(project)

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