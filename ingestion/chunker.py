def chunk_pages(pages: list[dict], chunk_size: int = 150, overlap: int = 20) -> list[dict]:
    """
    Splits cleaned page text into overlapping chunks, aligned to word boundaries.

    chunk_size and overlap are now measured in WORDS, not characters.

    Input: [{"page_number": 1, "text": "..."}, ...]
    Output: [{"chunk_id": 0, "page_number": 1, "text": "..."}, ...]
    """
    chunks = []
    chunk_id = 0

    for page in pages:
        words = page["text"].split()  # splits on whitespace, no partial words
        page_number = page["page_number"]

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words).strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page_number": page_number,
                    "text": chunk_text
                })
                chunk_id += 1

            start += chunk_size - overlap

    return chunks