from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import json
from pydantic import BaseModel
from typing import Literal
import time
import os



"""
chain of thought

"""

load_dotenv()
# client = OpenAI(
#     api_key="AIzaSyAwePF1oeR9cGvsTxcmUBYKl95JdZk__EA",
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )


api_key=os.getenv("API_KEY")
class OutputSchema(BaseModel):
    step: Literal["START" , "PLAN" ,"OUTPUT"]
    content: str


System_Prompt = """
You are an AI assistant following an externalized reasoning protocol.

You MUST respond in exactly one step at a time, using the following JSON schema:

{
  "step": "START | PLAN | OUTPUT",
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
"""
client = genai.Client(
     api_key=api_key,
)



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
            "response_mime_type":"application/json",
            "response_schema":OutputSchema
            }

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
    time.sleep(3)
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
