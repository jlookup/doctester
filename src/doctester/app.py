#!.venv/bin/python

import doctest
from pathlib import Path

import click

import doctester
from doctester import file_utils


def run_doctests_in(dir) -> None:
    """Executes doctest on all .py files in the directory."""
    py_files = file_utils.get_python_files_in(dir)
    for file in py_files:
        print(f"Running doctests in {file.stem}")
        mod = file_utils.import_module_from_path(file)
        doctest.testmod(mod)


    @click.command(context_settings=dict(ignore_unknown_options=True))
    @click.option('--dir', '-d',
                  prompt='The directory where you want doctests executed',
                  help='Path to the directory to execute')  
    @click.version_option(version=doctester.__version__)     
    def main(dir):
        """Executes doctests in all modules within `dir`."""
        d = Path(Path.cwd() / dir)
        run_doctests_in(d)    


# if __name__ == '__main__':
#     main()
