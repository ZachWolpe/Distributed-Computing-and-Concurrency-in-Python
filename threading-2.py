"""
---------------------------------------------------------------
threading-2.py

Using a `daemon` thread.

The core of the program is the main thread. The daemon thread is just a helper thread that runs in the background.

Note:
    - The use of `daemon=True` terminates the thread when the main thread terminates.
    - Despite the fact that the `while True` loop is infinite, the thread will terminate when the main thread terminates.

: 07 Nov 23
: zach wolpe
: zach.wolpe@medibio.com.au
---------------------------------------------------------------
"""

import threading
import time

def worker():
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        print(f"counter: {counter}")

threading.Thread(target=worker, daemon=True).start()

input("Press enter to quit...\n")
