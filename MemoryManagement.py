# Unit-III Memory Management: Swapping, demand paging, hybrid memory management with swapping and demand paging.

import time
import random

# ========== CONFIGURABLE PARAMETERS ==========
MEMORY_SIZE = 5  # Number of available memory slots
PAGE_FRAME_SIZE = 3  # Number of frames for demand paging

# ========== Data Structures ==========
class Process:
    def __init__(self, pid, pages):
        self.pid = pid
        self.pages = pages  # List of page IDs
        self.loaded = False
        self.page_table = {}  # page_id -> in_memory (True/False)

    def __repr__(self):
        return f"P{self.pid}"

# ========== SWAPPING ==========

def simulate_swapping(processes):
    print("\n=== Swapping Simulation ===")
    memory = []
    for p in processes:
        if len(memory) >= MEMORY_SIZE:
            removed = memory.pop(0)
            removed.loaded = False
            print(f"Swapped OUT: {removed}")
        memory.append(p)
        p.loaded = True
        print(f"Swapped IN: {p}")
        time.sleep(1)

# ========== DEMAND PAGING ==========

def simulate_demand_paging(process):
    print("\n=== Demand Paging Simulation ===")
    memory_frames = []
    for page in process.pages:
        if page in memory_frames:
            print(f"[{process}] Page {page} HIT")
        else:
            if len(memory_frames) >= PAGE_FRAME_SIZE:
                removed = memory_frames.pop(0)
                print(f"[{process}] Page {page} FAULT - Removing Page {removed}")
            memory_frames.append(page)
            print(f"[{process}] Loading Page {page}")
        time.sleep(0.5)

# ========== HYBRID (Swapping + Paging) ==========

def simulate_hybrid(processes):
    print("\n=== Hybrid Simulation ===")
    memory = []

    for p in processes:
        if len(memory) >= MEMORY_SIZE:
            removed = memory.pop(0)
            removed.loaded = False
            print(f"Swapped OUT: {removed}")
        memory.append(p)
        p.loaded = True
        print(f"Swapped IN: {p}")
        time.sleep(1)

        # Now simulate demand paging for this swapped-in process
        simulate_demand_paging(p)

# ========== MAIN SIMULATION DRIVER ==========

if __name__ == "__main__":
    # Create sample processes with random pages
    processes = [
        Process(pid=1, pages=[1, 2, 3, 4]),
        Process(pid=2, pages=[2, 4, 6, 8]),
        Process(pid=3, pages=[5, 6, 7, 8]),
        Process(pid=4, pages=[3, 6, 9]),
        Process(pid=5, pages=[1, 5, 7])
    ]

    simulate_swapping(processes)
    simulate_demand_paging(processes[0])
    simulate_hybrid(processes)
