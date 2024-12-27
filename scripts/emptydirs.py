import os
import sys


args = sys.argv[1:] if len(sys.argv) > 1 else [os.getcwd()]


def is_empty(dirpath, dirnames, filenames):
    if dirpath.endswith(("/.git", "/.hg")):
        return False

    return not bool(filenames or dirnames)  # not empty


for root in args:
    for dirpath, dirnames, filenames in os.walk(root):
        if is_empty(dirpath, dirnames, filenames):
            print(f"{dirpath}")
