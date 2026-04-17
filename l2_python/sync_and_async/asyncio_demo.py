import asyncio

# Define a simple async worker function that simulates some work with asyncio.sleep
async def worker(name):
    print(f"Worker {name} started")
    await asyncio.sleep(1)
    print(f"Worker {name} done")


async def main():
    # Create multiple tasks to run concurrently
    tasks = [asyncio.create_task(worker(i)) for i in range(4)]
    await asyncio.gather(*tasks)
    print("All workers done.")

# Run the main function using asyncio
asyncio.run(main())
