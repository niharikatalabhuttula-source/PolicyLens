import re

def clean_text(text: str) -> str:
    """
    Cleans raw extracted PDF text:
    - Strips trailing/leading whitespace per line
    - Collapses multiple blank lines into one
    - Collapses multiple spaces into one
    """
    # Strip whitespace from each line FIRST, so space-only lines become empty
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Now collapse 3+ real newlines (i.e. 2+ blank lines) into just one blank line
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Collapse repeated spaces/tabs within lines
    text = re.sub(r'[ \t]{2,}', ' ', text)

    return text.strip()