"""
----------------------------------------------------------------------------------------------------
threading-4-join.py

Waiting for multiple threads to complete.

Use the `join` method to wait for a thread to complete.

: 07 Nov 23
: zach wolpe
: zach.wolpe@medibio.com.au
----------------------------------------------------------------------------------------------------
"""

import threading
import time

done = False


def worker(worker_ID):
    counter = 0
    while not done:
        time.sleep(1)
        counter += 1
        print(f"> worker {worker_ID}: {counter}")

t1 = threading.Thread(target=worker, daemon=True, args=("1"))
t2 = threading.Thread(target=worker, daemon=False, args=("2"))

t1.start()
t2.start()

# BLOCK: wait for the threads to complete. The interpreter does not pass this line until the threads are complete.
# The below code has no effect.
t1.join()
t2.join()

input("Press enter to quit thread...\n")
done = True



