"""
The `rss2sh` utility downloads RSS (e.g. podcasts) & formats each entry into a
download script command. Each item is given the timestamp & RSS title in place
of the default filename (possibly a random letter/number jumble).

Only 'wget' is supported at present.

Usage:
$ rss2sh.py  https://some.url.com/listing.rss
"""

import sys
import datetime
import warnings

import feedparser

# TODO: add funcs to generate different types of download scripts
#       wget, requests, yt-dlp???

MEDIA_TYPES = ("audio/mpeg", )


def format_entry(e):
    """
    Extracts entry data, formats & returns a wget download command.
    """
    timestamp = get_timestamp(e)

    for item in e.links:
        raw_url = item.href
        media_type = item.type

        if media_type not in MEDIA_TYPES:
            msg = "Warning: media type '{media type}' not in {MEDIA_TYPES}"
            warnings.warn(msg)

        if ".mp3" in raw_url:
            break
        else:
            msg = f"Warning: no '.mp3' in media URL not in {raw_url}"
            warnings.warn(msg)

    # TODO: possibly add better error handling
    url = raw_url.partition("?")[0]  # trim tracking args
    return f"wget {url} -O '{timestamp}-{e.title}.mp3'"


def get_timestamp(entry):
    d = datetime.datetime(*entry.published_parsed[:7])
    return d.strftime("%Y%m%d-%H%M")


if __name__ == "__main__":
    # TODO: assume only 1 URL required
    url = sys.argv[1]
    feed = feedparser.parse(url)

    for ent in feed.entries:
        print(format_entry(ent))
