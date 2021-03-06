from rest_framework.authentication import get_authorization_header, BaseAuthentication 

from rest_framework.permissions import BasePermission

from rest_framework import exceptions

from authentication.models import User

from django.conf import settings
import jwt


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode("utf-8")
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed(
                {"status": "error", "message": "Token not valid"}
            )

        token = auth_token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

            username = payload["username"]
            user = User.objects.get(username=username)
            return (user, None)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                {"status": "error", "message": "Token is expired, login again",}
            )

        except jwt.DecodeError as de:
            raise exceptions.AuthenticationFailed(
                {"status": "error", "message": "Token is invalid"}
            )
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                {"status": "error", "message": "User Doesnot Exist!"}
            )

        return super().authenticate(request)
