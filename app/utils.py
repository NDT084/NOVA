import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from app import fernet

# Hachage du mot de passe
def hash_password(password):
    return generate_password_hash(password)

# Vérification du mot de passe
def verify_password(password, hashed):
    return check_password_hash(hashed, password)

# Génération du code d'invitation NV-XXXX
def generate_invite_code():
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(chars, k=4))
    return f"NV-{code}"

# Chiffrement d'un message
def encrypt_message(content):
    return fernet.encrypt(content.encode()).decode()

# Déchiffrement d'un message
def decrypt_message(encrypted_content):
    return fernet.decrypt(encrypted_content.encode()).decode()