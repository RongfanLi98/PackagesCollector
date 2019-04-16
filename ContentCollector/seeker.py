r"""
Package seeker
"""
# coding = utf-8
import os
import re
import json
from typing import List
import requests

regex_for_python_packages = \
    [r"from\s+(\w*)(?:\.\w+)?\s+(?:import\s+[\*\w*])(?:\sas\s\w+)?\s*|import\s+(\w+)(?:\s+as\s\w+)?\s*"]
regex_for_ipynb_packages = \
    [r"\"from\s+(\w*)(?:\.\w+)?\s+(?:import\s+[\*\w*])(?:\sas\s\w+)?\s*|\"import\s+(\w+)(?:\s+as\s\w+)?\s*"]
python_37_std_lib = ['__future__', '__main__', '_dummy_thread', '_thread', 'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat',
     'asyncio', 'asyncore', 'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2',
     'cProfile', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections',
     'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg',
     'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils',
     'doctest', 'dummy_threading', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl',
     'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass',
     'gettext', 'glob', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp',
     'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale',
     'logging', 'lzma', 'macpath', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder',
     'msilib', 'msvcrt', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'numbers', 'operator', 'optparse', 'os',
     'ossaudiodev', 'parser', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib',
     'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue',
     'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets',
     'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket',
     'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess',
     'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile',
     'termios', 'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace',
     'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest',
     'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound', 'wsgiref',
     'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib']


def get_path_list(directory: str, regex_list: List[str]) -> List:
    # get a file path list, in which the path names match the regular expression
    if not regex_list:
        regex_list = [r'\.py', r'\.ipynb']
    path_list = []
    files = os.listdir(directory)
    # get the path list of target under directory
    for file in files:
        file_path = os.path.join(directory, file)
        # skip the directories whose name starts with .
        if os.path.isdir(file_path):
            path_list.extend(get_path_list(file_path, regex_list))
        else:
            # note that some files don't have postfix, like dockerfile and some file have multi .
            if regex_list:
                mark = False
                for regex in regex_list:
                    # match more than once
                    if re.findall(regex, file):
                        mark = True
                if mark:
                    path_list.append(file_path)
            else:
                path_list.append(file_path)
    return path_list


def get_content_list_from_file(file_path: str, regex_list: List[str]) -> List:
    # search in the given file, return what it found
    if not file_path:
        print("path is empty")
        return []
    if not regex_list:
        regex_list = regex_for_python_packages
        regex_list.extend(regex_for_ipynb_packages)

    content_list = []
    file = open(file_path, 'r', encoding='utf-8')
    content = file.read()
    for regex in regex_list:
        packages = re.findall(regex, content)
        for package in packages:
            if package[0]:
                content_list.append(package[0])
            else:
                content_list.append(package[1])

    content_list = sort_and_remove_duplicate(content_list)
    content_list = remove_standard_lib_from_list(content_list)
    return content_list


def get_content_json_from_files(path_list: List[str], regex_list: List[str]) -> str:
    # every file in path_list will be searched by every regex in regex_list, add file path and content list in one json
    if not path_list:
        print("path_list is empty")
        return ""
    if isinstance(path_list, str):
        path_list = [path_list]

    content_dict = {}
    if regex_list:
        for file_path in path_list:
            content_list = get_content_list_from_file(file_path, regex_list)
            content_dict[file_path] = content_list
    else:
        # if regex_list is empty, find python packages, there may be import os in notebook's text field, so we do twice
        print("regex_list is empty, finding python packages in .py and .ipynb files...")
        #
        py_list = []
        ipynb_list = []
        content_dict = {}
        for path in path_list[:]:
            postfix = os.path.splitext(path)[-1]
            if postfix == ".py":
                py_list.append(path)
                path_list.remove(path)
            elif postfix == ".ipynb":
                ipynb_list.append(path)
                path_list.remove(path)

        ipynb_json = get_content_json_from_files(ipynb_list, regex_for_ipynb_packages)
        py_json = get_content_json_from_files(py_list, regex_for_python_packages)

        if ipynb_json:
            content_dict.update(json.loads(ipynb_json))
        if py_json:
            content_dict.update(json.loads(py_json))
    return json.dumps(content_dict, indent=4, ensure_ascii=False)


def remove_standard_lib_from_list(package_list: List[str], version=3.7) -> List[str]:
    """
    remove packages that already exist in standard library. The version must be one of 3, 3.5, 3.6, 3.7, 3.8.
    If don't select the 3.7 version, search https://docs.python.org/3/py-modindex.html for details.
    :param package_list:
    :param version: python version
    :return:
    """
    if version == 3.7:
        std_lib_list = python_37_std_lib
    else:
        url = r"https://docs.python.org/" + str(version) + "/py-modindex.html"
        context = requests.get(url).text
        regex = r"<code class=\"xref\">(\w*)(?:\.\w*)*</code>"
        regex = re.compile(regex)
        std_lib_list = re.findall(regex, context)
        std_lib_list = list(set(std_lib_list))

    for package in package_list[:]:
        if package in std_lib_list:
            package_list.remove(package)

    return package_list


def get_python_packages_json(directory: str = "./") -> str:
    # get python packages under directory
    path_list = get_path_list(directory, [])
    return get_content_json_from_files(path_list, [])


def sort_and_remove_duplicate(target_list: List) -> List:
    # note that set() return a new set
    target_list = list(set(target_list))
    # note that sort() doesn't return anything
    target_list.sort()
    return target_list
