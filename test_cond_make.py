import re
import sys
import pytest

filename = "cond_make"


def test_header_comments():
    """Students should have a docstring with author, date, and description"""
    with open(f"{filename}.py", encoding="utf-8") as f:
        kids_code = f.read()

    # Check that a module-level docstring exists
    docstring_match = re.search(r'^\s*"""(.*?)"""', kids_code, re.DOTALL)
    assert docstring_match is not None, "You must include a header docstring using triple quotes (\"\"\")"

    docstring = docstring_match.group(1)

    # Check for author field with a non-empty value
    author_match = re.search(r'author\s*:\s*(.+)', docstring, re.IGNORECASE)
    assert author_match is not None, "Your header must include an 'author:' field"
    assert author_match.group(1).strip() != "", "Your 'author:' field must not be empty"

    # Check for date field with a non-empty value
    date_match = re.search(r'date\s*:\s*(.+)', docstring, re.IGNORECASE)
    assert date_match is not None, "Your header must include a 'date:' field"
    assert date_match.group(1).strip() != "", "Your 'date:' field must not be empty"

    # Check that there's at least one line that isn't just author/date (a description)
    lines = [line.strip() for line in docstring.strip().splitlines()]
    description_lines = [
        line for line in lines
        if line
        and not re.match(r'author\s*:', line, re.IGNORECASE)
        and not re.match(r'date\s*:', line, re.IGNORECASE)
    ]
    assert len(description_lines) >= 1, "Your header must include a short description of the program"


def test_ipo_comments():
    """Students should have # Input, # Processing, and # Output comments"""
    with open(f"{filename}.py", encoding="utf-8") as f:
        kids_code = f.read()

    assert re.search(r'#.*input', kids_code, re.IGNORECASE), "You must include an '# Input' comment section"
    assert re.search(r'#.*processing|#.*output', kids_code, re.IGNORECASE), "You must include a '# Processing' and/or '# Output' comment section"


def test_levels(capsys, monkeypatch):
    """Test all the numbers from 1 to 100"""
    for i in range(1, 101):
        monkeypatch.setattr("builtins.input", lambda _: i)
        __import__(filename)
        captured = capsys.readouterr()

        if i < 50:
            expected_answer = "level 0"
        elif i < 60:
            expected_answer = "level 1"
        elif i < 70:
            expected_answer = "level 2"
        elif i < 80:
            expected_answer = "level 3"
        else:
            expected_answer = "level 4"

        assert expected_answer in captured.out.lower(), f"You got the level for {i} wrong, should have been {expected_answer}"
        del sys.modules[filename]