from ContentCollector import seeker
from ContentCollector import writer


path_list = ['E:\\MyProjects\\PackageSeeker_test_files\\base\\python_base\\7、对象.ipynb',
             'E:\\MyProjects\\PackageSeeker_test_files\\base\\python_base\\data\\a.py',
             'E:\\MyProjects\\PackageSeeker_test_files\\moviespider.py',
             'E:\\MyProjects\\PackageSeeker_test_files\\music.py',
             'E:\\MyProjects\\PackageSeeker_test_files\\practicalAI\\1.线性回归.ipynb',
             'E:\\MyProjects\\PackageSeeker_test_files\\base\\python_advance\\爬虫.ipynb']
regex_list = []

i = seeker.get_python_packages_json(r'E:\MyProjects\PackageSeeker_test_files')
# i = seeker.get_content_list_from_file('E:\\MyProjects\\PackageSeeker_test_files\\moviespider.py', [])
print(i)
# writer.write_to_requirement(i, True)
# writer.write_notebook_name_to_json(r'E:\MyProjects\PackageSeeker_test_files')
# i = ['json', 're', 'requests', 'os', 'bs4', 'typing', 'math', 'multiprocessing']

