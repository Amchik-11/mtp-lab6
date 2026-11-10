"""Проверка маршрутов и входа в читальный зал."""

import unittest

from werkzeug.security import generate_password_hash

from main import create_app


class RoomTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app({
            "TESTING": True,
            "SECRET_KEY": "test-key",
            "READING_USER": "читатель",
            "READING_PASSWORD_HASH": generate_password_hash("test-password"),
            "SESSION_COOKIE_SECURE": False,
        }).test_client()

    def test_public_pages(self):
        for path, marker in (("/", "reading.css"), ("/showcase", "table-striped"),
                             ("/recommendations", "Каверин")):
            with self.subTest(path=path), self.client.get(path) as response:
                self.assertEqual(response.status_code, 200)
                self.assertIn(marker, response.get_data(as_text=True))

    def test_room_requires_a_login(self):
        self.assertEqual(self.client.get("/reading-room").location, "/login")
        self.assertEqual(self.client.post("/login").status_code, 400)
        self.client.get("/login")
        with self.client.session_transaction() as session:
            token = session["form_token"]
        fields = {"username": "читатель", "password": "wrong", "token": token}
        self.assertEqual(self.client.post("/login", data=fields).status_code, 401)
        fields["password"] = "test-password"
        self.assertEqual(self.client.post("/login", data=fields).location, "/reading-room")
        self.assertIn("Добро пожаловать", self.client.get("/reading-room").get_data(as_text=True))
        self.assertEqual(self.client.post("/logout", data={"token": token}).status_code, 400)
        with self.client.session_transaction() as session:
            new_token = session["form_token"]
        self.assertEqual(self.client.post("/logout", data={"token": new_token}).location, "/")
        self.assertEqual(self.client.get("/reading-room").location, "/login")
