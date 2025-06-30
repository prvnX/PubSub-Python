import socket
import sys
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[INFO] Connection closed by server.")
                break
            print(data.decode())
        except:
            print("[ERROR] Lost connection.")
            break

if len(sys.argv) != 4:
    print("Usage: python client.py <SERVER_IP> <PORT> <ROLE>")
    sys.exit()

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
role = sys.argv[3].upper()

if role not in ["PUBLISHER", "SUBSCRIBER"]:
    print("Role must be either PUBLISHER or SUBSCRIBER")
    sys.exit()

# Create TCP socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Send the role to server
client_socket.send(role.encode())

# Behavior based on role
if role == "PUBLISHER":
    print("[CLIENT] You are a Publisher. Type messages to send. Type 'terminate' to quit.")
    while True:
        message = input()
        client_socket.send(message.encode())
        if message.lower() == "terminate":
            break
    client_socket.close()

elif role == "SUBSCRIBER":
    print("[CLIENT] You are a Subscriber. Waiting for messages...")
    receive_messages(client_socket)
    client_socket.close()