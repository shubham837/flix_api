import json
import constants


class Auth(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        credentials = self._authenticate(
            environ.get('HTTP_AUTH_KEY'),
            environ.get('HTTP_ACCESS_TOKEN')
        )
        environ['HTTP_USER'] = credentials.get('user_id', '')
        environ['HTTP_CLIENT_TYPE'] = credentials.get('client_type', '')
        return self.app(environ, start_response)

    def _authenticate(self, auth_key, access_token):
        client = self.app.redis_client
        auth_key = client.get(constants.REDIS_AUTH_KEY_FORMAT % (auth_key))
        access_token = client.get(
            constants.REDIS_ACCESS_TOKEN_KEY_FORMAT % (access_token))
        credentials = {}
        if auth_key:
            credentials['client_type'] = json.loads(auth_key)['type'].lower()
            if access_token:
                credentials['user_id'] = json.loads(access_token)['user_id']
        return credentials
