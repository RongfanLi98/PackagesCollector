# coding = utf-8
import json
import os
from typing import List


def merge_dict(primary_dict: dict) -> dict:
    # merge list under the same directory
    merged_dict = {}
    for key in primary_dict.keys():
        directory = os.path.split(key)[0]
        if merged_dict.get(directory):
            merged_dict[directory].extend(primary_dict[key])
        else:
            merged_dict.update({directory: primary_dict[key]})
            
    for key in merged_dict.keys():
        merged_dict[key] = sort_and_remove_duplicate(merged_dict[key])
        
    return merged_dict
    
    
def write_to_requirement(content_json: str):
    # write to a requirement file follow the json
    content_dict = json.loads(content_json)
    requirements_dict = merge_dict(content_dict)

    for key in requirements_dict.keys():
        requirements_file = os.path.join(key, "requirements.txt")
        with open(requirements_file, "w", encoding='utf-8') as file:
            for i in requirements_dict[key]:
                file.write(i + "\n")


def write_notebook_name_to_json(directory: str):
    # add index.json under directory
    labs = []
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        # skip the directories whose name starts with .
        if os.path.isdir(file_path):
            if file[0] == '.':
                pass
            else:
                write_notebook_name_to_json(file_path)
        else:
            # note that some files don't have postfix, like dockerfile
            file_name = file.split('.')
            if len(file_name) > 1 and file_name.pop(len(file_name) - 1) == 'ipynb':
                labs.append({file: '.'.join(file_name)})
    if labs:
        labs = {'labs': labs}
        json_str = json.dumps(labs, indent=4, ensure_ascii=False)
        with open(os.path.join(directory, 'index.json'), 'w', encoding='UTF-8') as json_file:
            json_file.write(json_str)


def sort_and_remove_duplicate(target_list: List) -> List:
    # note that set() return a new set
    target_list = list(set(target_list))
    # note that sort() doesn't return anything
    target_list.sort()
    return target_list
