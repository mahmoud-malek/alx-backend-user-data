#!/usr/bin/env python3

"""DB module defines a DB class

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User

from typing import TypeVar


class DB:
    """DB class
        """

    def __init__(self) -> None:
        """Initialize a new DB instance
                """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
                """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the data base
                """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> TypeVar('User'):
        """ Finds a user by a given attribute
                """
        if not kwargs:
            raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound

        return user
