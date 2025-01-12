import sys
import datetime
import feedparser

# TODO: add funcs to generate different types of download scripts
#       wget, requests, yt-dlp???


# TODO: refactor, only extract data with this func
def entry(e):
    timestamp = get_timestamp(e)

    url = None
    try:
        url = e.links[0].href
    except AttributeError as ex:
        pass

    if url is None:
        url = e.media_content[0]["url"].partition("?")[0]

    return f"wget {url} -O '{timestamp}-{e.title}.mp3'"


def get_timestamp(entry):
    d = datetime.datetime(*entry.published_parsed[:7])
    year = d.year

    # add leading zeros as numerical f string formatting doesn't allow this
    month = str(d.month).zfill(2)
    day = str(d.day).zfill(2)
    hour = str(d.hour).zfill(2)
    minute = str(d.minute).zfill(2)

    return f"{year}{month}{day}-{hour}{minute}"


if __name__ == "__main__":
    # TODO: assume only 1 URL required
    url = sys.argv[1]
    feed = feedparser.parse(url)
    entries = feed.entries

    for ent in entries:
        print(entry(ent))
