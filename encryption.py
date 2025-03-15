from cryptography.fernet import Fernet

# Generate a key for encryption
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_message(message):
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(message):
    return cipher.decrypt(message.encode()).decode()