from pathlib import Path

def get_target_file_location(directory: str, project_name: str, language: str):
    output_file_location = Path(directory) / language / f"target_{project_name}.tsv"
    return output_file_location.__str__()