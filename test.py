from ContentCollector import seeker
from ContentCollector import writer


i = seeker.get_python_packages_json(r'E:\MyProjects\PackageSeeker_test_files')
# i = seeker.get_content_list_from_file('E:\\MyProjects\\PackageSeeker_test_files\\moviespider.py', [])
print(i)
writer.write_to_requirement(i, with_version=True)
# writer.write_notebook_name_to_json(r'E:\MyProjects\PackageSeeker_test_files')

