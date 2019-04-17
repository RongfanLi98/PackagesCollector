from conda.cli import python_api
from pip._internal import main as pip_main
from pip._internal.commands import search
import os


def conda_search(package: str) -> str:
    """
    if found package on conda, return the latest version, if not, return "not found"
    note that the name must be exactly right

    :param package: name of the package
    :return: version, or ""
    """
    from conda.exceptions import PackagesNotFoundError
    try:
        r = python_api.run_command(python_api.Commands.SEARCH, package)
        # get the list of stdout
        r = r[0].splitlines()[-1]
        package_info = r.split()
        if package_info[0] == package:
            # check again and return the name
            return package_info[1]
        else:
            # PackagesNotFoundError needs args, so we return manually
            print("search for  %-10s but only find  %-10s" % (package, package_info[0]))
            return ""
    except PackagesNotFoundError:
        print("The following packages are not available from current channels:    ", package)
        return ""


def run_conda_command(command: str):
    """
    ensure that the second word should be one of clean, install, search...
    :param command: such like "conda search flask"
    :return: the run_command result
    """
    command = command.split()
    # remove "conda"
    command.pop(0)
    r = python_api.run_command(command.pop(0), *command)
    return r


def pip_search(packages, directory) -> str:
    # pip automatically send message to stdout by logging module, so we need to redirect it
    import sys
    if isinstance(packages, str):
        packages = [packages]
    packages.insert(0, "search")

    console = sys.stdout
    cache = open(os.path.join(directory, "search_result.txt"), "w")
    sys.stdout = cache
    code = pip_main(packages)
    sys.stdout = console

    if code == 0:
        print("please check search_result.txt under %s" % directory)
    else:
        print("something wrong when running pip_search")

    return ""
