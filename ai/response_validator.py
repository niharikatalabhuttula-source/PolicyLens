import re

NOT_FOUND_PHRASES = [
    "could not be found",
    "couldn't find",
    "not mentioned",
    "does not contain",
    "no information",
]

def is_no_answer_response(answer: str) -> bool:
    """
    Detects if the answer is a 'information not found' type response.
    """
    lower = answer.lower()
    return any(phrase in lower for phrase in NOT_FOUND_PHRASES)


import re

def extract_numbers(text: str) -> set[str]:
    """
    Extracts number-like tokens (amounts, dates, percentages) from text,
    while ignoring markdown list markers like '1.' '2.' '3.'
    """
    # Remove markdown list markers at the start of lines (e.g. "1. ", "2. ")
    text = re.sub(r'(?m)^\s*\d+\.\s+', '', text)

    # Find number-like tokens, then strip trailing punctuation from each
    raw_matches = re.findall(r"\d[\d,\.]*\d|\d", text)
    cleaned = {match.rstrip('.,') for match in raw_matches}

    return cleaned


def check_numeric_grounding(answer: str, context_chunks: list[str]) -> dict:
    """
    Checks whether numbers mentioned in the answer actually appear
    somewhere in the retrieved context. This is a simple sanity check,
    not a perfect guarantee — but it catches obvious invented figures.
    """
    context_text = " ".join(context_chunks)
    context_numbers = extract_numbers(context_text)
    answer_numbers = extract_numbers(answer)

    ungrounded = answer_numbers - context_numbers

    return {
        "all_numbers_grounded": len(ungrounded) == 0,
        "ungrounded_numbers": ungrounded
    }