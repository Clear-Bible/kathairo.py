import csv
from biblelib.word import fromubs
from machine.tokenization import LatinWordTokenizer, WhitespaceTokenizer
import lxml
import tree_sitter
import usfm_grammar
from usfm_grammar import USFMParser, Filter

# input_usfm_str = open("sample.usfm","r", encoding='utf8').read()
input_usfm_str = '''
\\id GEN
\\c 1
\\p
\\v 1 test verse
'''

my_parser = USFMParser(input_usfm_str)

errors = my_parser.errors
print(errors)