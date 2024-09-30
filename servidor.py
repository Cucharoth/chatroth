import socket
import threading
import signal

# Lista con los clientes (sockets) conectados
clients = []

client_usernames = {}  

all_messages = {}

def broadcast(message, sender_socket):
    """Send the message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"ERROR: {e}")
                # If sending fails, remove the client
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """Handle incoming messages from a client."""
    try:
        # Recibe el nombre de usuario del cliente
        username = client_socket.recv(1024).decode('utf-8')
        client_usernames[client_socket] = username
        print(f"{username} se ha conectado.")

        while True:
            message = client_socket.recv(1024)
            if message:
                if client_socket not in all_messages:
                    all_messages[client_socket] = []
                all_messages[client_socket].append(message.decode('utf-8'))
                print(f"{message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                break
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        # Remove the client if connection is lost
        client_socket.close()
        clients.remove(client_socket)
        print(f"{client_usernames[client_socket]} se ha desconectado.")
        del client_usernames[client_socket]

def main():
    server = None
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Permitir reutilización del puerto
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        server.bind(("0.0.0.0", 10005))
        server.listen(5)
        
        print('Servidor inicializado, esperando conexión...')

        def sigint_handler(signal, frame):
            for client in clients:
                client.close()
            if server:
                server.close()
            print("Servidor cerrado.")
            exit(0)

        signal.signal(signal.SIGINT, sigint_handler)

        while True:
            client_socket, addr = server.accept()
            print(f"Conexión exitosa con: {addr}")
            clients.append(client_socket)
            clients[0].send('newconexion'.encode('utf-8'))  # Convertir a bytes
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

    finally:
        # Clean up the connection
        if server:
            server.close()

if __name__ == "__main__":
    main()