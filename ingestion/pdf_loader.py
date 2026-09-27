import pymupdf  # PyMuPDF

def extract_text_by_page(pdf_path: str) -> list[dict]:
    """
    Extracts text from a PDF, page by page.

    Returns a list of dicts like:
    [{"page_number": 1, "text": "..."}, {"page_number": 2, "text": "..."}, ...]
    """
    doc = pymupdf.open(pdf_path)
    pages = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text()
        pages.append({
            "page_number": page_index + 1,  # human-readable, 1-indexed
            "text": text
        })

    doc.close()
    return pages