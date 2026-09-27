from ai.gemini_client import generate_with_retry

SUMMARY_PROMPT_TEMPLATE = """You are summarizing an official government scheme/policy document.

Write a clear, concise summary (150-250 words) covering:
- What the scheme is
- Who it is for
- The main benefit(s)
- Any major conditions or exclusions worth knowing upfront

Use plain language a non-expert can understand. Do not invent details not present \
in the document below.

DOCUMENT TEXT:
{document_text}

SUMMARY:"""

def summarize_document(full_text: str) -> str:
    prompt = SUMMARY_PROMPT_TEMPLATE.format(document_text=full_text)
    return generate_with_retry(prompt)