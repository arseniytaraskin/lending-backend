
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
from google.oauth2.service_account import Credentials

import os
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, os.getenv("SERVICE_ACCOUNT_FILE"))


SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_notification(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Ошибка Telegram API: {response.status_code}, {response.text}")



SEND_TELEGRAM_NOTIFICATIONS = True

class SubmitApplicationView(APIView):
    def post(self, request):
        try:

            submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_name = request.data.get('full_name', '').strip()
            phone_number = request.data.get('phone_number', '').strip()
            email = request.data.get('email', '').strip()
            organization = request.data.get('organization', '').strip()


            if not full_name or not phone_number or not email:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)


            credentials = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            service = build("sheets", "v4", credentials=credentials)
            sheet = service.spreadsheets()

            values = [[full_name, phone_number, email, organization, submission_time]]
            response = sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range="Лист1!A1",
                valueInputOption="RAW",
                body={"values": values}
            ).execute()


            if SEND_TELEGRAM_NOTIFICATIONS:
                message = (
                    f"📥 <b>Новая заявка</b>\n"
                    f"👤 <b>Имя:</b> {full_name}\n"
                    f"📞 <b>Телефон:</b> {phone_number}\n"
                    f"✉️ <b>Email:</b> {email}\n"
                    f"🏢 <b>Организация:</b> {organization or 'Не указано'}\n"
                    f"⏰ <b>Время:</b> {submission_time}"
                )
                send_telegram_notification(message)

            return Response({"message": "Application submitted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": "An error occurred while submitting the application"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import os
import time
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

@csrf_exempt
def generate_text_view(request):
    if request.method == "POST":
        try:

            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            if not prompt:
                return JsonResponse({"error": "Текст для генерации не предоставлен."}, status=400)


            result = call_huggingface_api(prompt)
            return JsonResponse({"generated_text": result}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "GET":
        prompt = request.GET.get("prompt", "Дай небольшой продающий текст")
        result = call_huggingface_api(prompt)
        return JsonResponse({"generated_text": result}, status=200)

    return JsonResponse({"error": "Метод не поддерживается."}, status=405)


def call_huggingface_api(prompt: str, retries=5, wait_time=5):

    if not HF_API_TOKEN:
        raise ValueError("HF_API_TOKEN не найден. Проверьте .env файл.")


    url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct"


    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}


    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 1024,
            "temperature": 0.4,
            "top_k": 50,
            "top_p": 0.8,
            "frequency_penalty": 0.0,
            "max_tokens": 2048
        }
    }

    for attempt in range(1, retries + 1):

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:

            return response.json()[0].get("generated_text", "Текст не сгенерирован.")
        elif response.status_code == 503:

            error = response.json().get("error", "")
            estimated_time = response.json().get("estimated_time", wait_time)
            time.sleep(estimated_time or wait_time)
        else:
            raise ValueError(f"Ошибка API Hugging Face: {response.status_code}, {response.text}")

    raise ValueError("Модель недоступна после нескольких попыток.")



import time
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

@csrf_exempt
def generate_image_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "An artistic depiction of a sunset over mountains")

            if not prompt:
                return JsonResponse({"error": "Описание изображения отсутствует."}, status=400)

            image_url = call_huggingface_image_api(prompt)
            return JsonResponse({"image_url": image_url}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Метод не поддерживается."}, status=405)

def call_huggingface_image_api(prompt: str, retries=5, wait_time=10):
    if not HF_API_TOKEN:
        raise ValueError("HF_API_TOKEN не найден. Проверьте .env файл.")

    url = "https://api-inference.huggingface.co/models/Datou1111/shou_xin"  # URL модели

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt}

    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)  # Увеличен тайм-аут

            print(f"Response {attempt + 1}: {response.status_code} - {response.text}")

            if response.status_code == 200:
                # Попробуем распечатать ответ для отладки
                response_data = response.json()
                print("Response Data:", response_data)
                # Предполагаем, что в ответе будет изображение или URL изображения
                return response_data[0].get("generated_image", "Изображение не получено.")

            elif response.status_code == 503:
                print(f"Сервер недоступен, попытка {attempt + 1} из {retries}. Попробую снова через {wait_time} секунд.")
                time.sleep(wait_time)
            else:
                raise ValueError(f"Ошибка API Hugging Face: {response.status_code}, {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            time.sleep(wait_time)

    raise ValueError("Модель недоступна после нескольких попыток.")

