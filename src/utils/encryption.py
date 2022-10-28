from cryptography.fernet import Fernet

import config

fernet = Fernet(config.ENCRYPTION_KEY)

def encrypt(message):
    return fernet.encrypt(message)

def decrypt(message):
    return fernet.decrypt(message)



if __name__ == '__main__':
    message = 'cccccccccccccccccccccccccccccccccccccccccccc'.encode()
    encrypted = encrypt(message)
    print(encrypted)
    decrypted = decrypt(encrypted)
    print(decrypted.decode())