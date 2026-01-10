from google import genai
import json
from pydantic import BaseModel
import os
from dotenv import load_dotenv
class OutputSchema(BaseModel):
    message:str

load_dotenv()

api_key=os.getenv("API_KEY")
client = genai.Client(
    api_key=api_key,
)

user_query=input("👉 ")
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=user_query, 
    config={
        "response_mime_type":"application/json",
        "response_schema":OutputSchema
    }
)
print(response.parsed.message)