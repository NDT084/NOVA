from flask import Flask, g
from cryptography.fernet import Fernet
from pusher import Pusher
from config import Config
import pymysql

fernet = None
pusher_client = None

def get_db():
    # On récupère proprement la config depuis le contexte de l'application Flask active
    from flask import current_app
    
    # Évite de réouvrir une connexion si elle existe déjà pour cette requête
    if 'db' not in g:
        config = {
            'host': current_app.config['MYSQL_HOST'],
            'user': current_app.config['MYSQL_USER'],
            'password': current_app.config['MYSQL_PASSWORD'],
            'database': current_app.config['MYSQL_DB'],
            'port': int(current_app.config['MYSQL_PORT']),
            'cursorclass': pymysql.cursors.DictCursor # DictCursor est souvent plus pratique
        }
        
        # Gestion stricte du SSL exigé par Aiven Cloud
        if current_app.config.get('MYSQL_SSL_CA'):
            config['ssl'] = {'ca': current_app.config['MYSQL_SSL_CA']}
        else:
            config['ssl'] = {'ssl': {}}  # Force le SSL générique si le chemin CA n'est pas fourni
            
        g.db = pymysql.connect(**config)
        
    return g.db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    global fernet, pusher_client

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

    # Nettoyage automatique des connexions en fin de requête (Crucial pour Vercel)
    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    # Enregistrement des routes
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.messages import messages_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(messages_bp)

    return app
