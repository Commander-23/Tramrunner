import json, pathlib

def write_to_json(json_data: dict, file_name: str):
    """
    output path:
        tramrunner/data/generated_files/
    """
    base_dir = pathlib.Path(__file__).parent.parent.parent
    json_dir = base_dir/'data'/'generated_files'
    output_path = json_dir/file_name
    with open(output_path, mode='w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)