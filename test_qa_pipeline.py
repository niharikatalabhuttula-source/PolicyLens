from core.qa_pipeline import answer_question

questions = [
    "What is the income limit for eligibility?",
    "What is the application fee?",
    "Who is eligible for this scheme?",
]

for q in questions:
    result = answer_question(q)
    print(f"\nQ: {q}")
    print(f"A: {result['answer']}")
    print(f"Source pages: {result['pages']}")
    print(f"No-answer detected: {result['no_answer_found']}")
    print(f"Numeric grounding: {result['numeric_grounding']}")
    print("-" * 60)