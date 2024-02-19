import socket
import threading
import pickle

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, message):
        message_data = pickle.dumps(message)
        self.client_socket.sendall(message_data)

    def receive_messages(self):
        while True:
            try:
                message_data = self.client_socket.recv(4096)
                if message_data:
                    message = pickle.loads(message_data)
                    print(message)
            except Exception as e:
                print("Error receiving message:", e)
                break

def main():
    HOST = '127.0.0.1'
    PORT = 12345
    client = ChatClient(HOST, PORT)
    while True:
        message = input("Enter message: ")
        client.send_message(message)

if __name__ == "__main__":
    main()
