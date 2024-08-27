import socket
import threading
import sys
from Crypto.Random import get_random_bytes

sys.path.append('../')
from crypto import *

all_messages = []

# Recibe e imprime mensaje
def receive_messages(client_socket):
    while True:
        try:
            message_encrypted_key = load_encrypted_key('../cliente_1/encrypted_symmetric_key')
            decrypted_key = decrypt_symmetric_key(private_key, message_encrypted_key)
            ciphertext = client_socket.recv(1024)
            if ciphertext == b'newconexion':
                for message in all_messages:
                    ciphertext = encrypt(f'{message}'.encode('utf-8'), symmetric_key)
                    client_socket.send(ciphertext)
            else:
                message = decrypt(ciphertext, decrypted_key).decode()
                if message:
                    print(f"{message}")
                else:
                    break
        except Exception as e:
            print(f"except?: {e}")
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
        client.bind(("127.0.0.1", 11004))
        client.connect(("127.0.0.1", 10005))

        # Crea hilo para conexiones entrantes
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        while True:
            message = input("You: ")
            all_messages.append(f'{user_name}: {message}')
            ciphertext = encrypt(f'{user_name}: {message}'.encode('utf-8'), symmetric_key)
            client.send(ciphertext)
    finally: 
        client.close()

if __name__ == "__main__":
    main()
