import json
from ai.gemini_client import generate_with_retry

EXTRACTION_PROMPT_TEMPLATE = """Extract the following structured information from this \
government scheme/policy document. Respond with ONLY a valid JSON object, no other \
text, no markdown formatting, no code fences.

Use this exact structure:
{{
  "scheme_name": "...",
  "eligibility": "...",
  "benefits": "...",
  "required_documents": "...",
  "application_process": "...",
  "important_conditions": "..."
}}

If any field is not mentioned in the document, use the string "Not specified in the document" \
for that field. Do not invent information.

DOCUMENT TEXT:
{document_text}

JSON OUTPUT:"""

def extract_scheme_info(full_text: str) -> dict:
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(document_text=full_text)
    raw_response = generate_with_retry(prompt)

    # Gemini sometimes wraps JSON in markdown code fences despite instructions —
    # strip those defensively before parsing
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "error": "Could not parse structured information from the document.",
            "raw_response": raw_response
        }