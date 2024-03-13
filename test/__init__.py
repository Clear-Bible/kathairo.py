#__macula_greek_tsv_rows__ = []

#TODO have common method of creating TSV file name
#tsv_path = "../TSVs/target_BSB_USX_new.tsv"
__tsv_vrs_files__ = []#tsv_path

#vrs_path = "../resources/bsb_usx/release/versification.vrs"
#__vrs_files__ = []#vrs_path

#TODO combine with wrapper.py and abstract it to reduce duplication
import json

json_file = "kathairo/prompts.json"

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
        
        prompt_tsv_vrs = [outputFileLocation, targetVersificationPath]
        __tsv_vrs_files__.append(prompt_tsv_vrs)


#with open(tsv_path, encoding='utf-8') as file:
#    reader = csv.DictReader(file, delimiter="\t")
#    for row in reader:
#        __macula_greek_tsv_rows__.append(row)