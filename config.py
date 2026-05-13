import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY')

    # MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')

    # Fernet
    FERNET_KEY = os.getenv('FERNET_KEY').encode()

    # Pusher
    PUSHER_APP_ID = os.getenv('PUSHER_APP_ID')
    PUSHER_KEY = os.getenv('PUSHER_KEY')
    PUSHER_SECRET = os.getenv('PUSHER_SECRET')
    PUSHER_CLUSTER = os.getenv('PUSHER_CLUSTER')