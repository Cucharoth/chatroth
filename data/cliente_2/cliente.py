import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
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

# Recibe e imprime mensaje
def receive_messages(client_socket):
    while True:
        try:
            message_encrypted_key = load_encrypted_key('../cliente_1/encrypted_symmetric_key')
            decrypted_key = decrypt_symmetric_key(private_key, message_encrypted_key)
            ciphertext = client_socket.recv(1024)
            message = decrypt(ciphertext, decrypted_key).decode()
            if message:
                print(f"{message}")
            else:
                break
        except:
            break

# Genera par de claves
# private_key, public_key = generate_rsa_key_pair()

# Guarda clave privada en PEM file
# save_private_key_to_pem(private_key, 'private.pem')

# carga clave privada desde PEM file
private_key = load_private_key_from_pem('private.pem')

# Guarda clave publica en PEM file
# save_public_key_to_pem(public_key, 'public.pem')

# Carga clave publica desde PEM file
public_key = load_public_key_from_pem('../cliente_1/public.pem')

# Crea clave simétrica
symmetric_key = get_random_bytes(32)

# Encripta llave simétrica utilizando clave publica
encrypted_key = encrypt_symmetric_key(public_key, symmetric_key)
save_encrypted_key = save_encrypted_key(encrypted_key, 'encrypted_symmetric_key')

# Des-encripta llave simétrica utilizando clave privada
# message_encrypted_key = load_encrypted_key('../cliente_2/encrypted_symmetric_key');
# decrypted_key = decrypt_symmetric_key(private_key, encrypted_key)


def main():
    try: 
        user_name = input('<<< Ingrese su nombre de usuario: ')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 666))

        # Crea hilo para conexiones entrantes
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        while True:
            message = input("You: ")
            ciphertext = encrypt(f'{user_name}: {message}'.encode('utf-8'), symmetric_key)
            client.send(ciphertext)
    finally: 
        client.close()

if __name__ == "__main__":
    main()