import pytest
from test import __tsv_vrs_name_files__
import polars as pl
from helpers.strings import is_unicode_punctuation

#Is punctuation excluded 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_exclude_punctuation(tsv_vrs_files):    
    data_frame = pl.read_csv(tsv_vrs_files[0], separator='\t', infer_schema_length=0, quote_char=None)
    for row in data_frame.iter_rows(named=True):
        id = row["id"]
        token = row["text"]
        exclude = row["exclude"]
        
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
            assert token_is_punct == exclude_bool, tsv_vrs_files[2] + " {} ".format(id) + "punctutation is not marked as excluded"
        
#Is bracketed text excluded 
@pytest.mark.parametrize("tsv_vrs_files", __tsv_vrs_name_files__)
def test_exclude_bracketed_text(tsv_vrs_files):    
    
    if ("RSB" in tsv_vrs_files[0]):
        
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
    print(tsv_vrs_files[0])
    if ("IRVHin" in tsv_vrs_files[0]):
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