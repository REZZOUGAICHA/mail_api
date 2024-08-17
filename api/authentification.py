import jwt
from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class TokenAuthentication(BaseTokenAuth):
    keyword = 'Bearer'
    