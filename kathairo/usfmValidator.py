from usfm_grammar import USFMParser

#use the parser to check our USFM and USX for Errors
#Then be able to check them all at once in a row
#then tie that in to the other stuff such that we have
#Pre-Test
    #validate the raw USFM and USX files
    #report
#TSV Generation
    #For each file that doesn't have issues, make a TSV
#Run post generation tests on the quality of the TSVs

input_usfm_str = open("./resources/bsb_usfm/50EPHBSB.SFM","r", encoding='utf8').read()
my_parser = USFMParser(input_usfm_str)

errors = my_parser.errors
print(errors)