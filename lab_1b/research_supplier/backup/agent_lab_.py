from ibm_watsonx_ai.foundation_models import Model
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("WATSONX_API_KEY", None)
ibm_cloud_url = os.getenv("WATSONX_API_BASE", None)
project_id = os.getenv("WATSONX_PROJECT_ID", None)

creds = {
    "url": ibm_cloud_url,
    "apikey": api_key
}
def connect_watsonx_llm(model_id_llm):
    model = Model(
        model_id=model_id_llm,
        params = {
            'decoding_method': "greedy",
            'min_new_tokens': 1,
            'max_new_tokens': 1600,
            'temperature': 0.0,
            'repetition_penalty': 1.2
        },
        credentials=creds,
        project_id=project_id
        )
    return model

sales_force_data = [{'Unit Price': 61.5, 'Pricebook Name': 'Excelentia Supplies'}, {'Unit Price': 76.9, 'Pricebook Name': 'Global Office Solutions'}, {'Unit Price': 92.3, 'Pricebook Name': 'CGV Supplier'}]

messages = [
    {"role": "system", "content": """You always answer the questions with markdown formatting using GitHub syntax. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.

Any HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized for not rendering code in block quotes.

When returning code blocks, specify language.

You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""},
    {"role": "user", "content": f"ให้คะแนนซัพพลายเออร์จากบนลงล่างโดยพิจารณาจากตัวเลือกที่ดีที่สุดไปจนถึงแย่ที่สุด พร้อมทั้งแบ่งปันเหตุผลด้วย ข้อมูลราคาสำหรับซัพพลายเออร์ ทั้งหมด: {sales_force_data}. พิจารณาข้อกำหนดและบทวิจารณ์การขายของซัพพลายเออร์เหล่านี้ด้วย"}
]
model_id_llm = "meta-llama/llama-3-3-70b-instruct"
model = connect_watsonx_llm(model_id_llm)
generated_response = model.chat(messages=messages)

# Print only content
print(generated_response['choices'][0]['message']['content'])