from usfm_grammar import USFMParser
from lxml import etree

#use the parser to check our USFM and USX for Errors
#Then be able to check them all at once in a row
#then tie that in to the other stuff such that we have
#Pre-Test
    #validate the raw USFM and USX files
    #report
#TSV Generation
    #For each file that doesn't have issues, make a TSV
#Run post generation tests on the quality of the TSVs

test_xml_file = "./resources/bsb_usx/release/USX_1/ZEC.usx"
with open(test_xml_file, 'r', encoding='utf-8') as usx_file:
    usx_str = usx_file.read()
    usx_obj = etree.fromstring(bytes(usx_str, encoding='utf8'))

    my_parser = USFMParser(from_usx=usx_obj)
    errors = my_parser.errors
    print(errors)
    # print(my_parser.to_usj())
    # print(my_parser.to_list())

#input_usfm_str = open("./resources/bsb_usfm/50EPHBSB.SFM","r", encoding='utf8').read()
#my_parser = USFMParser(input_usfm_str)
#errors = my_parser.errors
#print(errors)