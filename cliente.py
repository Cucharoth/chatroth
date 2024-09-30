import socket
import threading
import sys

all_messages = []

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                # Salir del bucle si no hay mensaje (socket cerrado)
                break  
            if message == b'newconexion':
                if len(all_messages):
                    whole_message = "\n".join(all_messages)
                    client_socket.send(whole_message.encode('utf-8'))
            else:
                if message:
                    print(message.decode('utf-8'))
                    all_messages.append(message.decode('utf-8'))
        except socket.error as e:
            print(f"Socket error: {e}")
            break

def main():
    try: 
        print('Bienvenido nuevo cliente, después de ingresar su nombre, para salir ingrese /logout')
        user_name = input('<<< Ingrese su nombre de usuario: ')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 10005))

        # Envía el nombre de usuario al servidor
        client.send(user_name.encode('utf-8'))

        # Crea hilo para conexiones entrantes
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        while True:
            message = input("You: ")
            if message == '/logout':
                # Cierra el socket 
                client.shutdown(socket.SHUT_RDWR)  
                client.close()
                # Espera a que el hilo de recepción termine
                receive_thread.join()  
                break
            all_messages.append(f'{user_name}: {message}')
            client.send(f'{user_name}: {message}'.encode('utf-8')) 
    except socket.error as e:
        print(f"Socket error: {e}")
    finally: 
        client.close()
        print('\nHistorial de mensajes:')
        for msg in all_messages:
            print(msg)
        # Termina el programa inmediatamente
        sys.exit(0) 

if __name__ == "__main__":
    main()