#!/usr/bin/env python3

""" Module of Auth views """

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class for the API """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract_base64_authorization_header
                                     """
        if not authorization_header or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ decode_base64_authorization_header
             """
        if not base64_authorization_header:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            return base64.b64decode(base64_authorization_header).decode(
                'utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract_user_credentials
                """
        if not decoded_base64_authorization_header or \
                type(decoded_base64_authorization_header) is not str or \
                ":" not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":", 1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ user_object_from_credentials
                """
        if not user_email or not user_pwd:
            return None

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            from models.user import User
            users = User.search({"email": user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
                """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        credentials = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(credentials[0],
                                                 credentials[1])
