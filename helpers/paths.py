def get_target_file_location(old_tsv_format:bool, directory:str, project_name:str, language:str):
    tsv_format_string = ""
    if(old_tsv_format):
        tsv_format_string = "_old"

    output_file_location = directory + "/"+language + "/target_" + project_name + tsv_format_string + ".tsv"
    return output_file_location