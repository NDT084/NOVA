from app import mysql
from app.utils import hash_password

def create_user(username, email, password):
    cursor = mysql.connection.cursor()
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed)
    )
    mysql.connection.commit()
    cursor.close()

def get_user_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_user_by_id(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user