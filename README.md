
# Pub/Sub Middleware System – Client-Server Socket Application

## 🎯 Objective
This project implements a simple **Publish/Subscribe (Pub/Sub)** middleware architecture using **Python Socket Programming**, simulating real-time communication between multiple clients (Publishers and Subscribers) via a server.

---

## 🧩 Architecture
The system follows a **Client-Server** model:

- `server.py`: Manages all incoming client connections and routes messages from publishers to subscribers.
- `client.py`: Acts as either a publisher or subscriber based on user input, connecting to the server via TCP.

---

## 🧪 Versions & Features

### ✅ **Version 1 (v1)** – Basic Client-Server Communication
- A single client connects to the server.
- Any message typed in the client is displayed on the server terminal.
- Server runs until interrupted.
- Client disconnects when `terminate` is typed.

➡️ *One-to-one communication only.*

---

### ✅ **Version 2 (v2)** – Multi-Client Pub/Sub System
- Server supports **multiple concurrent clients** using **threads**.
- Clients act as either:
  - `PUBLISHER`: Can send messages.
  - `SUBSCRIBER`: Receives messages from publishers.
- Messages from publishers are **broadcast to all subscribers**.
- Publishers do **not** see messages from other publishers.

➡️ *Threading added for concurrency. Basic role-based communication.*

---

### ✅ **Version 3 (v3 - Final)** – Topic-Based Pub/Sub System
- Adds **topic filtering**: Messages are delivered **only to subscribers of the same topic**.
- Thread-safe architecture using Python’s **threading.Lock** and **ThreadPoolExecutor**.

➡️ *Robust, scalable pub/sub system with efficient topic-based routing.*

---

## 🖥️ Usage

### 🔧 Server

```bash
python server.py <PORT>
```

Example:
```bash
python server.py 5000
```

### 🔧 Client

```bash
python client.py <SERVER_IP> <PORT> <ROLE> <TOPIC>
```

Examples:
```bash
python client.py 127.0.0.1 5000 PUBLISHER SPORTS
python client.py 127.0.0.1 5000 SUBSCRIBER SPORTS
```

---

## 🛠 Requirements

- Python 3.6+
- No external libraries needed. Uses standard libraries:
  - `socket`
  - `threading`
  - `sys`
  - `signal`
  - `collections`
  - `concurrent.futures`

---

---

## 📁 Folder Structure (Submission Guideline)
```
/pubsub-assignment/
│
├── v1/
│   ├── server.py
│   └── client.py
│
├── v2/
│   ├── server.py
│   └── client.py
│
├── v3/
│   ├── server.py
│   └── client.py

```

---

## 📝 Notes

- Clients can be tested locally with `localhost` or across machines on the same local network.
- Ensure proper port forwarding and firewall settings for cross-device testing.

---
