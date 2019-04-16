from conda.cli import python_api


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
