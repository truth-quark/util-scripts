"""
Utility to search file trees for empty directories.
"""

import os
import sys
import argparse


def is_empty(dirpath, dirnames, filenames):
    if dirpath.endswith(("/.git", "/.hg")):
        return False

    return not bool(filenames or dirnames)


def create_parser():
    # TODO: add arg to search version control dirs
    desc = "Search file trees for empty directories."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("dirs",
                        type=str,
                        nargs="*",
                        metavar="F",
                        default=[os.getcwd()],
                        help="Directories to search recursively.")
    return parser


def empty_dirs(directories):
    """
    Recursively search the provided directory paths, yielding empty paths.
    """
    for d in directories:
        for dirpath, dirnames, filenames in os.walk(d):
            if is_empty(dirpath, dirnames, filenames):
                yield f"{dirpath}"


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    for d in empty_dirs(args.dirs):
        print(d)
