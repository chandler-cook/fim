import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from getpass import getpass

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 32-byte key from the password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path: str, key: bytes):
    """Encrypts a file using AES-GCM."""
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # Generate a random 12-byte nonce and a 16-byte salt
    nonce = os.urandom(12)
    salt = os.urandom(16)

    # Derive the encryption key
    encryption_key = derive_key(key.decode(), salt)

    # Encrypt the file
    cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Write encrypted data
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as f:
        f.write(salt + nonce + encryptor.tag + ciphertext)

    # Remove original file
    os.remove(file_path)

    print(f"Encrypted: {file_path} -> {encrypted_file_path}")

def encrypt_directory(directory: str, password: str):
    """Encrypts all files in a directory."""
    key = password.encode()
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)

if __name__ == "__main__":
    dir_path = input("Enter directory path to encrypt: ")
    if not os.path.isdir(dir_path):
        print("Invalid directory.")
        exit(1)
    
    password = getpass("Enter encryption password: ")
    encrypt_directory(dir_path, password)
    print("Encryption complete.")
