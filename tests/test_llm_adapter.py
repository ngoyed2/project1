import pytest
from src.llm_adapter import translate, parse_response
from unittest.mock import patch, MagicMock
import os
os.environ["OPENAI_API_KEY"] = "test-fake-key"
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

# helps imitate the reponse that OpenAI would give
def mock_openai_helper(text:str):
       return MagicMock(
          choices = [
             MagicMock(
                message = MagicMock(content=text)
             )
          ]
       )
class TestTranslator:
    
    # tests that it functions properly
    def test_returns_sql_and_explanation(self):
        schema = "sales(id INTEGER, name TEXT, amount REAL, region TEXT)"
        fake_reply = "- SQL Query: SELECT * FROM sales;\n- Explanation: Returns all sales."
        with patch("llm_adapter.OpenAI") as mock_openai_class:
            # mock the instance that OpenAI() returns
            mock_instance = MagicMock()
            mock_openai_class.return_value = mock_instance
            mock_instance.chat.completions.create.return_value = mock_openai_helper(fake_reply)
            
            output = translate("show me all sales", schema)
        
        assert output["sql"] == "SELECT * FROM sales;"
        assert "sales" in output["explanation"].lower()

    # tests that an empty input will be handled
    def test_handles_empty_responses(self):
        schema = "sales(id INTEGER, name TEXT, amount REAL, region TEXT)"
        fake_reply = ""
        with patch("llm_adapter.OpenAI") as mock_openai_class:
            # mock the instance that OpenAI() returns
            mock_instance = MagicMock()
            mock_openai_class.return_value = mock_instance
            mock_instance.chat.completions.create.return_value = mock_openai_helper(fake_reply)
            output = translate("show me all sales", schema)
        
        assert output == "INVALID, Cannot extract SQL from response, please try again"

    

    

    
