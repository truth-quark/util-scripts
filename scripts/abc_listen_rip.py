import os
import re
import sys
import requests

urls = sys.argv[1:]
pattern = r"https://mediacore-live-production.akamaized.net/audio/../../Z/..[.]mp3"
title_pattern = r"<title>(?P<title>.+)</title>"

for url in urls:
    r = requests.get(url)

    if r.status_code != 200:
        msg = f"HTTP {r.status_code} for {url}"
        print(msg)
        continue

    if match_title := re.search(title_pattern, r.text):
        raw_title = match_title.group(1)
        title, _, _ = raw_title.partition(" - ")
        print(f"title={title}")
    else:
        print(f"No title found in HTML, skipping {url}")
        continue

    if match := re.search(pattern, r.text):
        #print(match)
        m_url = match.group()
        print(f"url={m_url}")

    cmd = f"""wget {m_url} -O "{title}.mp3" """
    # print(f"dl cmd: {cmd}")
    os.system(cmd)
