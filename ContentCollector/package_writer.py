# coding = utf-8
# 如何去生成txt
import json
import os


def write_to_requirement(content_json: str):
    content_dict = json.loads(content_json)
    for key in content_dict.keys():
        directory = os.path.split(key)[0]
        requirements = os.path.join(directory, "requirements.txt")
        with open(requirements, "w", encoding='utf-8') as file:
            for i in content_dict[key]:
                file.write(i + "\n")


