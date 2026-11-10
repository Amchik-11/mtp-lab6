"""Книжная гостиная на Flask."""

import os
from secrets import token_hex

import click
from flask import Flask, render_template
from werkzeug.security import generate_password_hash

from access import access


READING_LIST = (
    ("Маленький принц", "Антуан де Сент-Экзюпери", "Небольшая повесть на вечер"),
    ("Два капитана", "Вениамин Каверин", "Приключенческий роман на выходные"),
    ("Три товарища", "Эрих Мария Ремарк", "Роман для книжного клуба"),
)


def create_app(settings=None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        READING_USER=os.getenv("READING_USER"),
        READING_PASSWORD_HASH=os.getenv("READING_PASSWORD_HASH"),
        SESSION_COOKIE_SECURE=bool(os.getenv("DYNO")),
        SESSION_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=8192,
    )
    if settings:
        app.config.update(settings)
    app.register_blueprint(access)

    @app.get("/")
    def home():
        return app.send_static_file("welcome.html")

    @app.get("/showcase")
    def showcase():
        return app.send_static_file("showcase.html")

    @app.get("/recommendations")
    def recommendations():
        return render_template("recommendations.html", books=READING_LIST)

    @app.cli.command("access-values")
    def access_values():
        """Подготовить переменные для учебного входа."""
        password = click.prompt("Отдельный пароль для читального зала", hide_input=True, confirmation_prompt=True)
        click.echo(f"READING_PASSWORD_HASH={generate_password_hash(password)}")
        click.echo(f"SECRET_KEY={token_hex(32)}")

    return app


app = create_app()


@click.command()
@click.option("--demo", is_flag=True, help="Открыть локальный читальный зал с учебным входом.")
def run(demo: bool) -> None:
    if not demo:
        app.run(host="127.0.0.1")
        return

    demo_password = "reading-demo"
    reading_room = create_app({
        "READING_USER": "reader",
        "READING_PASSWORD_HASH": generate_password_hash(demo_password),
        "SECRET_KEY": token_hex(32),
        "SESSION_COOKIE_SECURE": False,
    })
    click.echo(f"Вход в читальный зал — reader, пароль — {demo_password}")
    reading_room.run(host="127.0.0.1")


if __name__ == "__main__":
    run()
