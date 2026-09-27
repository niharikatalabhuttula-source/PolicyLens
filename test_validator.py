from ai.response_validator import extract_numbers, check_numeric_grounding

answer = """1. Institutional Land holders.
2. Farmer families...
3. NRIs under the Income Tax Act, 1961, cannot be uploaded."""

context = ["... Income Tax Act, 1961 ... transfer between 01.12.2018 and 31.01.2019 ..."]

print("Extracted from answer:", extract_numbers(answer))
print("Grounding check:", check_numeric_grounding(answer, context))