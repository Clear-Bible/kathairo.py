import subprocess
import json

json_file = "kathairo\prompts.json"

with open(json_file) as json_data:
    jsonData = json.load(json_data)
    for jsonObject in jsonData:
        jsonKeys = jsonObject.keys()

        commandToRunList = [
            'poetry',
            'run',
            'python',
            'kathairo\main.py'
                            ]
        
        for key in jsonKeys:
            commandToRunList.append("--"+key)
            if(type(jsonObject[key]) != bool):
                commandToRunList.append(jsonObject[key])

        try:
            subprocess.run(commandToRunList, check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running otherScript.py: {e}")
        except FileNotFoundError:
            print("Error: otherScript.py not found. Make sure the file exists.")








