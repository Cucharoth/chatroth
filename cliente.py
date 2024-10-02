import socket
import threading
import sys
class Client(): 
    def __init__(self) -> None:
        self.all_messages = []
        self.user_name: str 

    def __receive_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break  
                if message == b'newconexion':
                    if len(self.all_messages):
                        whole_message = "\n".join(self.all_messages)
                        client_socket.send(whole_message.encode('utf-8'))
                else:
                    if message:
                        print(message.decode('utf-8'))
                        self.all_messages.append(message.decode('utf-8'))
            except socket.error as e:
                print(f"Socket error: {e}")
                break

    def main(self):
        try: 
            print('Bienvenido nuevo cliente, después de ingresar su nombre, para salir ingrese /logout')
            self.user_name = input('<<< Ingrese su nombre de usuario: ')

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("200.13.4.197", 2024))

            # Envía el nombre de usuario al servidor
            client.send(self.user_name.encode('utf-8'))

            # Crea hilo para conexiones entrantes
            receive_thread = threading.Thread(target = self.__receive_messages, args = (client,))
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
                self.all_messages.append(f'{self.user_name}: {message}')
                client.send(f'{self.user_name}: {message}'.encode('utf-8')) 
        except socket.error as e:
            print(f"Socket error: {e}")
        finally: 
            client.close()
            print('\nHistorial de mensajes:')
            for msg in self.all_messages:
                print(msg)
            # Termina el programa inmediatamente
            sys.exit(0) 

if __name__ == "__main__":
    Client = Client()
    Client.main()