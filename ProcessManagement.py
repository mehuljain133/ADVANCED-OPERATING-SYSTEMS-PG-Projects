# Unit-I Process Management: System calls for process creation and termination, invoking other programs, changing size of a process, process scheduling schemes, time, clock, multi-threading.

import multiprocessing
import threading
import subprocess
import time
import os
import psutil  # For getting process info (optional, you may need to install this with pip)

# 1. Process creation and termination
def child_process(name, duration):
    print(f"Process {name} with PID {os.getpid()} started")
    time.sleep(duration)
    print(f"Process {name} with PID {os.getpid()} terminated")

def create_process(name, duration):
    p = multiprocessing.Process(target=child_process, args=(name, duration))
    p.start()
    return p

# 2. Invoking other programs
def invoke_other_program():
    print("Invoking system command: 'ls' or 'dir'")
    if os.name == 'nt':
        result = subprocess.run(['dir'], shell=True, capture_output=True, text=True)
    else:
        result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
    print(result.stdout)

# 3. Changing size of a process (simulated by allocating memory)
def simulate_process_size_change(size_in_mb):
    print(f"Simulating allocation of {size_in_mb}MB memory")
    mem_block = bytearray(size_in_mb * 1024 * 1024)
    print(f"Allocated memory block size: {len(mem_block) / (1024*1024)} MB")
    time.sleep(2)
    del mem_block
    print("Memory block released")

# 4. Process Scheduling Schemes (Round Robin simulation)
def round_robin_scheduler(tasks, time_slice):
    print("\nStarting Round Robin Scheduling Simulation")
    queue = tasks[:]
    while queue:
        task = queue.pop(0)
        print(f"Running task: {task['name']} for {time_slice} seconds")
        time.sleep(time_slice)
        task['remaining'] -= time_slice
        if task['remaining'] > 0:
            print(f"Task {task['name']} remaining time: {task['remaining']}")
            queue.append(task)
        else:
            print(f"Task {task['name']} completed")

# 5. Time and Clock usage
def print_time_clock():
    print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Process CPU time used: {time.process_time()} seconds")

# 6. Multithreading example
def thread_function(name, duration):
    print(f"Thread {name} started")
    time.sleep(duration)
    print(f"Thread {name} finished")

def run_threads():
    threads = []
    for i in range(3):
        t = threading.Thread(target=thread_function, args=(f"T{i+1}", 2))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    print("=== Process Creation and Termination ===")
    p1 = create_process("P1", 3)
    p2 = create_process("P2", 5)

    print("=== Invoking Other Program ===")
    invoke_other_program()

    print("=== Simulate Process Size Change ===")
    simulate_process_size_change(10)  # 10 MB

    print("=== Process Scheduling Scheme: Round Robin ===")
    tasks = [
        {'name': 'Task1', 'remaining': 5},
        {'name': 'Task2', 'remaining': 7},
        {'name': 'Task3', 'remaining': 3}
    ]
    round_robin_scheduler(tasks, time_slice=2)

    print("=== Time and Clock ===")
    print_time_clock()

    print("=== Multi-threading Example ===")
    run_threads()

    # Wait for process to finish before exiting main
    p1.join()
    p2.join()

    print("All processes and threads have finished.")
