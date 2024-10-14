def get_target_file_location(directory:str, project_name:str, language:str):
    output_file_location = directory + "/"+language + "/target_" + project_name + ".tsv"
    return output_file_location

import importlib.util
import sys

def import_module_from_path(module_name, file_path):
    if(file_path is None):
        return None
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module