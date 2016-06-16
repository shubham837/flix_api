import app
from flask.ext.testing import TestCase
from middleware.auth import Auth
import json
import constants


class TestAuth(TestCase):
    def create_app(self):
        return app.create_app(testing=True)

    def setUp(self):
        self.auth = Auth(self.app)
        self.app.redis_client.setex(
            constants.REDIS_AUTH_KEY_FORMAT % "TEST_AUTH_KEY",
            json.dumps({"type": "flixbus_data_app"}), 300)
        self.app.redis_client.setex(
            constants.REDIS_ACCESS_TOKEN_KEY_FORMAT % "TEST_ACCESS_TOKEN",
            json.dumps({"user_id": 123}), 300)

    def test_authenticate_without_key(self):
        cred = self.auth._authenticate("", "")
        self.assertEquals(cred, {})

    def test_authenticate_with_key(self):
        cred = self.auth._authenticate("TEST_AUTH_KEY", "TEST_ACCESS_TOKEN")
        self.assertNotEquals(cred, {})
        self.assertEquals(cred['client_type'], 'flixbus_data_app')
        self.assertEquals(cred['user_id'], 123)
