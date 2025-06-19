import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

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

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        try:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            result = json.loads(text)
            return result
        except (KeyError, json.JSONDecodeError):
            return {"error": "Invalid or malformed response from Gemini."}
    else:
        return {"error": f"Google API Error: {response.status_code}"}
