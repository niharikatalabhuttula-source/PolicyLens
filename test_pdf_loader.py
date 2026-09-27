from ingestion.pdf_loader import extract_text_by_page
from ingestion.text_cleaner import clean_text
from ingestion.pdf_loader import extract_text_by_page
from ingestion.text_cleaner import clean_text
from ingestion.chunker import chunk_pages


pages = extract_text_by_page("data/uploads/sample.pdf")

# Clean each page's text
for page in pages:
    page["text"] = clean_text(page["text"])

chunks = chunk_pages(pages)


print(f"Total pages extracted: {len(pages)}")
print("--- First page preview (cleaned) ---")
print(pages[0]["text"][:500])
print(f"Total chunks created: {len(chunks)}")
print("--- Sample chunk (index 5) ---")
print(f"Page: {chunks[5]['page_number']}")
print(f"Text: {chunks[5]['text']}")