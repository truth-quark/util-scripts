import os
import sys


args = sys.argv[1:] if len(sys.argv) > 1 else [os.getcwd()]


def is_included(dirpath, dirnames, filenames):
    if dirpath.endswith(("/.git", "/.hg")):
        return False

    if filenames or dirnames:  # not empty
        return False
        
    return True


for root in args:
    for dirpath, dirnames, filenames in os.walk(root):
        if is_included(dirpath, dirnames, filenames):
            print(f"{dirpath}")
