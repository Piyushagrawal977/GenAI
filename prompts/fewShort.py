from dotenv import load_dotenv
from openai import OpenAI
import os


"""
Few short Prompting
The model is given a direct question or task with few examples before asking it to generate a response.

"""

load_dotenv()
api_key=os.getenv("API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

System_Prompt = """
You are a Math Teacher and only answer the Math realted question. For any other query just say sorry.

Rule: 
- Strictly follow the output in json format.

Output Foramt:
{{
"answer": "string" or null,
"isMathQuestion": boolean

}}

Example: 
Q: Can you write Poem for me?
A: {{"answer": null, isMathQuestion: false}}

Q: What is the sum for 234, 321 and 111
A: {{"answer": 666, isMathQuestion: true}}
"""



response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system", "content": System_Prompt
        },
        {
            "role":"user", "content":"Hey, Can you write a letter for me"
        }
    ]
)

# print("hello world ")
print(response.choices[0].message.content)
