import os
import re
import sys
import glob
import pathlib


# TODO: check for installed id3 tag utils?

NUMBERED_ALBUM_PATTERN = r"^[0-9]{2} "
pattern = re.compile(NUMBERED_ALBUM_PATTERN)

DEBUG = "DEBUG" in os.environ


def tag_files(dir_path: pathlib.Path, artist: str):
    """
    Search for mp3 files to automatically tag.

    :param dir_path: directory path to search for MP3 files - is also the album title
    :param artist: band name
    :return:
    """
    search_str = f"{dir_path}/*.mp3"
    file_paths = [pathlib.Path(p) for p in glob.glob(search_str)]

    if len(file_paths) == 0:
        raise TagError(f"No files found in {dir_path}")

    album = dir_path.name

    if DEBUG:
        print(f"Album title {album}")

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
    track = int(base[:2])  # TODO: make more robust with regex
    title = base[3:]

    if title.startswith("- "):
        title = title[2:]

    return track, title.strip()


def tag_file(path: pathlib.Path, track: int, title: str, album: str, artist: str):
    cmd = f"""id3tool -c {track} -t "{title}" -a '{album}' -r '{artist}' "{path}" """

    if DEBUG:
        print(cmd)

    # TODO: replace with popen
    os.system(cmd)


class TagError(Exception):
    pass


if __name__ == "__main__":
    usage = "mp3tag [artist name] [album_dir(s)]"
    _artist = sys.argv[1]
    _dirs = sys.argv[2:]

    for d in _dirs:
        tag_files(pathlib.Path(d), _artist)
