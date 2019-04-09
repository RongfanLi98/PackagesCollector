# coding = utf-8
import os
import sys
import re
import json


class PackageSeeker(object):
    def __init__(self):
        self.package_list = []
        self.modules = sys.modules.keys()

    def get_package_list(self, directory, write=True):
        # get a new list, so that the txt will not be created in a dir without target file
        path_list = []
        files = os.listdir(directory)
        # get the path list of target under directory
        for file in files:
            file_path = os.path.join(directory, file)
            # skip the directories whose name starts with .
            if os.path.isdir(file_path):
                if file[0] == '.':
                    pass
                else:
                    self.get_package_list(file_path, write)
            else:
                # note that some files don't have postfix, like dockerfile
                file_name = file.split('.')
                if len(file_name) > 1 and file_name[len(file_name) - 1] == 'ipynb':
                    path_list.append(file_path)
        # parse targets and get package list
        package_list = self.parse_targets(path_list)
        package_list = self.sort_and_remove_dupicate(package_list)
        if write and package_list:
            self.write_to_requirements(directory, package_list)

    def get_all_package_list(self, directory):
        p = self.collect_requirements(directory)
        p = self.sort_and_remove_dupicate(p)
        self.write_to_requirements(directory, p)

    def parse_targets(self, path_list):
        # parse target file and get the path_list
        regular = r"\"from\s+(\w*)(?:\.\w+)?\s+(?:import\s+[\*\w*])(?:\sas\s\w+)?\s*|\"import\s+(\w+)(?:\s+as\s\w+)?\s*"
        reg = re.compile(regular)
        package_list = []
        for file_path in path_list:
            file = open(file_path, 'r', encoding='utf-8')
            content = file.read()
            packages = re.findall(reg, content)
            for p in packages:
                if p[0] != '':
                    package_list.append(p[0])
                elif p[1] != '':
                    package_list.append(p[1])
        return package_list

    def write_to_requirements(self, directory, package_list):
        # write a requirements.txt under directory
        requirements_path = os.path.join(directory, 'requirements.txt')
        # to avoid duplicate data, use w
        with open(requirements_path, 'w', encoding='UTF-8') as file:
            for p in package_list:
                file.write(p+'\n')

    def write_to_dockerfile(self):
        pass

    def write_to_json(self, directory):
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
                    self.write_to_json(file_path)
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

    def sort_and_remove_dupicate(self, package_list):
        # note that set() return a new set
        package_list = list(set(package_list))
        # note that sort() doesn't return anything
        package_list.sort()
        return package_list

    def clear_files(self, directory, file_name='requirements.txt'):
        files = os.listdir(directory)
        # get the path list of target under directory
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path):
                self.clear_files(file_path)
            elif file == file_name:
                os.remove(file_path)

    def collect_requirements(self, directory):
        file_name = 'requirements.txt'
        files = os.listdir(directory)
        package_list = []
        # get the path list of target under directory
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path):
                package_list.extend(self.collect_requirements(file_path))
            elif file == file_name:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        package = line.strip()
                        if package not in self.modules:
                            package_list.append(package)
                        # todo: pip conda
        return package_list


print(sys.argv)
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = r'E:\MyProjects\notebooks'

Seeker = PackageSeeker()
# Seeker.clear_files(path)
# Seeker.get_package_list(path)
# Seeker.write_to_json(path)
Seeker.get_all_package_list(path)
# print(Seeker.collect_requirements(path))
print('pandas' in sys.modules.keys())


