from ContentCollector import seeker
from ContentCollector import writer
import os
from typing import List


def remove_local_lib(package_list: List[str]) -> List[str]:
    # check local library
    lib = os.path.split(os.__file__)[0]
    print(lib)


path_list = ['E:\\MyProjects\\PackageSeeker_test_files\\base\\python_base\\7、对象.ipynb',
             'E:\\MyProjects\\PackageSeeker_test_files\\base\\python_base\\data\\a.py',
             'E:\\MyProjects\\PackageSeeker_test_files\\moviespider.py',
             'E:\\MyProjects\\PackageSeeker_test_files\\music.py',
             'E:\\MyProjects\\PackageSeeker_test_files\\practicalAI\\1.线性回归.ipynb',
             'E:\\MyProjects\\PackageSeeker_test_files\\base\\python_advance\\爬虫.ipynb']
regex_list = []

i = seeker.get_packages(r'E:\MyProjects\PackageSeeker_test_files')
i = seeker.get_content_list_from_file('E:\\MyProjects\\PackageSeeker_test_files\\moviespider.py', [])
# writer.write_to_requirement(i, True)
# writer.write_notebook_name_to_json(r'E:\MyProjects\PackageSeeker_test_files')
print(i)
remove_local_lib(i)
