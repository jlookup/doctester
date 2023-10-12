
from pathlib import Path
import doctest
import importlib
import sys


def get_files_in(dir:str|Path) -> list[Path]:
    """Returns all files within the directory or subdirectories.

    Raises:
        RecursionError: if your directory is `highly` nested.
    """
    d = Path(dir)

    # TODO: raise exception
    if not d.exists(): #or not d.is_dir():
        return None

    contents:list[Path] = [e for e in d.iterdir()]
    files = []
    for e in contents:
        if e.is_file():
            files.append(e)
        elif e.is_dir():
            files.extend(get_files_in(e))

    return files


def get_python_files_in(dir) -> list[Path]:
    """Returns all files ending in .py within the directory or subdirectories.
    """
    files = get_files_in(dir)
    py_files = [f for f in files if f.suffix == '.py']

    return py_files 


def import_module_from_path(path:[str|Path], alias:str=None) -> bool:
    """Imports a python module from the file path.
    
    Args:
        path (str|Path): The path to the python file to be imported.
        alias (str): Optional name to import under.
    """
    # make sure cwd is in PATH
    wd = Path.cwd()
    sys.path.append(str(wd))

    # get file path relative to cwd
    dir = Path(wd / path)
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

__all__ = ['run_doctests_in']


if __name__ == '__main__':
    import click
    @click.command(context_settings=dict(ignore_unknown_options=True))
    @click.option('--dir', '-d',
                  prompt='The directory where you want doctests executed',
                  help='Path to the directory to execute')  
    @click.version_option(version="0.0.1")     
    def main(dir):
        """Executes doctests in all modules within `dir`."""
        d = Path(Path.cwd() / dir)
        run_doctests_in(d)    

    main()  
