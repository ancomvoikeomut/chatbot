import os
from groq import Groq
from dotenv import load_dotenv, find_dotenv
import sys
import utils
from groq.types.chat import ChatCompletionMessageParam
_ = load_dotenv(find_dotenv())

client = Groq(api_key = os.getenv("Groq_API_KEY"))

def get_completion_from_messages(messages, model="llama-3.3-70b-versatile"):
    response = client.chat.completions.create(
        model=model,
        messages=messages, 
        temperature=0,
        
    )
    return response.choices[0].message.content

def process_user_message(user_input, all_messages, debug=True):
    delimiter = "```"
    category_and_product_response = utils.find_category_and_product_only(user_input, utils.get_products_and_category())
    category_and_product_list = utils.read_string_to_list(category_and_product_response)
    product_information = utils.generate_output_string(category_and_product_list)
    system_messages = f"""
    Bạn là trợ lí Ai hỗ trợ của một cửa hàng điện máy lớn.
    Hỗ trợ với tông giọng thân thiện, với câu trả lời chính xác.
    Đặt ra những câu hỏi tiếp theo có liên quan.
    """
    messages = [
        {'role': 'system', 'content': system_messages},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
    ]

    final_response = get_completion_from_messages(all_messages + messages)
    all_messages = all_messages + messages[1:]

    return final_response, all_messages
user_input = "cho tôi biết về laptop gaming"
response, _ = process_user_message(user_input, [])
print(response)
