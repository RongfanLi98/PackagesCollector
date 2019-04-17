from PackagesCollector import seeker
from PackagesCollector import writer
from PackagesCollector import verifier

directory = r'E:\MyProjects\PackageSeeker_test_files'

# i = seeker.get_python_packages_json(directory)
# i = seeker.get_content_list_from_file('E:\\MyProjects\\PackageSeeker_test_files\\moviespider.py', [])
# print(i)
# writer.write_to_requirement(i, with_version=True)
# writer.write_to_one_requirement(directory, True)
# writer.write_notebook_name_to_json(r'E:\MyProjects\PackageSeeker_test_files')

writer.divide_requirement(r"E:\MyProjects\PackageSeeker_test_files\requirements.txt")
# verifier.pip_search("flask")
