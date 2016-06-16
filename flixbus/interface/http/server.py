from werkzeug.serving import run_simple
import statsd

import app
from .v1 import api
from middleware.auth import Auth
from middleware.statsd import StatsdMiddleware

application = app.create_app()

# Register blueprint
application.register_blueprint(
    api.v1, url_prefix='/v1'
)

# Apply middleware
application.wsgi_app = StatsdMiddleware(
    application, statsd.StatsClient(), 'Flixbus'
)
application = Auth(application)


def run_development_server():
    # Run Server
    run_simple(
        '0.0.0.0', 5000, application, use_reloader=True,
        use_debugger=True, use_evalex=True
    )

if __name__ == '__main__':
    run_development_server()
