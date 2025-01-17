import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Hàm mã hóa mật khẩu
def encrypt_password(password, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(decode_key(key)), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()    
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
    encrypted_data = iv + encrypted_password
    return base64.b64encode(encrypted_data).decode()


# Hàm giải mã mật khẩu
def decrypt_password(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    encrypted_password = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(decode_key(key)), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
    return decrypted_password.decode()

def encoded_key():
    return base64.b64encode(os.urandom(32)).decode()

def decode_key(encoded_key):
    return base64.b64decode(encoded_key)