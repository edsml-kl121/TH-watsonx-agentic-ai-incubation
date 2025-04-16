import requests
import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model

load_dotenv()
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

model_id_llm = "meta-llama/llama-3-3-70b-instruct"
api_key = os.getenv("WATSONX_API_KEY", None)
ibm_cloud_url = os.getenv("WATSONX_API_BASE", None)
project_id = os.getenv("WATSONX_PROJECT_ID", None)
creds = {
    "url": ibm_cloud_url,
    "apikey": api_key
}
model = connect_watsonx_llm(model_id_llm)




# sales_force_data = [{'Unit Price': 61.5, 'Pricebook Name': 'Excelentia Supplies'}, {'Unit Price': 76.9, 'Pricebook Name': 'Global Office Solutions'}, {'Unit Price': 92.3, 'Pricebook Name': 'CGV Supplier'}]




# def research_suppliers(user_query):
#     # user query: "Research the suppliers for Xtralife.", "Supplier for Xtralife"
#     # web search, procuement rules, sales reviews, pricing from salesforce
#     # products = get_all_price_book()
#     # prompt = f" {user_query} ให้คะแนนซัพพลายเออร์จากบนลงล่างโดยพิจารณาจากตัวเลือกที่ดีที่สุดไปจนถึงแย่ที่สุด พร้อมทั้งแบ่งปันเหตุผลด้วย ข้อมูลราคาสำหรับซัพพลายเออร์ ทั้งหมด: [{{'Unit Price': 61.5, 'Pricebook Name': 'Excelentia Supplies'}}, {{'Unit Price': 76.9, 'Pricebook Name': 'Global Office Solutions'}}, {{'Unit Price': 92.3, 'Pricebook Name': 'CGV Supplier'}}]. พิจารณาข้อกำหนดและบทวิจารณ์การขายของซัพพลายเออร์เหล่านี้ด้วย"
    
#     messages = [
#         {"role": "system", "content": """You always answer the questions with markdown formatting using GitHub syntax. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.

#     Any HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized for not rendering code in block quotes.

#     When returning code blocks, specify language.

#     You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
#     Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

#     If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""},
#         {"role": "user", "content": f"{user_query} ช่วยเรียงลำดับซัพพลายเออร์จากบนลงล่างโดยพิจารณาจากตัวเลือกที่ดีที่สุดไปจนถึงแย่ที่สุด พร้อมทั้งแบ่งปันเหตุผลด้วย ข้อมูลราคาสำหรับซัพพลายเออร์ ทั้งหมด: {sales_force_data}. พิจารณาข้อกำหนดและบทวิจารณ์การขายของซัพพลายเออร์เหล่านี้ด้วย. ตอบสั่นๆ และกระชับ"""},
#     ]
#     print("USERQ", user_query)
#     # prompt = f"ผู้จัดจำหน่ายรายใดระหว่าง Excelentia Supplies และ Global Office Supplies เป็นตัวเลือกที่เหมาะสมในการซื้อผลิตภัณฑ์ Xtralife ช่วยให้รายการข้อดีและข้อเสียของผู้จัดจำหน่ายแต่ละราย"
#     generated_response = model.chat(messages=messages)
#     rating = generated_response['choices'][0]['message']['content']
#     # add llm to extract top supplier
#     return rating


def create_inventory_task(current_inventory, historic_data, forecast):
    def calculate_reorder_quantity(forecast, inventory, historic_sales):
        # Step 1: Calculate shortfall
        shortfall = forecast - inventory
        
        # Step 2: Safety stock logic
        if shortfall <= historic_sales:
            safety_stock = 0.1 * historic_sales  # 10% of historic sales
            reorder_quantity = shortfall + safety_stock
        else:
            safety_stock = 0
            reorder_quantity = shortfall
        
        return {
            "Shortfall": shortfall,
            "Safety Stock": safety_stock,
            "Reorder Quantity": reorder_quantity
        }
    reorder_quantity = calculate_reorder_quantity(forecast, current_inventory, historic_data)
    user_query = f"""Explain how the optimal reorder quantity was arrived to ensure sufficient stock while minimizing excess inventory. 

Below are the Instructions for calculating the optimal reorder quantity:
1. Shortfall calculation.
    Shortfall = Forecast - Inventory
2. Saftey stock calculation
    If shortfall <= historic sales:
        Saftety Stock = 10% of historic sales
        Reorder Quantity = Shortfall + Safety Stock
    If shortfall > historic sales:
        Reorder Quantity = Shortfall

From using a calculator:
Given the following data:
- Current Inventory: {current_inventory}
- Quantity sold previous month: {historic_data}
- Forecasted Quantity for next month: {forecast}
Optimal reorder quantity: {reorder_quantity["Reorder Quantity"]}
Explain in thai and explain very concisely with natural language."""
    messages = [
        {"role": "system", "content": """You always answer the questions with markdown formatting using GitHub syntax. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.

    Any HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized for not rendering code in block quotes.

    When returning code blocks, specify language.

    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
    Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""},
        {"role": "user", "content": f"{user_query}"""},
    ]
    generated_response = model.chat(messages=messages)
    reasoning = generated_response['choices'][0]['message']['content']
    # add llm to extract top supplier
    return {"reorder_quantity": str(int(reorder_quantity["Reorder Quantity"])), "reasoning": reasoning}

# print (researchsuppliers("Research the suppliers for Xtralife."))