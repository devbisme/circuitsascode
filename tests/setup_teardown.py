import os

import pytest
from skidl import (
    ALL_TOOLS,
    INITIAL_QUERY_BACKUP_LIB,
    KICAD,
    SKIDL,
    lib_search_paths,
    no_files,
    set_default_tool,
    set_query_backup_lib,
)

import circuitsascode as casc

no_files()

this_file_dir = os.path.dirname(os.path.abspath(__file__))

files_at_start = set([])


def setup_function(f):
    # Record files originally in directory so we know which ones not to delete.
    global files_at_start
    files_at_start = set(os.listdir(os.getcwd()))

    # Mini-reset to remove circuitry but retain any loaded libraries.
    default_circuit.mini_reset()

    lib_search_paths.clear()
    lib_search_paths.update({tool: [os.getcwd(), this_file_dir] for tool in ALL_TOOLS})
    lib_search_paths.update(
        {SKIDL: [os.getcwd(), this_file_dir, get_filename("../skidl/libs")]}
    )

    set_default_tool(KICAD)
    set_query_backup_lib(INITIAL_QUERY_BACKUP_LIB)


def teardown_function(f):
    # Delete files created during testing.
    files_at_end = set(os.listdir(os.getcwd()))
    for file in files_at_end - files_at_start:
        try:
            os.remove(file)
        except Exception:
            pass


def get_filename(fn):
    """
    Resolves a filename relative to the "tests" directory.
    """
    abs_fn = fn if os.path.isabs(fn) else os.path.join(this_file_dir, fn)
    return os.path.realpath(abs_fn)


if __name__ == "__main__":
    setup_function(None)
    with open("test.txt", "wb") as f:
        f.write("test")
    teardown_function(None)
