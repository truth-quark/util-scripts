import os
import re
import sys
import glob
import pathlib
import subprocess
import warnings
import argparse

# TODO: add option for title only/title+artist when no track # exists
# TODO: strip common head/tail of title strings? (e.g. get rid of leading artist name)
#       e.g. "Tool - H." --> "H."

# check for installed id3 tag utils
# TODO: replace with a python dep?
MP3_UTILS = ("id3tool", )
_results = [subprocess.run(["which", util]) for util in MP3_UTILS]
_installed = [proc for proc in _results if proc.returncode == 0]

if not _installed:
    msg = f"No id3 tagging tools installed: {', '.join(MP3_UTILS)}"
    raise SystemExit(msg)


NUMBERED_ALBUM_PATTERN = r"^[0-9]{2} "
pattern = re.compile(NUMBERED_ALBUM_PATTERN)

TRACK_NUMBERING_PATTERN = r"^[0-9]{1,3}"
track_pattern = re.compile(TRACK_NUMBERING_PATTERN)

ARTIST_NAME = "artist-name"
FILES_OR_DIRS = "files-or-dirs"
DEBUG = "DEBUG" in os.environ


def tag_files(dir_path: pathlib.Path, artist: str):
    """
    Search for mp3 files to automatically tag.

    :param dir_path: directory path to search for MP3 files - is also the album title
    :param artist: band name
    :return:
    """
    # TODO: expand searches to include all media supporting id3 tags
    search_str = f"{dir_path}/*.mp3"
    file_paths = [pathlib.Path(p) for p in glob.glob(search_str)]

    if len(file_paths) == 0:
        raise TagError(f"No files found in {dir_path}")

    album = dir_path.name

    if DEBUG:
        print(f"DEBUG: Album title '{album}'")

    m = pattern.match(album)

    if m:
        # strip off album numbering prefix
        album = album[3:]

    for path in file_paths:
        track, title = parse_file_path(path)
        tag_file(path, track, title, album, artist)


def parse_file_path(path: pathlib.Path):
    assert path.is_file()
    base = path.stem

    m = track_pattern.match(base)

    if m:
        track = int(m[0])
        track_len = len(m[0])
    else:
        warnings.warn(f"No track number found for '{base}'")
        return base  # TODO: does this work?

    title = base[track_len+1:]

    if title.startswith("- "):
        title = title[2:]

    return track, title.strip()


def tag_file(path: pathlib.Path, track: int, title: str, album: str, artist: str):
    cmd = f"""id3tool -c {track} -t "{title}" -a '{album}' -r '{artist}' "{path}" """

    if DEBUG:
        print("DEBUG:", cmd)

    res = subprocess.run(cmd, shell=True)

    if res.returncode:
        err = f"Failed to exec: {cmd}"
        print(err)


def tag_title_only(path: pathlib.Path, title: str, album: str, artist: str):
    # TODO: check/strip leading numbering from files for title
    cmd = f"""id3tool -t "{title}" -r '{artist}' "{path}" """
    res = subprocess.run(cmd, shell=True)

    if DEBUG:
        print("DEBUG:", cmd)

    if res.returncode:
        err = f"Failed to exec: {cmd}"
        print(err)


class TagError(Exception):
    pass


if __name__ == "__main__":
    # usage = "mp3tag [artist name] [file(s) or album_dir(s)]"
    parser = argparse.ArgumentParser(description="Update tags for batches of MP3 files")
    parser.add_argument(ARTIST_NAME, help="Artist/band name")
    parser.add_argument(FILES_OR_DIRS,
                        type=str,
                        nargs="+",
                        metavar="F",
                        help="Files or directories of files to tag")

    raw_args = parser.parse_args()
    args = vars(raw_args)

    for d in args[FILES_OR_DIRS]:
        if os.path.isdir(d):
            tag_files(pathlib.Path(d), args[ARTIST_NAME])
        else:
            tag_title_only(pathlib.Path(d),
                           os.path.basename(d),
                           "-",  # no album
                           args[ARTIST_NAME])
