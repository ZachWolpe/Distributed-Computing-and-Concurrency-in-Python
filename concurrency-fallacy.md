# Concurrency

```
: 08.11.23
: zach.wolpe@medibio.com.au
```

# The Concurrent Fallacy

After meticulously writing your concurrent Python algorithm, you're devastated to see it now runs slower than before. Why?
Concurrency in Python is easy to get wrong, and even when handled correctly the benefits are limited.

## 1. Concurrency is easy to implement, wrongly.

It's easy to set up multiprocessing, multithreading or asyncio in Python. The flow of execution can, however, quickly become unpredictable without careful attention to when: daemon threads/processes are launched; event loops are terminated; threads/processes are terminated & what remains in the cache/RAM.
It's very easy to leave dangling threads/processes - failing to shut down CPU processes and clean up RAM/CPU resource utility as you go.
Python developers are used to the garbage collector doing all the dirty work for them, and so it's easy to miss memory or CPU leakage. To worsen this, leakage is usually only visible on bigger workloads - which can be missed in dev/test environments (see point 5).


## 2. The GIL prevents Parallelism in Python.

CPython's Global Interpreter Lock (GIL) prevents any real parallelism. It is impossible to actually launch multiple threads in a single execution. Instead, threading is simulated by rapid context switching via time-sliced execution, performed by the interpreter (we have no authority over the timing of context switching).

## 3. Concurrency in Python only benefits from IO-bound workloads, not CPU-bound work.

Context switching isn't free. It requires stashing the state of an existing task and loading the state of the next.
Because of the limitations of parallelism enforced by the GIL, and the cost of context switching, it's very likely that CPU-bound algorithms will become slower after threading.

Only use threading or asynchronous programming on IO-bound workloads.

**CPU-Bound**

Attempting to use multithreading to speed up a CPU-bound workload will not speed up the runtime as the GIL prevents parallelism. The additional overhead of context switching renders the time-sliced execution slower than a single-threaded execution.

**I/O Bound**

If your workload is I/O-bound you will benefit from multithreading if implemented properly, however in this case it is recommended to instead use use use asyncio - providing the same performance benefit but with less complexity.


## 4. Thread-safety

Some resources are not thread-safe. This means that the resource is not safe to access from multiple threads at the same time. This is because the resource is not protected by a mutex. `print` or `list` to the console is an example of a not thread-safe resource, because they may be interrupted by another thread.

- A _race condition_ occurs when multiple threads are trying to access the same resource at the same time.
- A _lock_ can be used to protect a resource from being accessed by multiple threads at the same time.
- A _threading lock_ is a synchronization primitive that provides exclusive access to a shared resource in a multithreaded application. A thread lock is also known as a mutex which is short for mutual exclusion.
See [threading-5-lock.py].

## 4. Shared resources & order of operations matters

Multithreading/processing is dangerous if resources are shared/global or if the order of operations matters. Ensure to isolate fragments before writing concurrent code.

## 5. Monitoring and testing are more involved and easy to neglect.

Extensive testing & monitoring is required to catch leaks. As processes grow in complexity leaks and processes/thread runtimes can become opaque. Leakage can also creep up over time, a small amount of leakage compounds, which may avoid detection in dev/test but become apparent when demand scales in prod.


----
# Concurrency Implementation Tips

1. _*Favour async over multithreading*_. Predictable workloads can be explicitly managed with asynchronous programming. An IO-bound workload can benefit from threading, but it's simpler to use async.
2. _*Only use concurrency for IO-bound workloads*_: A single thread is favoured for CPU-bound workloads.
3. _*Write code horizontal scaling from the get-go*_. See below.
4. _*Ensure testing/staging matches production*_. If you implement multithreading/processing, ensure that the batch size and workload are rigorously tested to catch memory or CPU leaks. The throughput in prod can dwarf that in standard testing/dev environments. Use tools like docker stats to monitor runtime and possibly even write scripts to flag memory/CPU leakage.
5. _*"ThreadPoolExecutor" and "ProcessPoolExecutor" (futures)*_: It is recommended to use "ThreadPoolExecutor" or "ProcessPoolExecutor" instead of "threading.Thread" or "multiprocessing.Process" directly. This is because the ThreadPoolExecutor and ProcessPoolExecutor are higher-level abstractions that provide a simpler interface to multithreading and multiprocessing.
6. _*Fuzzing*_: It is recommended to use "fuzzing" during development/testing - adding random noise as time delays during execution. Dev/test/stage are often more stable, leading to falsely predictable results.
