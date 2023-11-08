"""
----------------------------------------------------------------------------------------------------
threading-1-intro.py

Threading tutorial.

: 07 Nov 23
: zach wolpe
: zach.wolpe@medibio.com.au
----------------------------------------------------------------------------------------------------
"""

import threading
import time

done = False

def worker():
    counter = 0
    while not done:
        time.sleep(1)
        counter += 1
        print(f"counter: {counter}")

# Incorrect implementation:
    # without threading: execution starts here but cannot be reached because the main thread is blocked.
    # worker()
    # input("Press enter to quit...\n")
    # done = True

# Correct implementation:
# with threading: execution starts here
thread = threading.Thread(target=worker)

# start a worker function i a separate thread
thread.start()

input("Press enter to quit...\n")
done = True