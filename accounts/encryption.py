# utils/encryption.py
from cryptography.fernet import Fernet

# Generate a secret key for encryption. You should keep this key secure and not expose it in your code.
SECRET_KEY = Fernet.generate_key()


def encrypt_data(data):
    # Convert the data to a string if it's an integer
    if isinstance(data, int):
        data = str(data)

    f = Fernet(SECRET_KEY)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data):
    f = Fernet(SECRET_KEY)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data
