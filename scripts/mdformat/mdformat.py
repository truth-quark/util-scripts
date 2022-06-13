"""
Quick and dirty script to reformat markdown files from 'Docs to Markdown' extension in Google docs.
"""

import re
import sys
from pathlib import Path
from enum import Enum
from more_itertools import peekable


class LineType(Enum):
    DATA = "data"
    DATE = "date"
    BLANK = "blank"
    TEXT = "text"
    HEADER = "header"


RE_DATE_PATTERN = r"\d{1,2}/\d{1,2}/\d{4}"
date_regex = re.compile(RE_DATE_PATTERN)

RE_HEADER_PATTERN = r"#{1,4} "
header_regex = re.compile(RE_HEADER_PATTERN)


def _classify_line(line: str):
    if line == '' or line.isspace():
        return LineType.BLANK
    elif date_regex.match(line):
        return LineType.DATE
    elif header_regex.match(line):
        return LineType.HEADER
    elif line.startswith("* ") or line == "*" or line == "*\n":
        # dot point content in the document
        return LineType.DATA

    return LineType.TEXT


def format_markdown(lines):
    lookahead = peekable(lines)
    current = next(lookahead).rstrip()
    current_type = _classify_line(current)
    last_line_type = None
    line_dropped = False

    assert current_type in (LineType.TEXT, LineType.HEADER)
    yield current

    while lookahead:
        if not line_dropped:
            last_line_type = current_type
        else:
            # retain last line data as last processed line was dropped
            line_dropped = False

        current = next(lookahead).rstrip()  # preserve indent with rstrip
        current_type = _classify_line(current)
        peeked_type = _classify_line(lookahead.peek()) if lookahead else None

        if current_type is LineType.BLANK and last_line_type is LineType.DATA and peeked_type is LineType.DATA:
            # drop blank line between dot points
            line_dropped = True
            continue
        elif current_type is LineType.BLANK and peeked_type is LineType.BLANK:
            # drop duplicate newlines (simplify document in addition to newline removal in markdown render)
            line_dropped = True
            continue
        elif peeked_type is None:
            yield f"{current}\n"  # final inline newline avoids join() adding extra "\n"
        else:
            yield current


if __name__ == "__main__":
    usage = "mdformat.py [input_file]\nOR\nmdformat.py [input_file] > <output_file>  # redirect to file"

    try:
        path = Path(sys.argv[1])
    except IndexError:
        raise SystemExit(usage)

    if not path.exists():
        raise SystemExit(f"File: {path} does not exist")

    with open(path) as f:
        for _line in format_markdown(f):
            print(_line)
