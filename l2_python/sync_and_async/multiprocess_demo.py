import multiprocessing
import os

# Define a simple worker function that will run in each process
def worker(name):
    print(f"Worker {name} running in PID {os.getpid()}")


if __name__ == "__main__":
    processes = []

    for i in range(4):
        # Create a new process that runs the worker function with a unique name
        p = multiprocessing.Process(target=worker, args=(i,))
        # Add the process to the list and start it
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    print("All workers done.")
