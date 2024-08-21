import socket
import threading

def receive_messages(client_socket):
    """Receive and print messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received: {message.decode('utf-8')}")
            else:
                break
        except:
            break

def main():
    user_name = input('<<< Ingrese su nombre de usuario:')


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 10000))

    # Start a thread to listen for incoming messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input("You: ")
        client.send(f'{user_name}: {message}'.encode('utf-8'))
    
    client.close()

if __name__ == "__main__":
    main()
main()