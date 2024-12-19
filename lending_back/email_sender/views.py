from django.core import serializers
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template import loader
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators
from . import serializers


@extend_schema(
    summary="Отправка письма",
    request=serializers.Letter,
    responses={
        200: OpenApiResponse(description="Письмо успешно отправлено"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['email']
)
@rest_decorators.api_view(["POST"])
def send(request):
    letter = serializers.Letter(data=request.data)
    letter.is_valid(raise_exception=True)
    # inject the respective values in HTML template
    context = letter.validated_data['body'] | {'name': letter.validated_data['recipient'],
                                               'sign': letter.validated_data['sender']}
    html_message = loader.render_to_string(
        letter.validated_data['template'],
        # 'email_sender_app/message.html',
        context)
    send_mail(
        '',
        '',
        letter.validated_data['sender'],
        [letter.validated_data['recipient']],
        html_message=html_message,
        fail_silently=False,
    )

    return HttpResponse("Mail Sent!!")
