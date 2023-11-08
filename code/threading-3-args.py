"""
----------------------------------------------------------------------------------------------------
threading-3-args.py

Passing arguments to a thread.

Arguments are passed to the thread function via the `args` keyword argument.

Note:
    - There can be multiple daemon threads.

: 07 Nov 23
: zach wolpe
: zach.wolpe@medibio.com.au
----------------------------------------------------------------------------------------------------
"""

import threading
import time

done = False

def worker(name, arg2):
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        print(f"{name}/{arg2}: {counter}")

thread = threading.Thread(target=worker, daemon=True, args=("thread-1-arg-1","arg2"))
thread.start()

input("Press enter to quit thread...\n")
done = True
