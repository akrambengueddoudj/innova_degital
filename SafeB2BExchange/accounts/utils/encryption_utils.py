from cryptography.fernet import Fernet
from decouple import config

fernet = Fernet(config('FERNET_SECRET_KEY').encode())

def encrypt_bytes(data: bytes) -> bytes:
    return fernet.encrypt(data)

def decrypt_bytes(data):
    if isinstance(data, memoryview):
        data = data.tobytes()
    return fernet.decrypt(data)