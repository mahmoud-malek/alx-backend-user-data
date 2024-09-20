#!/usr/bin/env python3

""" Session expiration authentication views """

from flask import abort, jsonify, request
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session expiration authentication views """

    def __init__(self):
        """ Constructor """
        self.session_duration = 0

        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            pass

    def create_session(self, user_id=None):
        """ Create session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ User ID for Session ID """
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None:
            return None

        user_id = session_dictionary.get("user_id")

        if user_id is None:
            return None

        if self.session_duration <= 0:
            return user_id

        created_at = session_dictionary.get("created_at")

        if created_at is None:
            return None

        if (datetime.now() - created_at) > \
                timedelta(seconds=self.session_duration):
            return None

        return user_id
