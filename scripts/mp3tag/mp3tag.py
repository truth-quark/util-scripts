import os
import sys
import glob
import pathlib


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
        raise mp3tag_error(f"No files found in {dir_path}")

    for path in file_paths:
        track, title = parse_file_path(path)
        tag_file(path, track, title, album=dir_path.stem, artist=artist)


def parse_file_path(path: pathlib.Path):
    assert path.is_file()
    base = path.stem
    track = int(base[:2])
    title = base[3:]
    return track, title


def tag_file(path: pathlib.Path, track: int, title: str, album: str, artist: str):
    cmd = f"id3tool -c {track} -t '{title}' -a '{album}' -r '{artist}' '{path}'"
    os.system(cmd)


class mp3tag_error(Exception):
    pass


if __name__ == "__main__":
    usage = "mp3tag [artist name] [album_dir]"
    _artist, _dir = sys.argv[1:]
    tag_files(pathlib.Path(_dir), _artist)
