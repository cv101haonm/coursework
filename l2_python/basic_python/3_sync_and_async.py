# Multiprocessing, Multithreading, and Asyncio in Python
import time
import multiprocessing
import threading
import asyncio


# 1. SEQUENTIAL (BASELINE)
print("=== SEQUENTIAL EXECUTION ===")

def cpu_task(n):
    """Simulate CPU-bound work"""
    result = sum(i * i for i in range(n))
    return result

def io_task(n):
    """Simulate I/O-bound work (e.g., API call, file read)"""
    time.sleep(1)  # Simulate waiting for I/O
    return f"Task {n} done"

# Sequential CPU tasks
start = time.time()
for i in range(4):
    cpu_task(1000000)
print(f"Sequential CPU tasks: {time.time() - start:.2f}s")

# Sequential I/O tasks
start = time.time()
for i in range(4):
    io_task(i)
print(f"Sequential I/O tasks: {time.time() - start:.2f}s")


# 2. MULTIPROCESSING (for CPU-bound tasks)
print("\n=== MULTIPROCESSING ===")

def worker(n, return_dict, key):
    """Worker function for multiprocessing"""
    result = cpu_task(n)
    return_dict[key] = result

# Run CPU tasks in parallel processes
start = time.time()
manager = multiprocessing.Manager()
return_dict = manager.dict()
processes = []

for i in range(4):
    p = multiprocessing.Process(target=worker, args=(1000000, return_dict, i))
    processes.append(p)
    p.start()

for p in processes:
    p.join()  # Wait for all processes to finish

print(f"Multiprocessing (4 cores): {time.time() - start:.2f}s")
print(f"Results: {len(return_dict)} tasks completed")


# 3. MULTITHREADING (for I/O-bound tasks)
print("\n=== MULTITHREADING ===")

def thread_worker(n, results, index):
    """Worker function for threading"""
    result = io_task(n)
    results[index] = result

# Run I/O tasks in parallel threads
start = time.time()
threads = []
results = [None] * 4

for i in range(4):
    t = threading.Thread(target=thread_worker, args=(i, results, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()  # Wait for all threads to finish

print(f"Multithreading: {time.time() - start:.2f}s")
print(f"Results: {results}")


# 4. ASYNCIO (for I/O-bound tasks - more efficient)
print("\n=== ASYNCIO ===")

async def async_io_task(n):
    """Async I/O task"""
    await asyncio.sleep(1)  # Non-blocking sleep
    return f"Async task {n} done"

async def main_async():
    """Run async tasks concurrently"""
    tasks = [async_io_task(i) for i in range(4)]
    results = await asyncio.gather(*tasks)
    return results

# Run async tasks
start = time.time()
results = asyncio.run(main_async())
print(f"Asyncio: {time.time() - start:.2f}s")
print(f"Results: {results}")


# 5. COMPARISON EXAMPLE: Download simulation
print("\n=== PRACTICAL EXAMPLE: Simulate Downloads ===")

def download_sync(url):
    """Simulate synchronous download"""
    time.sleep(2)
    return f"Downloaded {url}"

async def download_async(url):
    """Simulate asynchronous download"""
    await asyncio.sleep(2)
    return f"Downloaded {url}"

urls = ["url1.com", "url2.com", "url3.com"]

# Sequential
start = time.time()
for url in urls:
    download_sync(url)
print(f"Sequential downloads: {time.time() - start:.2f}s")

# Threading
start = time.time()
threads = []
for url in urls:
    t = threading.Thread(target=download_sync, args=(url,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
print(f"Threading downloads: {time.time() - start:.2f}s")

# Asyncio
async def download_all():
    tasks = [download_async(url) for url in urls]
    return await asyncio.gather(*tasks)

start = time.time()
asyncio.run(download_all())
print(f"Asyncio downloads: {time.time() - start:.2f}s")