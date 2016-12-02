# -*- coding: utf-8 -*-

import enum


class UserLevel(enum.IntEnum):
    GUEST = 0
    USER = 10
    ADMIN = 20
    ROOT = 30


class Session(object):
    def __init__(self, db):
        self._db = db
        self._user = None
        self._is_logged = False
        self._session_id = None
        self._level = UserLevel.GUEST

    def get_user(self):
        return self._user

    def get_session_id(self):
        return self._session_id

    def is_logged(self):
        return self._is_logged

    def get_level(self):
        return self._level
