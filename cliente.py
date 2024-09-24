import socket
import threading

def receive_messages(client_socket: socket.socket):
    '''Receive and print messages from the server.'''
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received: {message.decode('utf-8')}")
            else:
                print("Conexión cerrada por el servidor.")
                break
        except socket.error as e:
            print(f"Error recibiendo mensaje: {e}")
            break
        
def define_client() -> socket:
    '''Define the client socket.'''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client

def handle_user_messages(client: socket, user_name: str) -> None:
    '''Handle the messages from the user.'''
    while True:
        message = input("You: ")
        if message.lower() == 'exit': 
            print("Desconectando...")
            break
        try:
            client.send(f'{user_name}: {message}'.encode('utf-8'))
        except socket.error as e:
            print(f"Error enviando mensaje: {e}")
            break
    client.close()
    print("Conexión cerrada.")
    
def main():
    try:
        user_name = input('<<< Ingrese su nombre de usuario: ')

        client = define_client()

        # Intentar conectar al servidor
        try:
            client.connect(("127.0.0.1", 10000))
            print("Conectado al servidor.")
        except socket.error as e:
            print(f"No se pudo conectar al servidor: { e }")
            return e

        # Start a thread to listen for incoming messages
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        handle_user_messages(client, user_name)

    except KeyboardInterrupt:
        print("\nDesconexión por el usuario.")
        try:
            client.close()
        except socket.error:
            pass

if __name__ == "__main__":
    main()
