import ollama
import requests
import json 
import time

def get_weather(city:str)->str:
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
        return response.text
    except:
        return "something went wrong"


client = ollama.Client(
    host="http://127.0.0.1:11434"
)

System_Prompt="""
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

CRITICAL TOOL RULE:

If the user asks about weather, temperature, climate, or current conditions
for any city or place, you MUST NOT answer directly.

You MUST respond ONLY with valid JSON in this exact format:

{
  "tool": "get_weather",
  "args": {
    "city": "<city_name>"
  }
}

Do not include START, PLAN, OUTPUT, or any text.
Do not explain.
Do not guess.
Return ONLY the JSON.


Use tools only for to get the weather data.
Do NOT use tools for reasoning or explanation.
"""

reasoning_history = []
previous_step = None
plan_count = 0
MAX_PLAN_STEPS = 10

user_query = input("👉 ")

while True:
    # -------- build context --------
    context_lines = []
    context_lines.append(f"User query: {user_query}")

    if reasoning_history:
        context_lines.append("Previous steps:")
        for step in reasoning_history:
            context_lines.append(f"{step['step']}: {step['content']}")

    prompt = "\n".join(context_lines)

    # -------- call Ollama --------
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": System_Prompt},
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response["message"]["content"].strip()

    # -------- TOOL DETECTION --------
    try:
       
        parsed = json.loads(raw_text)
        # print(parsed)
        if "tool" in parsed:
            tool_name = parsed["tool"]
            args = parsed.get("args", {})

            if tool_name == "get_weather":
                result = get_weather(**args)
                print(result)
            else:
                print("❌ Unknown tool")
                break

            # log TOOL (controller-side)
            reasoning_history.append({
                "step": "TOOL",
                "content": f"{tool_name}({args}) → {result}"
            })
            print(reasoning_history)
            # continue loop with tool result now in history
            # time.sleep(1)
            continue

    except json.JSONDecodeError:
        pass  # not a tool call → continue normal flow

    # -------- NORMAL STEP (START / PLAN / OUTPUT) --------
    try:
        step_json = json.loads(raw_text)
        step = step_json["step"]
        content = step_json["content"]
    except Exception:
        print("Invalid JSON from model:")
        print(raw_text)
        break

    # -------- step validation --------
    if previous_step is None and step != "START":
        print("❌ Invalid first step")
        break

    if previous_step == "START" and step != "PLAN":
        print("❌ START must be followed by PLAN")
        break

    if previous_step == "PLAN" and step not in ("PLAN", "OUTPUT"):
        print("❌ Invalid step after PLAN")
        break

    if reasoning_history and step == "PLAN":
        if reasoning_history[-1]["content"] == content:
            print("❌ Repeated PLAN detected")
            continue

    # -------- commit step --------
    reasoning_history.append({
        "step": step,
        "content": content
    })
    previous_step = step

    # -------- display --------
    if step == "START":
        print("🔥", content)

    elif step == "PLAN":
        print("🧠", content)
        plan_count += 1
        if plan_count >= MAX_PLAN_STEPS:
            print("❌ Max PLAN steps exceeded")
            break

    elif step == "OUTPUT":
        print("🤖", content)
        break

    time.sleep(1)
