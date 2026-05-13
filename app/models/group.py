from app import mysql
from app.utils import generate_invite_code

def create_group(name, owner_id):
    cursor = mysql.connection.cursor()
    invite_code = generate_invite_code()
    cursor.execute(
        "INSERT INTO `groups` (name, invite_code, owner_id) VALUES (%s, %s, %s)",
        (name, invite_code, owner_id)
    )
    mysql.connection.commit()
    group_id = cursor.lastrowid

    # Ajouter le créateur comme membre
    cursor.execute(
        "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
        (group_id, owner_id)
    )
    mysql.connection.commit()
    cursor.close()
    return invite_code

def get_group_by_code(invite_code):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `groups` WHERE invite_code = %s", (invite_code,))
    group = cursor.fetchone()
    cursor.close()
    return group

def join_group(group_id, user_id):
    cursor = mysql.connection.cursor()
    # Vérifier si déjà membre
    cursor.execute(
        "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
        (group_id, user_id)
    )
    existing = cursor.fetchone()
    if existing:
        cursor.close()
        return False
    cursor.execute(
        "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
        (group_id, user_id)
    )
    mysql.connection.commit()
    cursor.close()
    return True

def get_user_groups(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT g.* FROM `groups` g
        JOIN group_members gm ON g.id = gm.group_id
        WHERE gm.user_id = %s
        ORDER BY g.created_at DESC
    """, (user_id,))
    groups = cursor.fetchall()
    cursor.close()
    return groups
def get_group_by_id(group_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `groups` WHERE id = %s", (group_id,))
    group = cursor.fetchone()
    cursor.close()
    return group

def get_group_members(group_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT u.id, u.username FROM users u
        JOIN group_members gm ON u.id = gm.user_id
        WHERE gm.group_id = %s
    """, (group_id,))
    members = cursor.fetchall()
    cursor.close()
    return members