import ollama
import requests
import json

def get_weather(city:str)->str:
    response= requests.get(f"https://wttr.in/{city}?format=%C+%t")
    return response.text

client=ollama.Client(
    host="http://127.0.0.1:11434"
)

System_Prompt= """
    Use tool for all the weather query, when ever you are using a tool, respond only with valid json
    {
        "tool":"get_weather"
        "args":{
            "city": "<city_name>"
        }
    }

    for the rest give me the normal response

"""
user_query=input("-> ")
response=client.chat(
    model="qwen2.5:7b",
    messages=[
        {
            "role":"system",
            "content":System_Prompt
        },
        {
            "role":"user",
            "content":user_query
        }
    ]
)

parse = response["message"]["content"]

if "tool" in parse:
    parse=json.loads(parse)
    # print(parse["tool"])
    args = parse.get("args",{})
    print(get_weather(**args))
    # print(result)
else:
    print(parse)