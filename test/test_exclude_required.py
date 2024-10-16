import pytest
from test import __tsv_vrs_name_files__
import polars as pl
import regex as re
from helpers.strings import is_unicode_punctuation

@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_exclude_outer_punctuation(tsv_vrs_files):    
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0, quote_char=None)
    regex_rules_class = tsv_vrs_files[7]
    WORD_LEVEL_PUNCT_REGEX = regex_rules_class.WORD_LEVEL_PUNCT_REGEX
    
    previous_row = None
    current_row = None
    for next_row in data_frame.iter_rows(named=True):
        
        if(previous_row is not None):
            previous_id = previous_row["id"]
            previous_token = previous_row["text"]
            previous_exclude = previous_row["exclude"]
            previous_skip_space_after = previous_row["skip_space_after"]
            
        if(next_row is not None):    
            next_id = next_row["id"]
            next_token = next_row["text"]
            next_exclude = next_row["exclude"]
            next_skip_space_after = next_row["skip_space_after"]
        
        if(current_row is not None):
            current_id = current_row["id"]
            current_token = current_row["text"]
            current_exclude = current_row["exclude"]
            current_skip_space_after = current_row["skip_space_after"]
        
            if(current_exclude == 'y'):
                exclude_bool = True
            else:
                exclude_bool = False
            
            token_is_punct = True
            if (isinstance(current_token, str) and len(current_token)>0):
                for char in current_token:
                    if(not is_unicode_punctuation(char)):
                        token_is_punct = False
                        break
                
            if(not token_is_punct):
                previous_row = current_row
                current_row = next_row
                continue
            
            previous_space = ""
            if(previous_skip_space_after != 'y'):
                previous_space = " "
            
            current_space = ""
            if(current_skip_space_after != 'y'):
                current_space = " "
            
            substring = previous_token + previous_space + current_token + current_space + next_token
            index = len(previous_token + previous_space + current_token) - 1
            token_is_word_level_punct = False
            match = WORD_LEVEL_PUNCT_REGEX.match(substring, index)
            if match is not None:
                token_is_word_level_punct = True
                #group = match.group()
                #print(substring, " :: ", group, " :: ", index)
                
            if(token_is_word_level_punct):
                assert token_is_word_level_punct != exclude_bool, tsv_vrs_files[2] + " {} ".format(id) + "inner punctuation is marked as excluded: " + substring
            else:
                assert token_is_word_level_punct == exclude_bool, tsv_vrs_files[2] + " {} ".format(id) + "outer punctuation is not marked as excluded: " + substring
        
        previous_row = current_row
        current_row = next_row
        
#Is punctuation excluded 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_punctuation_not_required(tsv_vrs_files):    
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0, quote_char=None)
    for row in data_frame.iter_rows(named=True):
        id = row["id"]
        token = row["text"]
        required = row["required"]
        
        if(required == 'y'):
            required_bool = True
        else:
            required_bool = False
        
        token_is_punct = True
        if (isinstance(token, str) and len(token)>0):
            for char in token:
                if(not is_unicode_punctuation(char)):
                    token_is_punct = False
                    break
        
        if(token_is_punct):
            assert token_is_punct != required_bool, tsv_vrs_files[2] + " {} ".format(id) + "punctuation is not marked as required"
        
#Is bracketed text excluded 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_exclude_bracketed_text(tsv_vrs_files):    
    if (tsv_vrs_files[5]):
        in_brackets = False
        
        data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0, quote_char=None)
        for row in data_frame.iter_rows(named=True):
            
            id = row["id"]
            token = row["text"]
            exclude = row["exclude"]
            
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
                    assert(in_brackets == exclude_bool), tsv_vrs_files[2] + " {} ".format(id) + "bracketed content not marked as excluded"
                
                if(char ==']'):
                    in_brackets = False
                
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_cross_references_are_excluded(tsv_vrs_files):    
    if (tsv_vrs_files[6]):
        in_parentheses = False
        is_cross_reference = False
        unprinted_parenthetical_token_list = []
        #use prompts to control if this test gets skipped

        data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0, quote_char=None)
        for row in data_frame.iter_rows(named=True):

            id = str(row["id"])
            token = str(row["text"])
            
            if(not in_parentheses):
                if(is_cross_reference):
                    for unprinted_parenthetical_token in unprinted_parenthetical_token_list:
                        assert(unprinted_parenthetical_token["exclude"] == "y"), tsv_vrs_files[2] + " {} ".format(id) + "cross-reference not excluded"
                    is_cross_reference = False
                unprinted_parenthetical_token_list.clear()
            
            for char in token:
                if(char == '('):
                    in_parentheses = True
                if(in_parentheses and char == ':'):
                    is_cross_reference = True
            
            if(in_parentheses):    
                unprinted_parenthetical_token_list.append(row)
            
            if(')' in token):
                in_parentheses = False