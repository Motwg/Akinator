import json

from flask import Flask
# from .extensions import cache

from .jinjafilters import *
from .errorhandlers import *


def create_app(mode='prod'):
    if mode == 'test':
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_file('../test-config.json', load=json.load)
    elif mode == 'prod':
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_file('../prod-config.json', load=json.load)
    else:
        raise AttributeError(f'Failed to load flask with mode {mode}')
    # cache.init_app(app)

    with app.app_context():
        # from .db import get_db
        # get_db()

        # Add Blueprints
        from .blueprints import bl_home
        app.register_blueprint(bl_home.bp)

        # from .blueprints import bl_traps
        # app.register_blueprint(bl_traps.bp)
        #
        # from .blueprints import bl_connections
        # app.register_blueprint(bl_connections.bp)

        from .blueprints import auth
        app.register_blueprint(auth.bp)

    # Add error handlers
    app.register_error_handler(500, error_500)
    app.register_error_handler(404, error_404)

    # jinja filters
    app.jinja_env.filters['slugify'] = slugify
    app.jinja_env.filters['displayError'] = display_error
    app.jinja_env.filters['displayMessage'] = display_message

    return app
