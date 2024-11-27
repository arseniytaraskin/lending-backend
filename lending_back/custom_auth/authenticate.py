from rest_framework_simplejwt import authentication as jwt_authentication
from django.conf import settings
from rest_framework import authentication, exceptions as rest_exceptions


def enforce_csrf(request):
    check = authentication.CSRFCheck(request)
    reason = check.process_view(request, None, (), {})
    if reason:
      raise rest_exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CustomAuthentication(jwt_authentication.JWTAuthentication):
    def authenticate(self, request):
        token = self.get_header(request) or request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if token is None:
            return token

        validated_token = self.get_validated_token(token)
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token
        
