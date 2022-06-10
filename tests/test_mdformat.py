from io import StringIO
from scripts.mdformat import mdformat


MD_PRE_FORMAT_CONTENT = """Notes 2022

30/5/2022

* Notes line 1

* Notes line 2

* Notes line 3

31/5/2022

* Notes line 1

* Notes line 2

* Notes line 3

1/6/2022

* Notes line 1

* Notes line 2

* Notes line 3
"""


MD_POST_FORMAT_CONTENT = """Notes 2022

30/5/2022

* Notes line 1
* Notes line 2
* Notes line 3

31/5/2022

* Notes line 1
* Notes line 2
* Notes line 3

1/6/2022

* Notes line 1
* Notes line 2
* Notes line 3
"""


MD_HEADER_PRE_FORMAT_CONTENT = """**Notes 2022**

30/5/2022

* Notes line 1

* Notes line 2

* 

*

Here is some general text content where the next blank should be preserved.

More text.
    Indented content.
"""


MD_HEADER_POST_FORMAT_CONTENT = """**Notes 2022**

30/5/2022

* Notes line 1
* Notes line 2
*
*

Here is some general text content where the next blank should be preserved.

More text.
    Indented content.
"""


def test_md_formatter_no_header():
    # ensure formatter only removes blank lines between the dot points
    assert MD_POST_FORMAT_CONTENT.endswith("\n")

    content = StringIO(MD_PRE_FORMAT_CONTENT)
    raw_result = list(mdformat.format_markdown(content))
    result = "\n".join(raw_result)

    assert result.endswith('\n')
    assert result == MD_POST_FORMAT_CONTENT


def test_md_formatter_bold_header():
    # ensure formatter handles bold or italicised lines, and empty dot points
    assert MD_HEADER_POST_FORMAT_CONTENT.endswith("\n")

    content = StringIO(MD_HEADER_PRE_FORMAT_CONTENT)
    raw_result = list(mdformat.format_markdown(content))
    result = "\n".join(raw_result)

    assert result.endswith('\n')
    assert result == MD_HEADER_POST_FORMAT_CONTENT
