from cryptography.fernet import Fernet
from config.config import KEY

class Encryption():
    def __init__(self):
        self.f = Fernet(KEY)

    def encrypt(self, password):
        encrypted_password = self.f.encrypt(password.encode())
        return encrypted_password.decode()

    def decrypt(self, password):
        decrypted_password = self.f.decrypt(password.encode())
        return decrypted_password.decode()