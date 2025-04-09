from cryptography.fernet import Fernet # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
import base64
import os
from typing import Tuple

def generate_key(passkey: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    """Generate a secure encryption key using PBKDF2 key derivation"""
    if salt is None:
        salt = os.urandom(16)  # Generate a new salt
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passkey.encode()))
    return key, salt

def encrypt_data(data: str, passkey: str) -> str:
    """Encrypt data with passkey using Fernet encryption"""
    salt = os.urandom(16)
    key, salt = generate_key(passkey, salt)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    
    # Combine salt + encrypted data for storage
    return base64.urlsafe_b64encode(salt + encrypted).decode()

def decrypt_data(encrypted_data: str, passkey: str) -> str:
    """Decrypt data with passkey"""
    try:
        decoded = base64.urlsafe_b64decode(encrypted_data.encode())
        salt = decoded[:16]
        encrypted = decoded[16:]
        
        key, _ = generate_key(passkey, salt)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted).decode()
    except:
        raise ValueError("Decryption failed - incorrect passkey or corrupted data")