import pytest
from llm_adapter import translate, parse_response

class TestParser:

    # tests that parser can handle basic response given proper return
    def test_basic_correct_response(self):
        response = """- SQL Query: SELECT * from table 
        - Explanation: we are selecting this"""
        output = parse_response(response) # make sure these statements are unique to each test, bc they share attributes
        assert output["sql"] == "SELECT * from table;"
        assert output["explanation"] == "we are selecting this"
    
    # tests that parser handles the final output for query and explanation
    def test_multiple_outputs(self):
        response = """- SQL Query: SELECT * from table 
        - Explanation: explained 1 
        - SQL Query:SELECT * from table2 
        - Explanation: something else2"""
        output = parse_response(response)
        assert output["sql"] == "SELECT * from table2;"
        assert output["explanation"] == "something else2"

    # test that with semicolon, parser correcly accepts response as proper SQL
    def test_response_has_semicolon(self):
       response = """- SQL Query: SELECT * from table 
        - Explanation: explained 1 """
       output = parse_response(response)
       assert output["sql"] == "SELECT * from table;"
       assert output["explanation"] == "explained 1"
    
    # tests for missing returned values
    def test_missing_explanation(self):
       response = """- SQL Query: SELECT * from table """ 
       output = parse_response(response)
       assert output == "INVALID, Cannot extract SQL from response, please try again"

    def test_missing_sql(self):
       response = """- Explanation: explained 1 """ 
       output = parse_response(response)
       assert output == "INVALID, Cannot extract SQL from response, please try again"

    def test_empty_return(self):
       response = """""" 
       output = parse_response(response)
       assert output == "INVALID, Cannot extract SQL from response, please try again"
    
    def test_invalid_input(self):
       response = "this is unrelated text with no structured input, explanation is this and sql query is that"
       output = parse_response(response)
       assert output == "INVALID, Cannot extract SQL from response, please try again"
    
    
