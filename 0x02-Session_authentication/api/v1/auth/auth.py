#!/usr/bin/env python3

""" Module of Auth views """

from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """ Auth class for the API """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
                        """
        if not path or not excluded_paths:
            return True
        # Ensure path does not end with a trailing slash unless needed
        if path[-1] == '/':
            path = path[:-1]

        # Check for exact matches or wildcard matches
        for excluded_path in excluded_paths:
            # Handle paths with wildcard '*'
            if fnmatch.fnmatch(path, excluded_path):
                return False

            # Check if the path or path with a trailing slash matches exactly
            if path == excluded_path.rstrip(
                    '/') or path + '/' == excluded_path.rstrip('/'):
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

    def session_cookie(self, request=None):
        """ session_cookie
                        """
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))
