import re
import sys
import subprocess
import requests

# TODO: use argparse?
# TODO: should the HTML be saved & cached? Does a lib exist for this?
# TODO: add option to create wget script?

# Media file patterns can be:
# https://abcmedia.akamaized.net/something/some_podcast/name-2021-10-4-descriptor.mp3
# https://abcmedia.akamaized.net/rn/podcast/2022/02/eot_20220207.mp3
patterns = [r"https://mediacore-live-production.akamaized.net/audio/../../Z/..[.]mp3",
            r"http[s]{0,1}://abcmedia.akamaized.net/[\S]+[.]mp3"]

title_pattern = r"<title>(?P<title>.+)</title>"


def extract_media_path(re_patterns, text):
    for pattern in re_patterns:
        if match := re.search(pattern, text):
            return match.group()


def main():
    urls = sys.argv[1:]

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

        # download step
        if media_path := extract_media_path(patterns, r.text):
            cmd = ["wget", media_path, "-O", f"{title}.mp3"]
            subprocess.run(cmd)
        else:
            print(f"No media URL found in {url}")
            continue


if __name__ == "__main__":
    main()
