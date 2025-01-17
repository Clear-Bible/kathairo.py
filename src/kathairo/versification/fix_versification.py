from machine.scripture import Versification, VerseRef, ORIGINAL_VERSIFICATION
import polars as pl
import os

def fix_versification_file(versification_path, versification_issues_path):
    versification = Versification.load(versification_path)
    
    size = os.path.getsize(versification_issues_path)
    if(size == 0):
        return
    
    versification_issues_df = pl.read_csv(versification_issues_path, separator='\t', infer_schema_length=0, has_header=False)
    
    fixed_versification = fix_versification(versification, versification_issues_df)
    save_versification(versification_path, fixed_versification)
    
    #save_versification(versification_path, versification)

def fix_versification(versification, versification_issues_df):
    for issue in versification_issues_df.iter_rows():
        if(issue[0]=="source_verse" and issue[2]=="miss_end_verse"):
            versification = fix_missing_end_verses_in_source_verse_column(versification, issue[4], issue[5])
    return versification

def fix_missing_end_verses_in_source_verse_column(versification:Versification, current_verse_id, is_missing_verse_in_id_column):
    next_chapter = str(int(current_verse_id[3:5])+1).zfill(3)
    
    next_verse_id = current_verse_id[0:2] + next_chapter + '001'
    
    current_verse_ref = VerseRef.from_bbbcccvvv(int(current_verse_id), ORIGINAL_VERSIFICATION)
    next_verse_ref = VerseRef.from_bbbcccvvv(int(next_verse_id), ORIGINAL_VERSIFICATION)

    if(is_missing_verse_in_id_column == "True"):
        versification.mappings.add_mapping(current_verse_ref, current_verse_ref)    
        versification.mappings.add_mapping(current_verse_ref, next_verse_ref)
    else:
        versification.mappings.add_mapping(next_verse_ref, next_verse_ref)
        versification.mappings.add_mapping(next_verse_ref, current_verse_ref)
    
    return versification

def save_versification(versification_path, versification:Versification):
    with open(versification_path, "w", encoding="utf-8") as file:
        
        file.write(f'# Versification  "{versification.name}"\n')
        for book, book_size_array in zip(bible_book_abbreviations, versification.book_list):
            book_size_line = book
            
            current_chapter = 1
            for end_verse in book_size_array:
                book_size_line += f" {current_chapter}:{end_verse}"
                current_chapter += 1
                
            file.write(f'{book_size_line}\n')
        
        mappings_list = []
        
        for key in versification.mappings._standard_to_versification:
            mapping_id = versification.mappings._standard_to_versification[key].bbbcccvvvs + key.bbbcccvvvs
            mapping = f'{versification.mappings._standard_to_versification[key]} = {key}\n'
            mapping_id_pair = (mapping_id, mapping)
            if(mapping_id_pair not in mappings_list):
                mappings_list.append(mapping_id_pair)

        for key in versification.mappings._versification_to_standard:
            mapping_id =  key.bbbcccvvvs + (versification.mappings._versification_to_standard[key]).bbbcccvvvs
            mapping = f'{key} = {versification.mappings._versification_to_standard[key]}\n'
            mapping_id_pair = (mapping_id, mapping)
            if(mapping_id_pair not in mappings_list):
                mappings_list.append(mapping_id_pair)
        
        sorted_mappings_list = sorted(mappings_list, key=lambda x: x[0])  # Sort by ID (first element)
        
        for mapping in sorted_mappings_list:
            file.write(mapping[1])

bible_book_abbreviations = [
    'GEN',
    'EXO',
    'LEV',
    'NUM',
    'DEU',
    'JOS',
    'JDG',
    'RUT',
    '1SA',
    '2SA',
    '1KI',
    '2KI',
    '1CH',
    '2CH',
    'EZR',
    'NEH',
    'EST',
    'JOB',
    'PSA',
    'PRO',
    'ECC',
    'SNG',
    'ISA',
    'JER',
    'LAM',
    'EZK',
    'DAN',
    'HOS',
    'JOL',
    'AMO',
    'OBA',
    'JON',
    'MIC',
    'NAM',
    'HAB',
    'ZEP',
    'HAG',
    'ZEC',
    'MAL',
    'MAT',
    'MRK',
    'LUK',
    'JHN',
    'ACT',
    'ROM',
    '1CO',
    '2CO',
    'GAL',
    'EPH',
    'PHP',
    'COL',
    '1TH',
    '2TH',
    '1TI',
    '2TI',
    'TIT',
    'PHM',
    'HEB',
    'JAS',
    '1PE',
    '2PE',
    '1JN',
    '2JN',
    '3JN',
    'JUD',
    'REV'
]

#fix_versification_file("src/kathairo/versification/versification.vrs", "src/kathairo/versification/source_size_issues_AVD.tsv")