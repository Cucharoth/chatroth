from cliente import define_client, connect_to_server, receive_messages, handle_user_messages
import threading
    
def main():
   try:
      user_name = input('<<< Ingrese su nombre de usuario: ')
      client = define_client()

      # Intentar conectar al servidor
      connect_to_server(client, (('127.0.0.1', 10000)))
      
      # Start a thread to listen for incoming messages
      receive_thread = threading.Thread(target=receive_messages, args=(client,))
      receive_thread.start()

      handle_user_messages(client, user_name)

   except KeyboardInterrupt:
      print("\nDesconexión por el usuario.")
      client.close()
 

if __name__ == "__main__":
   main()
