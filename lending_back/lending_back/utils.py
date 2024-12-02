import os
from dotenv import load_dotenv
import requests


load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

def generate_text(prompt: str):

    if not HF_API_TOKEN:
        raise ValueError("HF_API_TOKEN не найден. Проверьте .env файл.")

    url = "https://api-inference.huggingface.co/models/sberbank-ai/rugpt3small_based_on_gpt2"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 100,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        raise ValueError(f"Ошибка API Hugging Face: {response.status_code}, {response.text}")
