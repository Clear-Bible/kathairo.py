#Based on https://github.com/Clear-Bible/macula-greek/blob/main/test/test_tsv.py
import os
import codecs
import re
import pytest
from test import __macula_greek_tsv_rows__, __tsv_files__
import pandas as pd

# Verify that the file exists.
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_files_exists(tsv_file):
    size = os.path.getsize(tsv_file)
    assert size > 0

# Verify that the file is in utf8 format.
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_file_is_valid_utf8(tsv_file):
    lines = codecs.open(tsv_file, encoding="utf-8", errors="strict").readlines()
    assert lines != ""

#do the ids only contain numbers
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_id_numeric(tsv_file):
    dataFrame = pd.read_csv(tsv_file, sep='\t',dtype=str)
    for id in dataFrame['id']:
        assert id.isnumeric()


#are the ids valid length
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_id_length(tsv_file):
    dataFrame = pd.read_csv(tsv_file, sep='\t',dtype=str)
    for id in dataFrame['id']:
        assert len(str(id)) == 11

#are the ids valid values (requires versification file)
@pytest.mark.parametrize("tsv_file", __tsv_files__)
def test_id_length(tsv_file):
    dataFrame = pd.read_csv(tsv_file, sep='\t',dtype=str)
    for id in dataFrame['id']:
        assert len(str(id)) == 11



#does each chapter have the number of verses listed in the versification
#is each chapter in the mapping present in the tsv