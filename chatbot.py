import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_llm_response(symptoms_text):
    prompt = f"""
You are a medical assistant. Based on the following symptoms: "{symptoms_text}", generate the following response STRICTLY in this JSON format without any extra explanation:

{{
  "medicines": ["Medicine 1", "Medicine 2", "..."],
  "precautions": ["Precaution 1", "Precaution 2", "..."],
  "diet": ["Diet tip 1", "Diet tip 2", "..."]
}}

Only return valid JSON. Do not include markdown or text before/after the JSON.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format from LLM."}
    else:
        return {"error": f"API Error: {response.status_code}"}
