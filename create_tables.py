from app import create_app, get_db

app = create_app()

with app.app_context():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `groups` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        invite_code VARCHAR(10) NOT NULL UNIQUE,
        owner_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS group_members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        group_id INT NOT NULL,
        user_id INT NOT NULL,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES `groups`(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        group_id INT NOT NULL,
        user_id INT NOT NULL,
        content TEXT NOT NULL,
        is_ghost BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES `groups`(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    db.commit()
    cursor.close()
    db.close()
    print("Tables créées avec succès sur Aiven !")