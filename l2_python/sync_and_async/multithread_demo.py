import threading

# Define a simple worker function that will run in each thread
def worker(name):
    print(f"Worker {name} running in thread {threading.current_thread().name}")


threads = []

for i in range(4):
    # Create a new thread that runs the worker function with a unique name
    t = threading.Thread(target=worker, args=(i,))
    # Add the thread to the list and start it
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("All workers done.")
