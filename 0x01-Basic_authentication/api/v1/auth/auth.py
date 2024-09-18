#!/usr/bin/env python3

""" Module of Auth views """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class for the API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """
        if not path or not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        if path[:-1] in excluded_paths or path + '/' in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None
