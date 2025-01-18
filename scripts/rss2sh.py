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
import argparse

import feedparser

# TODO: add funcs to generate different types of download scripts
#       wget, requests, yt-dlp???

MEDIA_TYPES = ("audio/mpeg", )


def extract_url(e):
    """
    Extracts URL from RSS entry data.
    """
    # ".links" is usually a pair of dicts, one with correct media type & a URL
    for item in e.links:
        raw_url = item.href
        media_type = item.type

        if media_type not in MEDIA_TYPES:
            msg = "Warning: media type '{media type}' not in {MEDIA_TYPES}"
            warnings.warn(msg)

        # TODO: possibly add better error handling
        if ".mp3" in raw_url:
            break
        else:
            msg = f"Warning: no '.mp3' in media URL not in {raw_url}"
            warnings.warn(msg)

    return raw_url


def clean_url(raw_url):
    url = raw_url.partition("?")[0]  # trim tracking args
    return url


def format_entry(e, url):
    """
    Returns a formatted 'wget' download command string.
    """
    timestamp = get_timestamp(e)
    return f"wget {url} -O '{timestamp}-{e.title}.mp3'"


def get_timestamp(entry):
    d = datetime.datetime(*entry.published_parsed[:7])
    return d.strftime("%Y%m%d-%H%M")


def parse_command_line():
    # TODO: add custom user agent option
    # TODO: add numerical limit option (e.g. top N feed entries)
    desc = """%(prog)s downloads &converts RSS feeds to wget download scripts."""

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-k", "--keep-url-query",
                        default=False,
                        action="store_true",
                        help="Retain query in any RSS entry URL.")

    parser.add_argument("-v", "--verbose",
                        default=False,
                        action="store_true",
                        help="Display runtime information.")

    parser.add_argument("url", help="Feed URL to download & convert.")
    return parser.parse_args()


def main():
    args = parse_command_line()
    feed = feedparser.parse(args.url)

    for ent in feed.entries:
        raw_url = extract_url(ent)
        url = raw_url if args.keep_url_query else clean_url(raw_url)
        print(format_entry(ent, url))


if __name__ == "__main__":
    main()
