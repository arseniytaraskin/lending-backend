from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, \
    permissions as rest_permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import tokens, views as jwt_views
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from . import serializers, models, permissions as custom_permissions
from .serializers import LoginSerializer, RegistrationSerializer, CookieTokenRefreshSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.views.decorators.csrf import csrf_exempt


def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }


@extend_schema(
    summary="Вход пользователя",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(response=LoginSerializer, description="Пользователь успешно вошел"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['Auth']
)
@csrf_exempt
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(email=email, password=password)

    if user is not None:
        tokens = get_user_tokens(user)
        res = response.Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.data = tokens
        res["X-CSRFToken"] = csrf.get_token(request)
        return res
    raise rest_exceptions.AuthenticationFailed(
        "Email or Password is incorrect!")


@extend_schema(
    summary="Создание пользователя",
    request=RegistrationSerializer,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Пользователь успешно создан"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['User']
)
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([custom_permissions.IsAdmin])
def create(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")

@extend_schema(
    summary="Выход пользователя",
    request=None,
    responses={
        200: OpenApiResponse(description="Пользователь успешно вышел"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['Auth']
)
@rest_decorators.api_view(['POST'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"] = None

        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")


# @extend_schema(
#     summary="Обновить токены",
#     # parameters=[
#     #     OpenApiParameter(
#     #         name="X-CSRFTOKEN",
#     #         location=OpenApiParameter.HEADER,
#     #     ),
#     # ],
#     request={},
#     responses={
#         200: OpenApiResponse(description="Токены успешно обновлены"),
#         400: OpenApiResponse(description="Ошибки валидации")
#     }
# )
class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    @extend_schema(
        summary="Обновить токены",
        # parameters=[
        #     OpenApiParameter(
        #         name="X-CSRFTOKEN",
        #         location=OpenApiParameter.HEADER,
        #     ),
        # ],
        request={},
        responses={
            200: OpenApiResponse(description="Токены успешно обновлены"),
            400: OpenApiResponse(description="Ошибки валидации")
        },
        tags=['Auth']
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)

@extend_schema(
    summary="Любой пользователь",
    request=RegistrationSerializer,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Пользователь"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['Tests']
)
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except models.User.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.UserSerializer(user)
    return response.Response(serializer.data)

@extend_schema(
    summary="Администратор",
    request=RegistrationSerializer,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Администратор"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['Tests']
)
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([custom_permissions.IsAdmin])
def admin(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except models.User.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.UserSerializer(user)
    return response.Response(serializer.data)

@extend_schema(
    summary="Владелец",
    request=RegistrationSerializer,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Владелец"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['Tests']
)
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([custom_permissions.IsSuperUser])
def superuser(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except models.User.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.UserSerializer(user)
    return response.Response(serializer.data)

@extend_schema(
    summary="Редактор",
    request=RegistrationSerializer,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Редактор"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['Tests']
)
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([custom_permissions.IsStaff])
def staff(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except models.User.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.UserSerializer(user)
    return response.Response(serializer.data)

@extend_schema(
    summary="Получение пользователей",
    request=None,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Пользователи успешно получены"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['User']
)
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([custom_permissions.IsAdmin])
def get(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")

@extend_schema(
    summary="Удаление пользователя",
    request=None,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Пользователи успешно получены"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['User']
)
@rest_decorators.api_view(["DELETE"])
@rest_decorators.permission_classes([custom_permissions.IsAdmin])
def delete(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")

@extend_schema(
    summary="Обновление пользователя",
    request=None,
    responses={
        201: OpenApiResponse(response=RegistrationSerializer, description="Пользователи успешно получены"),
        400: OpenApiResponse(description="Ошибки валидации")
    },
    tags=['User']
)
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([custom_permissions.IsAdmin])
def update(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")