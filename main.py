from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key=os.getenv("API_KEY")
# print(api_key)
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system", "content": "You are an expert in Maths and only and only answer maths related question. if the query is not related to the math just say sorry. "
        },
        {
            "role":"user", "content":"Hey, can you help me to solve the question 2+84"
        }
    ]
)

# print("hello world ")
print(response.choices[0].message.content)
