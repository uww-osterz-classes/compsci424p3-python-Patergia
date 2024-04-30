import threading
import time

# Define a function that will be run in each thread
def print_numbers(thread_id):
    for i in range(5):
        print(f"Thread {thread_id}: {i}")
        time.sleep(1)  # Simulate some work being done

# Get the number of threads from the user
num_threads = int(input("Enter the number of threads to create: "))

# Create a list to hold thread objects
threads = []

# Create and start the threads based on user input
for i in range(num_threads):
    thread = threading.Thread(target=print_numbers, args=(i,))
    threads.append(thread)
    thread.start()

# Main thread continues running
for i in range(5):
    print(f"Main Thread: {i}")
    time.sleep(1)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("Main Thread Exiting")
