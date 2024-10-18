import sqlite3
import sqlparse
from transformers import T5Tokenizer, T5ForConditionalGeneration, logging

# Path to the local model directory
model_path = "text_to_sql_model/"

# Load the tokenizer and model from the local directory
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Define the get_sql function
def get_sql(query, tokenizer, model):
  input_text = "translate English to SQL: %s" % query
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'],
               attention_mask=features['attention_mask'],
                max_new_tokens=50)

  return tokenizer.decode(output[0], skip_special_tokens=True)

# Define the clean_sql_output function
def clean_sql_output(sql_query):
    # Remove unwanted tokens like '<pad>' and '</s>'
    cleaned_query = sql_query.replace('<pad>', '').replace('</s>', '')

    # Replace the word "table" with "employees"
    cleaned_query = cleaned_query.replace('table', 'employees')

    # Remove any extra leading/trailing whitespace
    cleaned_query = cleaned_query.strip()

    return cleaned_query

def validate_sql(query, db_file='example.db'):
    # Connect to the SQLite database file
    conn = sqlite3.connect(db_file)
    
    try:
        # Try executing the SQL statement
        conn.execute(query)
        return True
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
        return False
    finally:
        conn.close()

def format_sql_query(sql_query):
    # Format SQL query with sqlparse and convert keywords to uppercase
    formatted_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')

    # Replace newlines with spaces to make it one line
    formatted_query = ' '.join(formatted_query.split())
    
    return formatted_query

# Generate SQL Query
query = "What is the salary of the employeed with ID 4?"
sql_query = get_sql(query, tokenizer, model)
cleaned_sql_query = clean_sql_output(sql_query)

# Format SQL Query
formatted_sql_query = format_sql_query(cleaned_sql_query)

print(formatted_sql_query)
print(validate_sql(cleaned_sql_query))