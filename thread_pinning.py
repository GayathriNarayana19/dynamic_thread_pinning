import os
import subprocess
import random

def get_threads_for_pid(pid):
    try:
        result = subprocess.run(
            ["ps", "-T", "-p", pid, "-o", "tid,comm"],
            capture_output=True,
            text=True
        )
        thread_list = []
        for line in result.stdout.splitlines()[1:]:  # Skip header line
            parts = line.split()
            if len(parts) >= 2:
                tid, name = parts[0], parts[1]
                thread_list.append((tid, name))
        return thread_list
    except Exception as e:
        print(f"Error fetching threads for PID {pid}: {e}")
        return []

def assign_taskset(threads, pinned_cores, floating_cores):
    """Assigns threads to pinned or floating CPU cores using taskset."""
    pinned_core_list = pinned_cores.split(',')
    floating_core_list = floating_cores.split(',')

    pinned_index = 0

    for tid, name in threads:
        if name in selected_thread_types:
            # Assign pinned cores in round-robin fashion
            core = pinned_core_list[pinned_index]
            pinned_index = (pinned_index + 1) % len(pinned_core_list)
        else:
            # Assign floating cores randomly
            core = random.choice(floating_core_list)

        print(f"Assigning TID {tid} ({name}) to core(s) {core}")
        os.system(f"sudo taskset -cp {core} {tid}")

if __name__ == "__main__":
    print("Dynamic CPU Pinning Script")

    # Get user input for main process ID
    pid = input("Enter the main process ID (PID) to control: ").strip()

    # Get all threads for the given PID
    threads = get_threads_for_pid(pid)
    if not threads:
        print("No matching threads found. Exiting.")
        exit()

    # Get specific thread types to pin
    selected_thread_types = input("Enter thread names to pin (comma-separated, e.g., worker1,worker2): ").strip().split(',')

    # Get user input for pinned and floating cores
    pinned_cores = input("Enter cores for selected threads (e.g., 2,3,4): ").strip()
    floating_cores = input("Enter cores for floating threads (e.g., 5,6): ").strip()

    # Apply taskset to threads
    assign_taskset(threads, pinned_cores, floating_cores)

