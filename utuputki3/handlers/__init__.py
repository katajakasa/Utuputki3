# -*- coding: utf-8 -*-

from . import auth

handlers = {
    'auth.login': auth.login,
    'auth.logout': auth.logout,
    'auth.authenticate': auth.authenticate,
}
