import socket
import pickle

def main():
    # Define host and port
    HOST = '127.0.0.1'
    PORT = 12345

    # Specify the file path of the file to be transferred
    file_path = "Q1/sample_file.txt"

    # Read file data
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return
    except Exception as e:
        print("Error occurred while reading the file:", e)
        return

    # Create socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to server
            client_socket.connect((HOST, PORT))

            # Pickle file object
            pickled_data = pickle.dumps(file_data)

            # Send pickled file object
            client_socket.sendall(pickled_data)
            print("File sent successfully.")
        except ConnectionRefusedError:
            print("Connection was refused. Make sure the server is running.")
        except Exception as e:
            print("Error occurred during file transfer:", e)

if __name__ == "__main__":
    main()
