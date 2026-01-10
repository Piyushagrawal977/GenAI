from dotenv import load_dotenv
# from google import genai
import ollama
import json
from pydantic import BaseModel
from typing import Literal
import time
import os
import requests
from google.genai import types

"""
chain of thought

"""

load_dotenv()
# client = OpenAI(
#     api_key="AIzaSyAwePF1oeR9cGvsTxcmUBYKl95JdZk__EA",
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

get_weather_declaration = {
    "name":"get_weather",
    "parameters":{
        "type":"object",
        "properties":{
            "city":{
                "type":"string"
            }
        },
        "required":["city"]
    }

}

def get_weather(city:str)->str:
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
        return response
    except:
        return "something went wrong"


api_key=os.getenv("API_KEY")
class OutputSchema(BaseModel):
    step: Literal["START" , "PLAN" ,"OUTPUT"]
    content: str

# weather_tool = tools.Tool(
#     callable=get_weather,
#     description="Get the weather of a city"
# )



System_Prompt = """
You are an AI assistant following an externalized reasoning protocol.

You MUST respond in exactly one step at a time, using the following JSON schema:

{
  "step": "START | PLAN | OUTPUT ",
  "content": "string"
}


Protocol rules:

Always return valid JSON matching the schema.

Return ONLY one step per response — never combine steps.

The allowed step sequence is:

START → PLAN (one or more times) → OUTPUT

Never skip steps in the sequence.

Once you return OUTPUT, the task is complete and no further steps are allowed.

START:

Acknowledge the user query.

Restate the goal briefly.

PLAN:

Provide one small reasoning or planning action only.

Do NOT solve the full problem.

Do NOT reveal internal hidden thoughts.

Keep it concise and incremental.

OUTPUT:

Provide the final answer only.

No reasoning, no planning, no extra explanation.

Do not include any text outside the JSON object.


Progression control rules:

You are responsible for deciding when planning is complete.

You MUST NOT move to OUTPUT until all necessary planning steps are completed.

You MUST produce at least one PLAN step before OUTPUT.

Each PLAN step must add new information or advance the solution.

If no further planning is required, transition to OUTPUT in the next response.

Do NOT repeat the same planning step.

Do NOT stall indefinitely in PLAN.

Tool usage rules:

- You have access to external tools when necessary.
- Use a tool ONLY if the information cannot be reliably determined without it.
- When you decide to use a tool, you MUST request the tool instead of guessing.
- Do NOT fabricate tool results.
- Do NOT include tool calls inside the JSON response.
- Tool calls are separate from reasoning steps.
- After receiving a tool result, incorporate it into the next PLAN or OUTPUT step.

Use tools only for to get the weather data.
Do NOT use tools for reasoning or explanation.
"""
client = genai.Client(
     api_key=api_key,
)
tools = types.Tool(function_declarations=[get_weather_declaration])



reasoning_history =[]
plan_count=0
previous_step = None
user_query = input("👉 ")




while True:

    context =[
        f"user query: {user_query}\n"
    ]

    if reasoning_history:
        context.append("Previous steps:")
        for step in reasoning_history:
            context.append(
                f'{step["step"]}: {step["content"]}'
            )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context,
        config={
            "system_instruction": System_Prompt,
            # "response_mime_type":"application/json",
            # "response_schema":OutputSchema,
            "tools":[tools]
            },
        

    )

    parts = response.candidates[0].content.parts

    tool_called = False

    for part in parts:
        if part.function_call:
            tool_called = True
            fn_name = part.function_call.name
            args = part.function_call.args
            break
    if tool_called:
        if fn_name=="get_weather":
            result = get_weather(**args)
        else:
            print("Unknown tool")
            break
        reasoning_history.append({
            "step":"TOOL",
            "content":f"{fn_name}({args})->{result}"
        })
        context.append(f"Tool result: {result}")
        time.sleep(10)
        continue
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context,
        config={
            "system_instruction": System_Prompt,
            "response_mime_type":"application/json",
            "response_schema":OutputSchema,
            # "tools":[tools]
            },
        

    )
    step = response.parsed.step
    content=response.parsed.content
    
    if previous_step is None and step!= "START":
        print("invalid first step")
        break
    if previous_step == "START" and step not in ("PLAN",):
        print ("Start must be followed by the Plan")
        break
    if previous_step == "PLAN" and step not in ("PLAN","OUTPUT"):
        print("Invalid step after PLAN")
        break
    if reasoning_history and step == "PLAN":
        if reasoning_history[-1]["content"] == content:
            print("❌ Repeated PLAN detected")
            continue

    reasoning_history.append({
        "step": step,
        "content": content
    })

    previous_step = step

    # ---- Display ----
    if step == "START":
        print("🔥", content)

    elif step == "PLAN":
        print("🧠", content)
        plan_count += 1
        if plan_count >= 10:
            print("❌ Max PLAN steps exceeded")
            break

    elif step == "OUTPUT":
        print("🤖", content)
        break
    time.sleep(10)
# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={"type":"json_object"},
#     messages=[
#         {
#             "role":"system", "content": System_Prompt
#         },
#         {
#             "role":"user", "content":"Hey, give me equation for the differentaition"
#         }
#     ]
# )

# # print("hello world ")
# print(response.choices[0].message.content)
