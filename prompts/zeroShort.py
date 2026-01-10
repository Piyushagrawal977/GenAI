from dotenv import load_dotenv
from openai import OpenAI
import os


"""
Zero short Prompting
The model is given a direct question or task without prior example.

"""

load_dotenv()
api_key=os.getenv("API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

System_Prompt = "You are a Math Teacher, answer only the math related question apart from it don't entertain any query and just say sorry"
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system", "content": System_Prompt
        },
        {
            "role":"user", "content":"Hey, give me equation for the differentaition"
        }
    ]
)

# print("hello world ")
print(response.choices[0].message.content)
