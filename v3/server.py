import socket
import threading
import sys

# Store connected clients and their roles
clients = {}  # {conn: ("PUBLISHER" or "SUBSCRIBER", addr)}

def handle_client(conn, addr):
    try:
        # First message from client should be its role
        role = conn.recv(1024).decode().strip().upper()

        if role not in ("PUBLISHER", "SUBSCRIBER"):
            conn.send("Invalid role. Use PUBLISHER or SUBSCRIBER.".encode())
            conn.close()
            return

        clients[conn] = (role, addr)
        print(f"[SERVER] {addr} connected as {role}")

        if role == "SUBSCRIBER":
            while True:
                try:
                    # Subscribers don't send anything; just keep them alive
                    data = conn.recv(1024)
                    if not data:
                        break
                except:
                    break
        else:  # role == "PUBLISHER"
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                print(f"[{role}] {addr}: {message}")
                if message.lower() == "terminate":
                    break
                # Send to all subscribers
                for c in list(clients):
                    if clients[c][0] == "SUBSCRIBER" and c != conn:
                        try:
                            c.send(f"[MESSAGE from {addr}]: {message}".encode())
                        except:
                            c.close()
                            del clients[c]

    except Exception as e:
        print(f"[ERROR] Client {addr} error: {e}")
    finally:
        print(f"[SERVER] {addr} disconnected.")
        if conn in clients:
            del clients[conn]
        conn.close()


def start_server(port):
    host = ''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(f"[ERROR] Bind failed: {e}")
        sys.exit()

    server_socket.listen(5)
    print(f"[SERVER] Listening on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit()

    port = int(sys.argv[1])
    start_server(port)