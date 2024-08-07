from machine.scripture import (
    VerseRef,
    Versification,
)
from biblelib.word import fromubs
import regex as re

def set_source_verse(targetVref:VerseRef, sourceVersification:Versification, unused_versification_mapping:dict[VerseRef:VerseRef]) -> tuple:
    
    sourceVref = ""
    source_verse_range_end = ""    
    
    mappings_to_targetVref = [(key, value) for key, value in unused_versification_mapping.items() 
                            if value.bbbcccvvvs == targetVref.bbbcccvvvs]

    for mapping in mappings_to_targetVref:
        unused_versification_mapping.pop(mapping[0])
    
    mappings_to_targetVref_len = len(mappings_to_targetVref)
            
    if(mappings_to_targetVref_len > 0):
        sourceVref = mappings_to_targetVref[0][0]
        if(mappings_to_targetVref_len > 1):
            last_mapping = mappings_to_targetVref[mappings_to_targetVref_len-1]
            last_mapping_key = last_mapping[0]
            source_verse_range_end = fromubs(f"{re.sub(r'[^0-9]', '', last_mapping_key.bbbcccvvvs)}00000").to_bcvid
    
    if(sourceVref == ""):
        targetVref.change_versification(sourceVersification)
        sourceVref = targetVref
    
    return sourceVref, source_verse_range_end