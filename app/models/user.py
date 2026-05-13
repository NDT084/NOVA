from app import get_db
from app.utils import hash_password

def create_user(username, email, password):
    db = get_db()
    cursor = db.cursor()
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed)
    )
    db.commit()
    cursor.close()
    db.close()

def get_user_by_email(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user