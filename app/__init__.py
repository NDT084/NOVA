from flask import Flask
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
from pusher import Pusher
from config import Config

mysql = MySQL()
fernet = None
pusher_client = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisation MySQL
    mysql.init_app(app)

    # Initialisation Fernet
    global fernet
    fernet = Fernet(app.config['FERNET_KEY'])

    # Initialisation Pusher
    global pusher_client
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