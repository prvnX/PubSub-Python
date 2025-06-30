import socket
import sys
import signal
import threading
from concurrent.futures import ThreadPoolExecutor

roles = ("PUBLISHER", "SUBSCRIBER")
clients = {}  
lock = threading.Lock()  # ensuring thread safe 
threadPoolExec = ThreadPoolExecutor(max_workers=10)  # thread pool for sending messages

def signal_handler(sig, frame):
    print("\n[SERVER] Signal received (Ctrl+C). Shutting down server...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def sendMessage(clientConn, message, address, topic):
    try:
        clientConn.send(f"[PUBLISHER] {address} - {topic}: {message}".encode("utf-8"))
    except Exception as e:
        print(f"[SERVER] Failed to send to subscriber {address}: {e}")
        clientConn.close()
        with lock:
            if clientConn in clients:
                del clients[clientConn]

def handleClient(conn, address):
    try:
        # initial recieve role , topic
        data = conn.recv(1024).decode("utf-8").strip()
        try:
            role, topic = data.split()
            role = role.upper()
            topic = topic.upper()
        except ValueError:
            conn.send("[ERROR] Please send role and topic separated by space.".encode("utf-8"))
            conn.close()
            return

        if role not in roles:
            print(f"[SERVER] Invalid role '{role}' from {address}. Closing connection.")
            conn.send("[ERROR] Invalid role. Use PUBLISHER or SUBSCRIBER.".encode("utf-8"))
            conn.close()
            return

        with lock:
            clients[conn] = (role, address, topic)

        print(f"[SERVER] {role} connected from {address} on topic {topic}.")

        if role == "PUBLISHER":
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"[SERVER] Publisher {address} disconnected.")
                    break

                message = data.decode("utf-8").strip()
                print(f"[PUBLISHER] {address} - {topic}: {message}")

                if message.lower() == "terminate":
                    print(f"[SERVER] Terminate received from {address}.")
                    break

                with lock:
                    for c in list(clients):
                        c_role, c_addr, c_topic = clients[c]
                        if c_role == "SUBSCRIBER" and c != conn and c_topic == topic:
                            threadPoolExec.submit(sendMessage, c, message, address, topic)
        else:  # SUBSCRIBER
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print(f"[SERVER] Subscriber {address} disconnected.")
                        break
                except:
                    break

    except Exception as e:
        print(f"[ERROR] Client {address} error: {e}")
    finally:
        with lock:
            if conn in clients:
                del clients[conn]
        conn.close()
        print(f"[SERVER] Connection with {address} closed.")

def startServer(PORT):
    host = ''
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        serverSocket.bind((host, PORT))
    except socket.error as e:
        print(f"[ERROR] Failed to bind: {e}")
        sys.exit()

    serverSocket.listen(10)
    print(f"[SERVER] Listening on port {PORT}...")

    try:
        while True:
            conn, address = serverSocket.accept()
            thread = threading.Thread(target=handleClient, args=(conn, address))
            thread.start()
    except KeyboardInterrupt:
        print("\n[SERVER] KeyboardInterrupt detected. Shutting down...")
    finally:
        serverSocket.close()
        print("[SERVER] Server socket closed.")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit()

    PORT = int(sys.argv[1])
    startServer(PORT)