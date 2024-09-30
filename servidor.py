import socket
import threading
import signal
from typing import List, Dict

class Server: 
    def __init__(self) -> None:
        self.clients: List[socket.socket] = []
        self.client_usernames: Dict[socket.socket, str] = {}
        self.all_messages: Dict[socket.socket, List[str]] = {}
        self.server: socket.socket

    def __broadcast(self, message: bytes, sender_socket: socket.socket) -> None:
        '''Send the message to all clients except the sender.'''
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"ERROR: {e}")
                    # If sending fails, remove the client
                    client.close()
                    self.clients.remove(client)

    def __handle_client(self, client_socket: socket.socket) -> None:
        '''Incoming messages from a client.'''
        try:
            # Recibe el nombre de usuario del cliente
            username = client_socket.recv(1024).decode('utf-8')
            self.client_usernames[client_socket] = username
            print(f"{username} se ha conectado.")

            while True:
                message = client_socket.recv(1024)
                if message:
                    if client_socket not in self.all_messages:
                        self.all_messages[client_socket] = []
                    self.all_messages[client_socket].append(message.decode('utf-8'))
                    print(f"{message.decode('utf-8')}")
                    self.__broadcast(message, client_socket)
                else:
                    break
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            # Remove the client if connection is lost
            client_socket.close()
            self.clients.remove(client_socket)
            print(f"{self.client_usernames[client_socket]} se ha desconectado.")
            del self.client_usernames[client_socket]

    def main(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Permitir reutilización del puerto
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
            self.server.bind(("0.0.0.0", 10005))
            self.server.listen(5)
            
            print('Servidor inicializado, esperando conexión...')

            def sigint_handler(signal, frame):
                for client in self.clients:
                    client.close()
                if self.server:
                    self.server.close()
                print("Servidor cerrado.")
                exit(0)

            signal.signal(signal.SIGINT, sigint_handler)

            while True:
                client_socket, addr = self.server.accept()
                print(f"Conexión exitosa con: {addr}")
                self.clients.append(client_socket)
                self.clients[0].send('newconexion'.encode('utf-8'))  # Convertir a bytes
                thread = threading.Thread(target=self.__handle_client, args=(client_socket,))
                thread.start()

        finally:
            if self.server:
                self.server.close()

if __name__ == "__main__":
    Server = Server()
    Server.main()