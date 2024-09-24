import socket

def define_client() -> socket:
   '''Define the client socket.'''
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   return client

def connect_to_server(client: socket, server_address: tuple) -> None:
   '''Connect to the server.'''
   try:
      client.connect(server_address)
      print('Conectado al servidor.')
   except socket.error as e:
      print(f"No se pudo conectar al servidor: { e }")
      return e

def receive_messages(client_socket: socket.socket):
   '''Receive and print messages from the server.'''
   while True:
      try:
         message = client_socket.recv(1024)
         if message:
            print(f"Received: { message.decode('utf-8') }")
         else:
            print('Conexión cerrada por el servidor.')
            break
      except socket.error as e:
         print(f"Error recibiendo mensaje: {e}")
         break
      
def handle_user_messages(client: socket, user_name: str) -> None:
   '''Handle the messages from the user.'''
   while True:
      message = input('You: ')
      if message.lower() == 'exit': 
         print('Desconectando...')
         break
      try:
         client.send(f'{user_name}: {message}'.encode('utf-8'))
      except socket.error as e:
         print(f"Error enviando mensaje: {e}")
         break
   client.close()
   print('Conexión cerrada.')
    
