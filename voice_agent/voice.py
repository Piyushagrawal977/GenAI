# code doen't work properly

import whisper
import ollama
import pyttsx3
import os

# 1️⃣ Record audio using Windows (FFmpeg via PowerShell)
# os.system(
#     r'powershell.exe -ExecutionPolicy Bypass '
#     r'-File "D:\genai\voice_agent\record.ps1"'
# )


# 2️⃣ Ollama client
client = ollama.Client(
    host="http://127.0.0.1:11434"
)

# 3️⃣ Speech → Text
def speech_to_text():
    model = whisper.load_model("base")
    result = model.transcribe("/mnt/d/genai/voice_agent/input.wav")
    return result["text"]

# 4️⃣ Text → LLM
def ask_llm(prompt):
    response = client.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.message.content

# 5️⃣ Text → Speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 6️⃣ Pipeline
print("Speak...")
user_text = speech_to_text()
print("🧑 You said:", user_text)

ai_reply = ask_llm(user_text)
print("🤖 AI:", ai_reply)

speak(ai_reply)
