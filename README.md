# PackageSeeker
## 功能
包检查器  
本地版的爬虫，针对python包进行了优化  
检查指定路径下的全部ipynb和py文件，自动生成requirements.txt

## 模块内容
1. seeker  
    1. seeker.get_path_list(directory: str, regex_list: List[str])  
    regex_list是储存正则表达式的列表，搜索directory下面的全部文件，找到文件名满足正则表达式的的文件，返回这些文件的路径组成的list。
    2. seeker.get_content_list_from_file(file_path: str, regex_list: List[str])  
    指定文件路径，搜索文件内容中满足正则表达式的内容，返回内容组成的list。  
    若regex_list为空，则按照py文件和ipynb文件的规则，搜索python packages。
    3. seeker.get_content_json_from_files(path_list, regex_list: List[str])  
    path_list可由seeker.get_path_list得到，是path组成的list，同时也支持一个路径字符串。遍历path_list，对每一个path指定的文件，执行get_content_list_from_file。  
    若regex_list为空，则按照py文件和ipynb文件的规则，搜索python packages。  
    返回json格式如下：
        ```json
        {
        "dirpath_one": ["rquests", "re"],
        "dirpath_tow": ["math", "os"]
        }
        ```
    4. seeker.remove_standard_lib_from_list(package_list: List[str], version=3.7)  
    从package_list中，移除标准库中的packages。默认python版本是3.7，可以指定[python standard library](https://docs.python.org/3/py-modindex.html)中提供的版本。  
    返回整理后的list
    5. seeker.get_python_packages_json(directory: str = "./")  
    先后调用get_path_list，get_content_json_from_files。搜索指定文件夹下的全部文件中的python packages，返回json。
    6. seeker.sort_and_remove_duplicate(target_list: List)  
    对于一个list，删除重复内容并排序，返回新的list。

2. writer
    1. writer.merge_dict(primary_dict: dict)  
    指定一个字典，字典格式如seeker.get_content_json_from_files的返回json。返回一个新的字典，key是多个文件的共同的所在目录，value原字典对应的value的整合。
    2. writer.write_to_requirement(content_json: str, with_version=False)  
    按照json内容写requirement，格式与anaconda要求的requirement相同。  
    若with_version=True，则查询每一个依赖在conda中的最新版本，若找不到，则version为'not found'。
    3. writer.write_notebook_name_to_json(directory: str)  
    将目录下所有ipynb的文件名按照预定格式写入json文件。
    4. writer.clear_files(directory, file_name='requirements.txt')  
    删除directory目录下所有指定file_name的文件。
    5. writer.sort_and_remove_duplicate(target_list: List)  
    对于一个list，删除重复内容并排序，返回新的list。

3. verifier
    1. verifier.conda_search(package: str)  
    在conda中查询某个包是否存在，若存在则返回最新版本，若不存在则返回'not found'。
    2. verifier.run_conda_command(command: str)  
    执行conda命令，返回执行结果，需要自行解析。


## 将来的改进方向

1. seeker
    * 对命名进行优化
2. writer
3. verifier
    * 到conda和pip上查询包是否存在，并且确认目前最新版本到requirements。如果有所冲突，保留原文件，判断后填入requirements_conda和requirements_pip，若都不存在则写一个失败文档
    * 查询本地包的版本和最新包的差距
    * 比较本地两个requirement的不同，见[pip-pop](https://github.com/heroku-python/pip-pop)的功能
