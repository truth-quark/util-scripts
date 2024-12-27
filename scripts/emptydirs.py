import os
import sys
import argparse


def is_empty(dirpath, dirnames, filenames):
    if dirpath.endswith(("/.git", "/.hg")):
        return False

    return not bool(filenames or dirnames)  # not empty


def create_parser():
    # TODO: add arg to search version control dirs
    desc = "Search file trees for empty dirs."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("dirs",
                        type=str,
                        nargs="?",
                        metavar="F",
                        default=[os.getcwd()],
                        help="Directories to search recursively.")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    for root in args.dirs:
        for dirpath, dirnames, filenames in os.walk(root):
            if is_empty(dirpath, dirnames, filenames):
                print(f"{dirpath}")
