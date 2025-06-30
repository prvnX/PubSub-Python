import socket
import sys

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
    except socket.error as e:
        print(f"Connection failed: {e}")
        sys.exit()

    print(f"[CLIENT] Connected to {server_ip}:{server_port}")
    print("Type messages to send to server. \n Type 'terminate' to end the connection.")

    while True:
        msg = input(">> ")
        client_socket.send(msg.encode("utf-8"))

        if msg.strip().lower() == "terminate":
            print("[CLIENT] Terminate command sent. Closing connection.")
            break

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <PORT>")
        sys.exit()

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    start_client(server_ip, server_port)