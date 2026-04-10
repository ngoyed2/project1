from src.llm_adapter import parse_response

passing_response = """
- SQL Query:SELECT * FROM sales WHERE amount > 1000;
- Explanation:Returns all sales where amount exceeds 1000.
"""
sql, explanation = parse_response(passing_response)
print(sql)          # SELECT * FROM sales WHERE amount > 1000;
print(explanation)  # Returns all sales where amount exceeds 1000.

# Simulate a bad LLM response
failing_response = "I'm sorry, I don't understand the question."
sql, explanation = parse_response(failing_response)
print(sql)          # INVALID
print(explanation)  # Cannot extract SQL from response...
