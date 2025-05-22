# Unit-V Network and distributed operating systems: Network operating systems and applications, client server applications, advantages of network operating over standalone PC operating systems, distributed operating systems and distributed applications, advantages of distributed operating systems over centralized operating systems, remote procedure call, distributed file system. distributed clock synchronization, mutual exclusions

import socket
import threading
import time
import queue

# === 1. Client-Server Network Application ===

def start_server():
    def handle_client(client_socket):
        msg = client_socket.recv(1024).decode()
        print(f"[Server] Received: {msg}")
        client_socket.send("ACK from server".encode())
        client_socket.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8888))
    server.listen(1)
    print("[Server] Listening on port 8888")
    client, addr = server.accept()
    print(f"[Server] Connection from {addr}")
    handle_client(client)
    server.close()

def start_client():
    time.sleep(1)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8888))
    client.send("Hello Server!".encode())
    print(f"[Client] Server says: {client.recv(1024).decode()}")
    client.close()

# === 2. Remote Procedure Call (Simulated) ===

def rpc_add(a, b):
    return a + b

def simulate_rpc():
    print("\n[RPC] Client requesting remote addition (4 + 5)")
    result = rpc_add(4, 5)
    print(f"[RPC] Server responded with result: {result}")

# === 3. Distributed File System (Simulated) ===

distributed_fs = {}

def write_to_dfs(node, filename, content):
    distributed_fs[filename] = (node, content)
    print(f"[DFS] {node} wrote {filename}: {content}")

def read_from_dfs(filename):
    if filename in distributed_fs:
        node, content = distributed_fs[filename]
        print(f"[DFS] Read from {filename} by {node}: {content}")
    else:
        print(f"[DFS] File {filename} not found")

# === 4. Distributed Clock Sync (Lamport Clock) ===

class LamportClock:
    def __init__(self):
        self.clock = 0

    def tick(self):
        self.clock += 1

    def send_event(self):
        self.tick()
        return self.clock

    def receive_event(self, received_clock):
        self.clock = max(self.clock, received_clock) + 1

# === 5. Mutual Exclusion (Ricart-Agrawala-style Simulation) ===

request_queue = queue.Queue()
access_lock = threading.Lock()
clock = LamportClock()

def request_critical_section(process_id):
    clock.tick()
    timestamp = clock.clock
    print(f"[P{process_id}] Requesting critical section at time {timestamp}")
    request_queue.put((timestamp, process_id))
    time.sleep(1)  # simulate waiting
    enter_critical_section(process_id)

def enter_critical_section(process_id):
    with access_lock:
        print(f"[P{process_id}] Entering critical section")
        time.sleep(1)
        print(f"[P{process_id}] Leaving critical section")
        request_queue.get()

# === Main Simulation ===

if __name__ == "__main__":
    print("\n=== Network Client-Server Demo ===")
    t_server = threading.Thread(target=start_server)
    t_client = threading.Thread(target=start_client)
    t_server.start()
    t_client.start()
    t_server.join()
    t_client.join()

    print("\n=== Remote Procedure Call Demo ===")
    simulate_rpc()

    print("\n=== Distributed File System Demo ===")
    write_to_dfs("NodeA", "file1.txt", "Hello World")
    read_from_dfs("file1.txt")

    print("\n=== Distributed Clock Synchronization Demo ===")
    node1 = LamportClock()
    node2 = LamportClock()

    event1 = node1.send_event()
    print(f"[Node1] Sent event with clock {event1}")
    node2.receive_event(event1)
    print(f"[Node2] Updated clock to {node2.clock}")

    print("\n=== Distributed Mutual Exclusion Demo ===")
    p1 = threading.Thread(target=request_critical_section, args=(1,))
    p2 = threading.Thread(target=request_critical_section, args=(2,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("\nAll simulations complete.")
