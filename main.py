import os
import subprocess
import threading
import multiprocessing
import queue
import time


def ipc_example():
    """
    Example of IPC using pipes
    """
    r, w = multiprocessing.Pipe()

    p = multiprocessing.Process(target=child_process, args=(w,))
    p.start()

    # Parent process
    print("Parent reading")
    print(r.recv())
    p.join()


def child_process(w):
    """
    The child process for the IPC example.
    """
    print("Child writing")
    w.send("IPC example message")
    w.close()


def execute_command_in_thread(command):
    """
    Execute a command in a separate thread
    """
    threading.Thread(target=run_command, args=(command,)).start()


def run_command(command):
    """
    Run a command
    """
    subprocess.Popen(command, shell=True)


def create_process(command):
    """
    Create a new process running the given command
    """
    if os.name == 'nt':  # Check if the OS is Windows
        command = command.replace('ls', 'dir')
    process = subprocess.Popen(command, shell=True)
    return process.pid


def list_processes():
    """
    List all running processes
    """
    command = "ps aux" if os.name != 'nt' else "tasklist"
    try:
        process = subprocess.Popen(command, shell=True)
    except Exception as e:
        print(f"An error occurred: {e}")


# Queue for IPC (Producer-Consumer example)
ipc_queue = queue.Queue()


def producer():
    """
    A producer function for the producer-consumer problem
    """
    for i in range(5):
        print(f"Producing item {i}")
        ipc_queue.put(i)
        time.sleep(1)


def consumer():
    """
    A consumer function for the producer-consumer problem
    """
    for i in range(5):
        item = ipc_queue.get()
        print(f"Consuming item {item}")
        time.sleep(2)


if __name__ == "__main__":
    # For the purpose of this example, I'm using the 'dir' command for Windows,
    # which lists directory contents (similar to 'ls' in UNIX).
    command = "dir" if os.name == 'nt' else "ls"

    pid = create_process(command)
    print(f"Created a new process with pid: {pid}")

    print("Listing processes:")
    list_processes()

    print("Executing command in a new thread:")
    execute_command_in_thread(command)

    # Call the IPC example:
    ipc_example()

    print("Producer-consumer example:")
    threading.Thread(target=producer).start()
    threading.Thread(target=consumer).start()

    # Wait for the threads to finish
    time.sleep(10)
    print("Done")
