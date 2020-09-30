#!/usr/bin/env python3

from flask import Flask, request
from flask_jwt import jwt_required, current_identity
import requests

import email
import users
import config
from . import config

from collections import namedtuple
from sys import argv

app = Flask("reactor")
app.config['SECRET_KEY'] = config["flask"]["secret_key"]
app.config['JWT_AUTH_PASSWORD_KEY'] = 'token'
jwt = users.init_jwt(app)


@app.route("/ok")
def health():
    return "ok"


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['u']
        user = users.username_table[username]

        try:
            confirm = request.form['c']
            if confirm != "true":
                raise KeyError
        except KeyError:
            return render_template("web/login_email_check.html", username=username, email_masked=email.mask(user.email))

        token = user.new_token()
        login_link = url_for('login', u=username, t=token)
        email.send(user.email, render_template("email/login.txt", login_link=login_link, username=username, base_url=request.base_url))
        return render_template("web/login_sent.html")

    try:
        token = request.args['t']
    except KeyError:
        return render_template("login.html")

    new_jwt = requests.post(f"{request.base_url}/auth", json={"username": username, "token": token})
    new_jwt.raise_for_status()

    # FIXME: set new_jwt for future authorization headers somehow?

    return redirect('root')


@app.route('/')
@jwt_required()
def root():
    return f"Welcome, {{current_identity}}!"


if __name__ == '__main__':
    app.run(debug="--debug" in argv)
