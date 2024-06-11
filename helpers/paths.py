def get_target_file_location(directory:str, project_name:str, language:str):
    output_file_location = directory + "/"+language + "/target_" + project_name + ".tsv"
    return output_file_location