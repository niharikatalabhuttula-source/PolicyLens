from ingestion.pdf_loader import extract_text_by_page
from ingestion.text_cleaner import clean_text
from core.summarizer import summarize_document
from core.document_info import extract_scheme_info

pages = extract_text_by_page("data/uploads/sample.pdf")
for page in pages:
    page["text"] = clean_text(page["text"])

full_text = "\n\n".join(page["text"] for page in pages)

print("=== SUMMARY ===")
print(summarize_document(full_text))

print("\n=== STRUCTURED INFO ===")
info = extract_scheme_info(full_text)
for key, value in info.items():
    print(f"\n{key.upper()}:")
    print(value)