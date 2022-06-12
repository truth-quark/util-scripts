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


RE_DATE_PATTERN = r"\d{1,2}/\d{1,2}/\d{4}"
regex = re.compile(RE_DATE_PATTERN)


# TODO: does not handle leading hashes for heading lines
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
    current = next(lookahead).rstrip()
    current_type = _classify_line(current)

    assert current_type == LineType.TEXT
    yield current

    while lookahead:
        last_line_type = current_type
        current = next(lookahead).rstrip()  # using rstrip preserves indent
        current_type = _classify_line(current)

        if lookahead:
            peeked = lookahead.peek()
            peeked_type = _classify_line(peeked)
        else:
            # flag being the last line
            peeked = peeked_type = None

        if current_type == LineType.BLANK and last_line_type == LineType.DATA and peeked_type == LineType.DATA:
            # remove blank line between dot points
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
