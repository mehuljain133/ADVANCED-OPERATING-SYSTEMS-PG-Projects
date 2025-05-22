# Unit-II Interprocess Communication and Synchronization: Interprocesss communication mechanisms, signals handling, network communication mechanisms, process synchronization in multiprocessor environment.

import multiprocessing
import signal
import os
import socket
import time

# ========== 1. Interprocess Communication (Pipe & Queue) ==========

def pipe_process(conn):
    msg = conn.recv()
    print(f"[Pipe Child] Received: {msg}")
    conn.send(f"ACK: {msg}")
    conn.close()

def queue_process(q):
    msg = q.get()
    print(f"[Queue Child] Got from Queue: {msg}")
    q.put(f"Processed: {msg}")

# ========== 2. Signal Handling ==========

def handle_signal(signum, frame):
    print(f"\n[Signal Handler] Caught signal: {signum}")
    print("Graceful shutdown...")

def setup_signal_handler():
    signal.signal(signal.SIGINT, handle_signal)
    print("[Signal Handler] Press Ctrl+C to trigger")

# ========== 3. Network Communication (Client-Server with socket) ==========

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 9999))
    s.listen(1)
    print("[Server] Waiting for connection...")
    conn, addr = s.accept()
    print(f"[Server] Connected to {addr}")
    data = conn.recv(1024).decode()
    print(f"[Server] Received: {data}")
    conn.send("Message received".encode())
    conn.close()
    s.close()

def client():
    time.sleep(1)  # Ensure server is ready
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    s.send("Hello from client!".encode())
    reply = s.recv(1024).decode()
    print(f"[Client] Server replied: {reply}")
    s.close()

# ========== 4. Process Synchronization ==========

def worker(lock, sema, name):
    with sema:
        with lock:
            print(f"[{name}] Entered critical section")
            time.sleep(1)
            print(f"[{name}] Exiting critical section")

# ========== Main Driver ==========

if __name__ == "__main__":
    print("=== IPC with Pipe ===")
    parent_conn, child_conn = multiprocessing.Pipe()
    p_pipe = multiprocessing.Process(target=pipe_process, args=(child_conn,))
    p_pipe.start()
    parent_conn.send("Hello via Pipe")
    print(f"[Main] Pipe Response: {parent_conn.recv()}")
    p_pipe.join()

    print("\n=== IPC with Queue ===")
    q = multiprocessing.Queue()
    p_queue = multiprocessing.Process(target=queue_process, args=(q,))
    q.put("Hello via Queue")
    p_queue.start()
    p_queue.join()
    print(f"[Main] Queue Response: {q.get()}")

    print("\n=== Signal Handling ===")
    setup_signal_handler()
    print("[Main] Waiting... Press Ctrl+C to test signal handler.")
    time.sleep(3)

    print("\n=== Network Communication ===")
    server_proc = multiprocessing.Process(target=server)
    client_proc = multiprocessing.Process(target=client)
    server_proc.start()
    client_proc.start()
    client_proc.join()
    server_proc.join()

    print("\n=== Process Synchronization (Lock & Semaphore) ===")
    lock = multiprocessing.Lock()
    semaphore = multiprocessing.Semaphore(2)  # Max 2 can access at once

    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(lock, semaphore, f"Worker-{i+1}"))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("\nAll operations complete.")
