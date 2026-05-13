from flask import Flask
from cryptography.fernet import Fernet
from pusher import Pusher
from config import Config
import pymysql

fernet = None
pusher_client = None
db_config = None

def get_db():
    config = {
        'host': db_config['host'],
        'user': db_config['user'],
        'password': db_config['password'],
        'database': db_config['database'],
        'port': db_config['port'],
        'ssl': {'ca': db_config['ssl_ca']} if db_config.get('ssl_ca') else None,
        'cursorclass': pymysql.cursors.Cursor
    }
    return pymysql.connect(**config)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    global fernet, pusher_client, db_config

    # Config base de données
    db_config = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'database': app.config['MYSQL_DB'],
        'port': app.config['MYSQL_PORT'],
        'ssl_ca': app.config.get('MYSQL_SSL_CA')
    }

    # Initialisation Fernet
    fernet = Fernet(app.config['FERNET_KEY'])

    # Initialisation Pusher
    pusher_client = Pusher(
        app_id=app.config['PUSHER_APP_ID'],
        key=app.config['PUSHER_KEY'],
        secret=app.config['PUSHER_SECRET'],
        cluster=app.config['PUSHER_CLUSTER'],
        ssl=True
    )

    # Enregistrement des routes
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.messages import messages_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(messages_bp)

    return app