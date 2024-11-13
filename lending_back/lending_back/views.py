import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, os.getenv("SERVICE_ACCOUNT_FILE"))

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

class SubmitApplicationView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("full_name")
        phone = data.get("phone")
        email = data.get("email")
        organization = data.get("organization", "")


        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()


        values = [[name, phone, email, organization]]
        body = {
            "values": values
        }


        try:
            sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range="Лист1!A:D",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            return Response({"message": "Заявка успешно отправлена!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": "Ошибка при отправке заявки."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

