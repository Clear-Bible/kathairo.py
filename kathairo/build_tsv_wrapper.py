import subprocess
import json

json_file = "kathairo/Prompts/prompts.json"

with open(json_file) as json_data:
    jsonData = json.load(json_data)
    for jsonObject in jsonData:
        jsonKeys = jsonObject.keys()

        commandToRunList = [
            'poetry',
            'run',
            'python',
            'kathairo/build_tsv_args_parser.py'
                            ]
        
        for key in jsonKeys:
            commandToRunList.append("--"+key)
            if(type(jsonObject[key]) != bool):
                commandToRunList.append(jsonObject[key])

        try:
            subprocess.Popen(commandToRunList)
            commandToRunList.append("--"+"runBuildWordLevelTsv")
            subprocess.Popen(commandToRunList)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running wrapper.py: {e}")
        except FileNotFoundError:
            print("Error: wrapper.py not found. Make sure the file exists.")