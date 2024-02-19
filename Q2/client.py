import socket
import pickle
from task_functions import task_multiply

def send_task(task, args, worker_addresses):
    results = []
    for address in worker_addresses:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)  # Set timeout for connection
                client_socket.connect(address)
                task_data = pickle.dumps((task, args))
                client_socket.sendall(task_data)
                response = client_socket.recv(4096)
                if response:
                    result = pickle.loads(response)
                    results.append(result)
                else:
                    print(f"No response received from {address}")
        except socket.timeout:
            print(f"Connection to {address} timed out.")
        except ConnectionRefusedError:
            print(f"Connection to {address} refused.")
    return results

def main():
    # Define worker node addresses
    worker_addresses = [('127.0.0.1', 12346), ('127.0.0.1', 12347)]  # Add more worker addresses if needed

    # Define task
    args = (5, 10)

    # Send task to worker nodes
    results = send_task(task_multiply, args, worker_addresses)
    print("Results:", results)

if __name__ == "__main__":
    main()
