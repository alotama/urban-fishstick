import json
from cryptography.fernet import Fernet
from config.config import load_config

config = load_config()
env_encryption_key = config['env_encryption_key'].encode()

def generate_key():
    return Fernet.generate_key()

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as env_encryption_key:
        env_encryption_key.write(encrypted)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as env_encryption_key:
        encrypted = env_encryption_key.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)