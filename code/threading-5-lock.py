"""
----------------------------------------------------------------------------------------------------
threading-5-lock.py

A `lock` can be used to synchronize access to a shared resource.

Follow:
    1. Instantiate a `lock()`.
    2. Use `lock.acquire()` to acquire the lock.
    3. Use `lock.release()` to release the lock.

Alternatively:
    1. Use a `with` statement to acquire and release a lock automatically.

: 07 Nov 23
: zach wolpe
: zach.wolpe@medibio.com.au
----------------------------------------------------------------------------------------------------
"""

import threading
import time


# example 1: unstable counter ------------------------------------>>
counter = 0

def increase(by):
    global counter

    local_counter = counter
    local_counter += by

    time.sleep(0.1)

    counter = local_counter
    print(f'counter={counter}')


# create threads
t1 = threading.Thread(target=increase, args=(10,))
t2 = threading.Thread(target=increase, args=(20,))

# start the threads
t1.start()
t2.start()


# wait for the threads to complete
t1.join()
t2.join()


print(f'The final counter is {counter}')
# example 1: unstable counter ------------------------------------>>



# example 2: stable counter (lock) ------------------------------->>
counter = 0

def increase(by, lock):
    global counter
    lock.acquire()

    local_counter = counter
    local_counter += by

    time.sleep(0.1)

    counter = local_counter
    print(f'counter={counter}')
    lock.release()

# init lock
lock = threading.Lock()

# create threads
t1 = threading.Thread(target=increase, args=(10, lock))
t2 = threading.Thread(target=increase, args=(20, lock))

# start the threads
t1.start()
t2.start()


# wait for the threads to complete
t1.join()
t2.join()


print(f'The final counter is {counter}')
# example 2: stable counter (lock) ------------------------------->>



# example 3: stable counter (lock using `with`) ------------------>>
counter = 0

def increase(by, lock):
    global counter
    with lock:
        local_counter = counter
        local_counter += by

        time.sleep(0.1)

        counter = local_counter
        print(f'counter={counter}')

# init lock
lock = threading.Lock()

# create threads
t1 = threading.Thread(target=increase, args=(10, lock))
t2 = threading.Thread(target=increase, args=(20, lock))

# start the threads
t1.start()
t2.start()


# wait for the threads to complete
t1.join()
t2.join()


print(f'The final counter is {counter}')
# example 3: stable counter (lock using `with`) ------------------>>
