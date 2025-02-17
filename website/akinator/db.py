from flask import current_app, g
import mysql.connector


def get_db():
    if 'db' not in g or not g.db.is_connected():
        g.db = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_DATABASE'],
            # ssl_verify_identity=True,
            # ssl_ca='SSL/certs/ca-cert.pem',
            # use_pure=True
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()


current_app.teardown_appcontext(close_db)
