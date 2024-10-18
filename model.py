
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the tokenizer and model from the local directory
# model_path = "text_to_sql_model/"
model_path = "/app/model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Define the get_sql function
def get_sql(query):
    input_text = "translate English to SQL: %s" % query
    features = tokenizer([input_text], return_tensors='pt')

    output = model.generate(input_ids=features['input_ids'],
                            attention_mask=features['attention_mask'],
                            max_new_tokens=50)

    return tokenizer.decode(output[0], skip_special_tokens=True)