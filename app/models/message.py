from app import get_db
from app.utils import encrypt_message, decrypt_message

def save_message(group_id, user_id, content, is_ghost=False):
    if is_ghost:
        return None

    db = get_db()
    cursor = db.cursor()
    encrypted = encrypt_message(content)
    cursor.execute(
        "INSERT INTO messages (group_id, user_id, content, is_ghost) VALUES (%s, %s, %s, %s)",
        (group_id, user_id, encrypted, False)
    )
    db.commit()
    cursor.close()
    db.close()

def get_group_messages(group_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.id, u.username, m.content, m.created_at
        FROM messages m
        JOIN users u ON m.user_id = u.id
        WHERE m.group_id = %s
        ORDER BY m.created_at ASC
    """, (group_id,))
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    messages = []
    for row in rows:
        try:
            decrypted = decrypt_message(row[2])
        except Exception:
            decrypted = "[message illisible]"
        messages.append({
            'id': row[0],
            'username': row[1],
            'content': decrypted,
            'created_at': str(row[3])
        })
    return messages