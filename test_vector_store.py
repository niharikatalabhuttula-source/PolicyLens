from ingestion.pdf_loader import extract_text_by_page
from ingestion.text_cleaner import clean_text
from ingestion.chunker import chunk_pages
from retrieval.vector_store import add_chunks, query_chunks

# Build and store chunks (only need to do this once per document)
pages = extract_text_by_page("data/uploads/sample.pdf")
for page in pages:
    page["text"] = clean_text(page["text"])
chunks = chunk_pages(pages)

print(f"Embedding and storing {len(chunks)} chunks... this may take a moment.")
add_chunks(chunks)
print("Done storing chunks.")

# Now test retrieval with a real question
results = query_chunks("What is the income limit for eligibility?")

print("\n--- Top matching chunks ---")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"\n[Page {meta['page_number']}]")
    print(doc[:300])