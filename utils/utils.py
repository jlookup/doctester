
import pathlib
import doctest
import importlib
import sys


def get_files_in(dir:str|pathlib.Path) -> list[pathlib.Path]:
    """Returns all files within the directory or subdirectories."""
    d = pathlib.Path(dir)

    # TODO: raise exception
    if not d.exists(): #or not d.is_dir():
        return None

    contents:list[pathlib.Path] = [e for e in d.iterdir()]
    files = []
    for e in contents:
        if e.is_file():
            files.append(e)
        elif e.is_dir():
            files.extend(get_files_in(e))

    return files


def get_python_files_in(dir) -> list[pathlib.Path]:
    """Returns all files ending in .py within the directory or subdirectories.
    """
    files = get_files_in(dir)
    py_files = [f for f in files if f.suffix == '.py']

    return py_files 


def import_module_from_path(path:[str|pathlib.Path], alias:str=None) -> bool:
    """Imports a python module from the file path.
    
    Args:
        path (str|Path): The path to the python file to be imported.
        alias (str): Optional name to import under.
    """
    # make sure cwd is in PATH
    wd = pathlib.Path.cwd()
    sys.path.append(str(wd))

    # get file path relative to cwd
    dir = pathlib.Path(wd / path)
    mod_name = dir.relative_to(wd)

    # format module name for importlib
    mod_name_list = list(mod_name.parts)
    mod_name_list[-1] = dir.stem
    mod_name_fmt = '.'.join(mod_name_list)
    
    mod = importlib.import_module(mod_name_fmt)
    return mod


def run_doctests_in(dir) -> None:
    """Executes doctest on all .py files in the directory."""
    py_files = get_python_files_in(dir)
    for file in py_files:
        print(f"Running doctests in {file.stem}")
        mod = import_module_from_path(file)
        doctest.testmod(mod)


def is_rjust(array:list) -> bool:
    """checks if all elements of a list are right justified
    
    Examples:
    >>> l1 = ['   2', '3525', ' 233']
    >>> is_rjust(l1)
    True

    >>> l2 = ['2345', '3456', '4567']
    >>> is_rjust(l2)
    True

    >>> l3 = ['2345', '3456', '4500']
    >>> is_rjust(l3)
    True    

    >>> l4 = ['2345', '3456', '456700']
    >>> is_rjust(l4)
    False    

    >>> l5 = ['2345 ', '3456 ', '45670']
    >>> is_rjust(l5)
    False 

    """
    # naive version:
    # get max length of the elements of the list
    # check that all elements match that length 
    # check that no elements are left-padded
    # return True
    lengths = set(len(e) for e in array)
    is_rjustified = (len(lengths) == 1 
                     and all((1 if e == e.rstrip()
                              else 0 for e in array)))

    return is_rjustified

if __name__ == '__main__':
    d = '0_0'
    run_doctests_in(d)
