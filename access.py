"""Вход в читальный зал и выход из него."""

from secrets import compare_digest, token_urlsafe

from flask import Blueprint, abort, current_app, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash


access = Blueprint("access", __name__)


def check_token() -> None:
    expected = session.get("form_token")
    actual = request.form.get("token", "")
    if not expected or not compare_digest(expected.encode(), actual.encode()):
        abort(400, "Обновите страницу и повторите действие.")


@access.route("/login", methods=("GET", "POST"))
def login():
    username = current_app.config["READING_USER"]
    password_hash = current_app.config["READING_PASSWORD_HASH"]
    if not (username and password_hash and current_app.secret_key):
        return render_template("login.html", enabled=False), 503
    if request.method == "GET":
        session.setdefault("form_token", token_urlsafe(24))
        return render_template("login.html", enabled=True)

    check_token()
    name_ok = compare_digest(request.form.get("username", "").encode(), username.encode())
    password_ok = check_password_hash(password_hash, request.form.get("password", ""))
    if not (name_ok and password_ok):
        return render_template("login.html", enabled=True, invalid=True), 401
    session.clear()
    session["reader"] = username
    session["form_token"] = token_urlsafe(24)
    return redirect(url_for("access.room"))


@access.get("/reading-room")
def room():
    reader = session.get("reader")
    if not reader or reader != current_app.config["READING_USER"]:
        return redirect(url_for("access.login"))
    return render_template("room.html", reader=reader)


@access.post("/logout")
def logout():
    check_token()
    session.clear()
    return redirect(url_for("home"))
