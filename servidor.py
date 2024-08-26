import socket
import threading
import signal

# Lista con los clientes (sockets) conectados
clients = []

def broadcast(message, sender_socket):
    """Send the message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # If sending fails, remove the client
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """Handle incoming messages from a client."""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"{message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    # Remove the client if connection is lost
    client_socket.close()
    clients.remove(client_socket)

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 666))
        server.listen(5)
        print("Servidor inicializado, esperando conexión...")
        def sigint_handler():
            print("handler")
            for client in clients:
                client.close()
            server.close()
        signal.signal(signal.SIGINT,sigint_handler)
        
            
        
        while True:
            client_socket, addr = server.accept()
            print(f"Conexión exitosa con: {addr}")
            clients.append(client_socket)
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

    finally:
        # Clean up the connection
        server.close()


    

if __name__ == "__main__":
    main()

main()
