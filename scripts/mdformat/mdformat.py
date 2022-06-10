"""
Quick and dirty script to reformat markdown files from "Docs to Markdown" extension in Google docs.
"""

import re
import sys
from enum import Enum
from more_itertools import peekable


class LineType(Enum):
    DATA = "data"
    DATE = "date"
    BLANK = "blank"
    TEXT = "text"


RE_DATE_PATTERN = r"\d{1,2}/\d{1,2}/\d{4}"
regex = re.compile(RE_DATE_PATTERN)


def _classify_line(line: str):
    if line == '' or line.isspace():
        return LineType.BLANK
    elif regex.match(line):
        return LineType.DATE
    elif line.startswith("* ") or line == "*" or line == "*\n":
        # dot point content in the document
        return LineType.DATA

    return LineType.TEXT


def format_markdown(lines):
    lookahead = peekable(lines)
    current = next(lookahead)
    current_type = _classify_line(current)

    assert current_type == LineType.TEXT
    yield current

    while lookahead:
        last_line_type = current_type
        current = next(lookahead).rstrip()  # rstrip to preserve indent
        current_type = _classify_line(current)

        if lookahead:
            peeked = lookahead.peek()
            peeked_type = _classify_line(peeked)
        else:
            # Handle last line
            peeked_type = None

        if current_type == LineType.BLANK and last_line_type == LineType.DATE and peeked_type == LineType.DATA:
            # retain blank line between the date/title & first dot point
            yield current
        elif current_type == LineType.BLANK and last_line_type == LineType.DATA and peeked_type == LineType.DATA:
            # remove blank line between dot points
            continue
        elif current_type == LineType.BLANK and last_line_type == LineType.DATA and peeked_type == LineType.DATE:
            # retain blank line between last dot point and new title entries
            yield current
        elif current_type == LineType.BLANK and peeked_type == LineType.BLANK:
            # maintain multiple line breaks
            yield current
        elif current_type == LineType.BLANK and peeked_type == LineType.TEXT:
            # maintain multiple line breaks
            yield current
        elif peeked_type and current_type in (LineType.DATA, LineType.DATE, LineType.TEXT):
            yield current
        elif peeked_type is None:
            yield f"{current}\n"  # final newline needs to be inline to avoid join() adding extra "\n"


if __name__ == "__main__":
    path = sys.argv[1]

    with open(path) as f:
        for _line in format_markdown(f):
            print(_line)
