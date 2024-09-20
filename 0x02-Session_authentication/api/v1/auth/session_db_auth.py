#!/usr/bin/env python3

""" defines the user authentication model for db storage """

from api.v1.auth.session_auth import SessionAuth


class SessionDBAuth(SessionAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ Create a session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        from models.user_session import UserSession
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ User ID for Session ID """
        if session_id is None:
            return None

        from models.user_session import UserSession
        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return None

        if self.session_duration <= 0:
            return user_session[0].user_id

        if (user_session[0].created_at +
                self.session_duration) < datetime.now():
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """ Delete a session / logout """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        from models.user_session import UserSession
        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return False

        user_session[0].remove()

        return True
