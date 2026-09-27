from retrieval.vector_store import query_chunks
from ai.prompts import build_prompt
from ai.response_validator import is_no_answer_response, check_numeric_grounding
from ai.gemini_client import generate_with_retry

def answer_question(question: str, n_results: int = 4) -> dict:
    results = query_chunks(question, n_results=n_results)

    context_chunks = results["documents"][0]
    pages_used = [meta["page_number"] for meta in results["metadatas"][0]]

    prompt = build_prompt(question, context_chunks)
    answer_text = generate_with_retry(prompt)

    no_answer = is_no_answer_response(answer_text)
    grounding = check_numeric_grounding(answer_text, context_chunks)

    return {
        "answer": answer_text,
        "pages": sorted(set(pages_used)),
        "no_answer_found": no_answer,
        "numeric_grounding": grounding
    }