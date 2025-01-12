import sys
import datetime
import feedparser

# TODO: add funcs to generate different types of download scripts
#       wget, requests, yt-dlp???

url = sys.argv[1]
feed = feedparser.parse(url)
entries = feed.entries


# TODO: refactor, only extract data with this func
def entry(e):
    d = datetime.datetime(*e.published_parsed[:7])

    url = None
    try:
        url = e.links[0].href
    except AttributeError as ex:
        pass

    if url is None:
        url = e.media_content[0]["url"].partition("?")[0]

    # return f"wget {url} -O '{d.year}{d.month}{d.day}-{e.title}.mp3'"
    return f"wget {url} -O '{d.year}{str(d.month).zfill(2)}{str(d.day).zfill(2)}-{e.title}.mp3'"


for ent in entries:
    print(entry(ent))
