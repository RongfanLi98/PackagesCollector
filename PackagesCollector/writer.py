# coding = utf-8
import json
import os
from typing import List
from PackagesCollector import verifier, seeker


def merge_dict(primary_dict: dict) -> dict:
    """
    merge list under the same directory
    :param primary_dict: primary_dict has file paths as keys
    :return: merged_dict has directory paths as keys, and the values are merged from the values under the same
    dir in primary_dict
    """
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
    
    
def write_to_requirement(content_json: str, with_version=False):
    # write to a requirement file follow the json
    content_dict = json.loads(content_json)
    requirements_dict = merge_dict(content_dict)

    for key in requirements_dict.keys():
        # keys are file paths
        requirements_file = os.path.join(key, "requirements.txt")
        with open(requirements_file, "w", encoding='utf-8') as file:
            for i in requirements_dict[key]:
                if with_version:
                    version = verifier.conda_search(i)
                    if version:
                        file.write(i + "==" + version + "\n")
                    else:
                        file.write(i + "\n")
                else:
                    file.write(i + "\n")


def write_to_one_requirement(directory, with_version=False):
    path_list = seeker.get_path_list(directory, [])
    content_json = seeker.get_content_json_from_files(path_list, [])
    content_dict = json.loads(content_json)
    requirements_list = []

    for key in content_dict:
        requirements_list.extend(content_dict[key])
    requirements_list = sort_and_remove_duplicate(requirements_list)
    requirements_file = os.path.join(directory, "requirements.txt")
    with open(requirements_file, "w", encoding='utf-8') as file:
        for i in requirements_list:
            if with_version:
                version = verifier.conda_search(i)
                if version:
                    file.write(i + "==" + version + "\n")
                else:
                    file.write(i + "\n")
            else:
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


def clear_files(directory, file_name='requirements.txt'):
    files = os.listdir(directory)
    # get the path list of target under directory
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            clear_files(file_path)
        elif file == file_name:
            os.remove(file_path)


def sort_and_remove_duplicate(target_list: List) -> List:
    # note that set() return a new set
    target_list = list(set(target_list))
    # note that sort() doesn't return anything
    target_list.sort()
    return target_list
