import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Recibe e imprime mensaje
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received: {message.decode('utf-8')}")
            else:
                break
        except:
            break

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

# Generate RSA key pair
private_key, public_key = generate_rsa_key_pair()

# Save private key to PEM file
save_private_key_to_pem(private_key, 'private.pem')

# Load private key from PEM file
private_key = load_private_key_from_pem('private.pem')

# Save public key to PEM file
save_public_key_to_pem(public_key, 'public.pem')

# Load public key from PEM file
public_key = load_public_key_from_pem('public.pem')

# Generate random symmetric key
symmetric_key = get_random_bytes(32)

# Encrypt the symmetric key using the public key
encrypted_key = encrypt_symmetric_key(public_key, symmetric_key)

# Encrypt the plaintext using the symmetric key
#plaintext = b"Hello, world!"
#ciphertext = encrypt(plaintext, symmetric_key)

# Decrypt the symmetric key using the private key
decrypted_key = decrypt_symmetric_key(private_key, encrypted_key)

# Decrypt the ciphertext using the symmetric key
decrypted_plaintext = decrypt(ciphertext, decrypted_key)

print("Encrypted text:", ciphertext)
print("Decrypted plaintext:", decrypted_plaintext.decode())

def main():
    try: 
        user_name = input('<<< Ingrese su nombre de usuario:')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 666))

        # Crea hilo para conexiones entrantes
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        while True:
            message = input("You: ")
            ciphertext = encrypt(message, symmetric_key)
            client.send(f'{user_name}: {message}'.encode('utf-8'))
    finally: 
        client.close()

if __name__ == "__main__":
    main()
main()