import socket
import sys

VALID_ROLES = ("PUBLISHER", "SUBSCRIBER")


def startClient(server_ip, server_port, role):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        client_socket.send(role.encode("utf-8"))

        if role not in VALID_ROLES:
            print(f"[ERROR] Invalid role '{role}'. Must be 'PUBLISHER' or 'SUBSCRIBER'.")
            client_socket.close()
            return

        print(f"[CLIENT] Connected to server at {server_ip}:{server_port} as {role}.")

        if role == "PUBLISHER":
            handlePublisher(client_socket)
        elif role == "SUBSCRIBER":
            handleSubscriber(client_socket)

    except socket.error as e:
        print(f"[CLIENT ERROR] Could not connect: {e}")
    finally:
        client_socket.close()
        print("[CLIENT] Disconnected.")

#  PUBLISHER
def handlePublisher(client_socket):
    print("[PUBLISHER] You can now send messages. Type 'terminate' to exit.")
    try:
        while True:
            message = input(">> ")
            client_socket.send(message.encode("utf-8"))

            if message.strip().lower() == "terminate":
                print("[PUBLISHER] Termination sent. Disconnecting...")
                break
    except Exception as e:
        print(f"[PUBLISHER ERROR] {e}")

#  SUBSCRIBER 
def handleSubscriber(client_socket):
    print("[SUBSCRIBER] Waiting for messages from publishers...\n")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("[SUBSCRIBER] Server closed the connection.")
                break
            print(data.decode("utf-8"))
    except Exception as e:
        print(f"[SUBSCRIBER ERROR] {e}")

# main
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <SERVER_IP> <PORT> <ROLE>")
        print("Example: python client.py 127.0.0.1 5000 PUBLISHER")
        sys.exit()

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()

    startClient(server_ip, server_port, role)