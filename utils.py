
import os
from groq import Groq
from dotenv import load_dotenv , find_dotenv
import json
_ = load_dotenv(find_dotenv())
client  = Groq(api_key = os.getenv("Groq_API_KEY"))
def get_completion_from_messages(messages ,model  = "llama-3.3-70b-versatile"):
    response =  client.chat.completions.create(
        model=model,
        messages = messages,
        temperature = 0
    )
    return response.choices[0].message.content
def find_category_and_product_only(user_input, products):
    import json
    with open("product.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    system_messages = f"""
    Bạn là Ai phân tích câu hỏi của khách hàng.\
    Danh sách sản phẩm {products}\
    Trả về category và product dưới dạng JSON,\
    """
    messages = [
        {"role" : "system", "content" : system_messages},
        {"role" : "user", "content" : user_input}
    ]
    return get_completion_from_messages(messages)
def read_string_to_list(input_string):
    import json
    try:
        return json.loads(input_string)
    except:
        return []
def get_products_and_category():
    import json
    with open("product.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    result = {}
    for item in products:
        category = item["category"]
        result[category] = [p["name"] for p in item["products"]]
    return result


def generate_output_string(product_list):
    import json
    with open("product.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    output_string = ""

    if not product_list:
        return output_string

    for item in product_list:
        category = item.get("category")
        product_name = item.get("product")

        for cat in products:
            if cat["category"] == category:
                for p in cat["products"]:
                    if p["name"] == product_name:
                        output_string += json.dumps(p, ensure_ascii=False) + "\n"

    return output_string