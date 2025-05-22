# Unit-IV File Management: Internal representation of files, buffer cache allocation of disk blocks,
mounting and unmounting of file systems, file systems maintenance.

import time
import random

# Simulated Disk & Cache
disk_blocks = [None] * 100  # Simulated disk with 100 blocks
buffer_cache = {}           # Simulated buffer cache

# ========== Internal File Representation (Inode-like) ==========

class File:
    file_id_counter = 1

    def __init__(self, name, size):
        self.id = File.file_id_counter
        File.file_id_counter += 1
        self.name = name
        self.size = size  # In blocks
        self.blocks = []
        self.create_inode()

    def create_inode(self):
        free_blocks = [i for i, block in enumerate(disk_blocks) if block is None]
        if len(free_blocks) < self.size:
            raise Exception("Not enough disk space")
        self.blocks = free_blocks[:self.size]
        for block in self.blocks:
            disk_blocks[block] = self.id

    def __repr__(self):
        return f"<File {self.name}, Blocks: {self.blocks}>"

# ========== Buffer Cache Simulation ==========

def read_file(file):
    print(f"\n[Buffer Cache] Reading file: {file.name}")
    for block in file.blocks:
        if block in buffer_cache:
            print(f"Cache HIT: Block {block}")
        else:
            print(f"Cache MISS: Block {block} - Loading into cache")
            buffer_cache[block] = disk_blocks[block]
        time.sleep(0.2)

def flush_cache():
    print("\n[Buffer Cache] Flushing cache to disk...")
    buffer_cache.clear()

# ========== Mounting & Unmounting File Systems ==========

mounted_filesystems = {}

def mount_fs(name):
    print(f"\n[Mount] Mounting filesystem: {name}")
    mounted_filesystems[name] = []

def unmount_fs(name):
    print(f"\n[Unmount] Unmounting filesystem: {name}")
    if name in mounted_filesystems:
        flush_cache()
        del mounted_filesystems[name]
    else:
        print(f"Filesystem {name} not found.")

# ========== File System Maintenance ==========

def fs_check():
    print("\n[FS Maintenance] Checking filesystem integrity...")
    used_blocks = set()
    errors = False

    for i, val in enumerate(disk_blocks):
        if val is not None:
            if i in used_blocks:
                print(f"Error: Block {i} is duplicated!")
                errors = True
            used_blocks.add(i)

    if not errors:
        print("Filesystem OK")
    else:
        print("Errors detected. Initiating repair...")

def fs_repair():
    print("[FS Maintenance] Releasing duplicate blocks...")
    block_count = {}
    for i, val in enumerate(disk_blocks):
        if val is not None:
            block_count[val] = block_count.get(val, 0) + 1
            if block_count[val] > 1:
                disk_blocks[i] = None
    print("Repair complete.")

# ========== MAIN DRIVER ==========

if __name__ == "__main__":
    mount_fs("rootfs")

    # Simulate creating files
    file1 = File("alpha.txt", 5)
    file2 = File("beta.txt", 3)
    mounted_filesystems["rootfs"].extend([file1, file2])

    print(f"\nCreated files: {mounted_filesystems['rootfs']}")

    # Simulate buffer cache read
    read_file(file1)
    read_file(file2)

    # Simulate maintenance
    fs_check()
    fs_repair()
    fs_check()

    # Unmount filesystem
    unmount_fs("rootfs")

    print("\nAll operations complete.")
