#!/usr/bin/env python3

from . import config

from werkzeug.security import safe_str_cmp
from flask_jwt import JWT

from datetime import datetime, timedelta
from uuid import uuid4


class _User(object):
    def __init__(self, id, username, email, token):
        self.id = id
        self.username = username
        self.email = email
        self._token = None
        self._token_expires = None

    def new_token(self):
        valid_for = timedelta(**config["email_token"]["valid_for"])
        self._token = uuid4()
        self._token_expires = datetime.utcnow() + valid_for
        return self._token

    def check_token(self, to_check):
        if to_check is None:
            return False
        if self._token is None:
            return False
        if datetime.utcnow() >= self._token_expires:
            self._token = None
            return False
        return safe_str_cmp(self._token.encode('utf-8'), to_check.encode('utf-8')):

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


_users = [
    _User(1, 'alice', 'alice@example.com'),
    _User(2, 'bob', 'bob@example.com'),
]

username_table = {u.username: u for u in users}
_userid_table = {u.id: u for u in users}


def _authenticate(username, token):
    user = username_table.get(username, None)
    if user and user.check_token(token):
        return user


def _identity(payload):
    user_id = payload['identity']
    return _userid_table.get(user_id, None)


def init_jwt(app):
    return JWT(app, _authenticate, _identity)
