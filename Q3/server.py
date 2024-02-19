import socket
import threading
import pickle

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.listen(5)
        print("Server is listening for incoming connections...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection established from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        with self.lock:
            self.clients.append(client_socket)
        while True:
            try:
                message_data = client_socket.recv(4096)
                if message_data:
                    message = pickle.loads(message_data)
                    print(f"Received message from {client_socket.getpeername()}: {message}")
                    self.broadcast(message, client_socket)
                else:
                    with self.lock:
                        self.clients.remove(client_socket)
                    client_socket.close()
                    break
            except Exception as e:
                print("Error handling client:", e)
                break

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client_socket in self.clients:
                if client_socket != sender_socket:
                    try:
                        message_data = pickle.dumps(message)
                        client_socket.sendall(message_data)
                    except Exception as e:
                        print("Error broadcasting message:", e)

def main():
    HOST = '127.0.0.1'
    PORT = 12345
    server = ChatServer(HOST, PORT)
    server.start()

if __name__ == "__main__":
    main()
