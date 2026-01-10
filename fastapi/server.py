from fastapi import FastAPI, Body
from pydantic import BaseModel
import ollama

app = FastAPI()

client = ollama.Client(
    host="http://localhost:11434"
)
class ChatRequest(BaseModel):
    message:str

@app.get("/")
def red_loot():
    return { "hello ":"world"}

@app.get("/hello")
def red_loot():
    return {"hello"}

@app.post("/chat")
def chat(
     req:ChatRequest
):
    response=client.chat(model="gemma:2b",messages=[
        {'role':"user","content":req.message}
    ])

    return {"response":response.message.content}
   
