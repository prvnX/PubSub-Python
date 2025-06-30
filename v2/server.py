import socket
import sys
import signal
import time

def signal_handler(sig, frame):
    print("\n[SERVER] Signal received (Ctrl+C). Shutting down server...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def startServer(PORT):
    host = ''
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        serverSocket.bind((host, PORT))
    except socket.error as e:
        print(f"[ERROR] Failed to bind: {e}")
        sys.exit()

    serverSocket.listen(3)
    print(f"[SERVER] Listening on port {PORT}. Waiting for connections...")

    try:
        while True:
            conn, address = serverSocket.accept()
            print(f"[SERVER] Connection established with {address}")

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8").strip()
                print(f"[CLIENT]: {message}")

                if message.lower() == "terminate":
                    print("[SERVER] Termination command received. Closing connection.")
                    break
                    # for i in range(3, 0, -1):
                    #     conn.sendall(f"Terminating in {i}...\n".encode("utf-8"))
                    # break

            conn.close() #close connection with the current client 
            print(f"[SERVER] Connection with client {address} is closed.\n")

            for i in range(5, 0, -1):
                print(f"[SERVER] Next connection in {i} seconds...", end='\r')
                time.sleep(1)
                if(i == 1):
                    print("\n[SERVER] Ready for the next client connection.")

    except KeyboardInterrupt:
        print("\n[SERVER] KeyboardInterrupt detected. Shutting down...")

        

    finally:
        serverSocket.close()
        print("[SERVER] Socket is  closed. Server stopped.")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERROR] Usage: python server.py <PORT>\nExample: python server.py 8080")
        sys.exit(1)

    PORT = int(sys.argv[1])
    startServer(PORT)
