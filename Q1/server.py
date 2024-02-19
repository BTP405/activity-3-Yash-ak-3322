import socket
import pickle
import os

def save_file(file_data, save_path):
    with open(save_path, 'wb') as f:
        f.write(file_data)
    print(f"File saved to {save_path}")

def main():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345

    # Specify the directory to save the received file
    save_directory = "./received_files/"

    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Create socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind socket to address
        server_socket.bind((HOST, PORT))
        
        # Listen for incoming connections
        server_socket.listen(1)
        print("Server is listening for incoming connections...")

        # Accept connection
        conn, addr = server_socket.accept()
        print(f"Connection established from {addr}")

        with conn:
            # Receive pickled file object
            file_data = conn.recv(4096)
            if not file_data:
                print("No data received")
                return
            
            # Unpickle file object
            try:
                file_obj = pickle.loads(file_data)
                # Specify the file name
                file_name = "received_file.txt"
                save_path = os.path.join(save_directory, file_name)
                save_file(file_obj, save_path)
            except pickle.UnpicklingError as e:
                print("Error unpickling the file object:", e)
            except Exception as e:
                print("Error occurred while saving the file:", e)

if __name__ == "__main__":
    main()
