
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

class SubmitApplicationView(APIView):
    def post(self, request):
        try:
            # Получение данных из запроса
            submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_name = request.data.get('full_name', '').strip()
            phone_number = request.data.get('phone_number', '').strip()
            email = request.data.get('email', '').strip()
            organization = request.data.get('organization', '').strip()


            # Проверка данных
            if not full_name or not phone_number or not email:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Установление соединения с Google Sheets
            credentials = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            service = build("sheets", "v4", credentials=credentials)
            sheet = service.spreadsheets()

            # Формирование данных для отправки
            values = [[full_name, phone_number, email, organization, submission_time]]

            # Добавление данных в таблицу
            response = sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range="Лист1!A1",  # Укажите диапазон, в который будут добавляться данные
                valueInputOption="RAW",
                body={"values": values}
            ).execute()

            return Response({"message": "Application submitted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": "An error occurred while submitting the application"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

