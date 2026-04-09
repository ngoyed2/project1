from openai import OpenAI # necessary for API calls
from dotenv import load_dotenv 
import os # for api key

load_dotenv() # to read .env file into environment

# prompt being directly sent to OpenAI, with placeholder values later to be filled by user input, and schema info
main_prompt = """You are an AI assistant tasked with converting user queries into SQL statements. 
The database uses SQLite and contains the following tables: 

Table: {schema_info}
User Query: "{user_input}" 

Your task is to: 
1. Generate a SQL query that accurately answers the user's 
question. 
2. Ensure the SQL is compatible with SQLite syntax. 
3. Provide a short comment explaining what the query does. 

Output Format: 

- SQL Query: <sql query here>
- Explanation: <brief explanation of query here> """

# function to parse LLM response in desired format
def parse_response(text:str) -> tuple[str, str]:
# tuple will return sql format, and explanation
# values start off blank and are overwritten if proper info is generated
    sql = ""
    explanation = ""

    # loop allows us to check the lines individually, assuring in depth checks
    for line in text.splitlines():
        line = line.strip()

        # looks to find line that'll be returned as sql value, and takes info only after the colon
        if line.lower().startswith("- sql query:"):
            sql = line.split(":",1)[1].strip()

            # strip markdowns as well, and adds semicolon in proper SQL form
            if sql.startswith("```"):
                sql = sql.replace("```sql", "").replace("```","").strip()
            if sql and not sql.endswith(";"):
                sql += ";"
        # looks to find line that'll be returned as explanation, and takes info only after the colon
        elif line.lower().startswith("- explanation:"):
            explanation = line.split(":",1)[1].strip()

    # if sql info not found, will result in error message
    if not sql:
        return  "INVALID", "Cannot extract SQL from response, please try again"
    return sql, explanation

# function to translate user natural language into something understood by SQL 
def translate(user_input:str, schema:str) -> tuple[str,str]:

    # necessary to use OpenAI api
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    client = OpenAI() # actually allows for utilization

    # returns message is no schema was input
    if not schema:
        return "INVALID", "No table input, cannot generate response"
    
    # helps build full prompt using the schema and users input
    prompt = main_prompt.format(
        schema=schema,
        user_input=user_input
    )

    # sends prompt to OpenAI and awaits response, specifies necessary info for command to be made 
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0,
    )

    # indexes into response to get actual content, then strips of whitespace and returns formatted version
    raw = response.choices[0].message.content.strip()
    return parse_response(raw)

