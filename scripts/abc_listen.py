import os
import re
import sys
import html
import warnings
import subprocess
import requests

# TODO: use argparse?
# TODO: should HTML be saved?
# TODO: add option to create wget script?

# Media file patterns can be:
# https://abcmedia.akamaized.net/something/some_podcast/name-2021-10-4-descriptor.mp3
# https://abcmedia.akamaized.net/rn/podcast/2022/02/eot_20220207.mp3
patterns = [r"https://mediacore-live-production.akamaized.net/audio/../../Z/..[.]mp3",
            r"http[s]{0,1}://abcmedia.akamaized.net/[\S]+[.]mp3"]

title_pattern = r"<title>(?P<title>.+)</title>"


USER_AGENT_KEY = "USER_AGENT"
USER_AGENT = os.environ.get(USER_AGENT_KEY)


def extract_media_path(re_patterns, text):
    for pattern in re_patterns:
        if match := re.search(pattern, text):
            return match.group()


# FIXME: clean up escaping & quote chars from title
def clean_title(title):
    raw_title = html.unescape(title)

    for c in ("'", '"', "?"):
        raw_title = raw_title.replace(c, "")

    return raw_title


def main():
    urls = sys.argv[1:]
    headers = {'user-agent': USER_AGENT} if USER_AGENT else None

    for url in urls:
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            msg = f"HTTP {r.status_code} for {url}"
            warnings.warn(msg)
            continue

        if match_title := re.search(title_pattern, r.text):
            raw_title = match_title.group(1)
            title, _, _ = raw_title.partition(" - ")
            title = clean_title(title)
        else:
            warnings.warn(f"No title found in HTML, skipping {url}")
            continue

        # download step
        if media_path := extract_media_path(patterns, r.text):
            cmd = ["wget", media_path, "-O", f"\"{title}.mp3\""]

            # temporarily use env var until argparse is implemented
            if USER_AGENT:
                cmd.extend(["-U", USER_AGENT])

            subprocess.run(cmd)
        else:
            warnings.warn(f"No media URL found in {url}")
            continue


if __name__ == "__main__":
    main()
