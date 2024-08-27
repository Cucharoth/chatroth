from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def save_private_key_to_pem(private_key, filename):
    with open(filename, 'wb') as file:
        file.write(private_key)


def load_private_key_from_pem(filename):
    with open(filename, 'rb') as file:
        private_key = file.read()
    return private_key

def save_public_key_to_pem(public_key, filename):
    with open(filename, 'wb') as file:
        file.write(public_key)

def load_public_key_from_pem(filename):
    with open(filename, 'rb') as file:
        public_key = file.read()
    return public_key

def save_encrypted_key(encrypted_symmetric_key, filename):
    with open(filename, 'wb') as file:
        file.write(encrypted_symmetric_key)

def load_encrypted_key(filename):
    with open(filename, 'rb') as file:
        public_key = file.read()
    return public_key       

def encrypt_symmetric_key(public_key, symmetric_key):
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_key = cipher_rsa.encrypt(symmetric_key)
    return encrypted_key


def decrypt_symmetric_key(private_key, encrypted_key):
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    decrypted_key = cipher_rsa.decrypt(encrypted_key)
    return decrypted_key


def encrypt(plaintext, symmetric_key):
    cipher = AES.new(symmetric_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = cipher.iv
    return iv + ciphertext


def decrypt(ciphertext, symmetric_key):
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(symmetric_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext