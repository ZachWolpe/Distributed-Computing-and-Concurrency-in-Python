# Concurrency

_*Concurrency*_ is the ability of a program to be broken into parts that can run independently of each other. This is different from _*parallelism*_, which is the ability of a program to run multiple tasks at the same time.

The objective is to speed up runtime by running multiple independent `tasks`/`fragments` at the same time. This is useful for `CPU bound` tasks (processing a large amount of data).


----
## Parallelism

Paraellel execution runs multiple fragments simultaneously - each using a different CPU core.

----
# Time-Sliced Execution (Interleaving)

A single CPU core is used to run multiple fragments of code. The CPU switches between fragments, giving the illusion of parallelism.

## Context Switching

During time-sliced execution, the CPU switches between fragments of code. It is therefor necessary for the interpreter to keep track of the `state` of each fragment's execution.

This is called _*context switching*_. Context switching is expensive, it requires saving the state of the current fragment and loading the state of the next fragment.

It is best to minimize the number of context switches. The cost often outweighs the benefits of `threading` due to this context switching. 


----
# Processes

Think of a process as an executing program. A process has its own memory space, and is isolated from other processes. Processes are managed by the operating system.

Processes may run concurrency:
    - parallel
    - time-sliced (interleaved)

Each process runs `independently`: the memory is not shared between processes.

Each process has $3$ possible states:
    - _running_: has access to the CPU and is executing code.
    - _ready_: could run, but is waiting access to the CPU.
    - _blocked_: is waiting for something to happen (e.g. I/O operation).

## Threads

A `thread` is a sequence of instructions that can be executed independently of other code. Threads are managed by the operating system. Each `process` is executed using one or more threads. 

Concurrent code can be executed using multiple threads:
    - multithreaded process
    - single-threaded process

Unlike processes, threads have access to shared resources in the process.

## Schedualing

OS has a piece of software called a `scheduler` that decides which thread to run next. The scheduler can switch between threads at any time. This is called `preemptive multitasking`.


*NB* The schedualer decides which thread to run next, not the order in which the threads are executed. The order of execution is not guaranteed.

`preemptive multitasking`: when the scheduler performs a context switch, we say it _preempts_ the thread. Hence _preemtive multitasking_.

----
# Python GIL: Global Interpreter Lock

CPython has no true parellelism due to the `Global Interpreter Lock (GIL)`. The GIL is a mutex that prevents multiple threads from executing Python bytecodes at once. This lock is necessary mainly because CPython's memory management is not thread-safe. However, the GIL is always released when doing I/O operations, so this is where concurrency can be useful.

CPython is only capable of interleaved/time-sliced execution of multiple threads.

- No parallelism.
- Cannot take advantage of multple CPUs/cores.


## Cooperative Multitasking

Preemptive multitasking requires great care when using shared resources. Cooperative multitasking is a form of multitasking where each task must explicitly give up control to let other tasks run. This is also called `non-preemptive multitasking`.

- The GIL is a form of cooperative multitasking.
- The GIL is released when doing I/O operations.

Examples of I/O operations:
    - reading/writing files
    - making network requests
    - API requests
    - database operations
    - etc.

Non-preemptive multitasking is useful for `I/O bound` tasks, (reading a file or making network requests). This is *_NOT_* useful for `CPU bound` tasks (processing a large amount of data).


----
# Workloads

Characterize workloads as either `CPU bound` or `I/O bound`.

- `CPU bound`: the program is bottlenecked by the speed of the CPU. The program is doing a large amount of computation.
- `I/O bound`: the program is bottlenecked by the speed of the I/O subsystem. The program is waiting for input/output to complete.

### CPU Bound Workloads in Python

#### Threading

IF the workload can be written into concurrent fragments. Running the fragments in parallel will speed up the runtime. 

Issue: the `GIL` prevents parallelism. The fragments will be run in time-sliced execution. This will (often) not speed up the runtime.

The additonal overhead of context switching renders the time-sliced execution slower than a single-threaded execution.

#### Multiprocessing

Python can be sped up CPU bound loads by using multiple processes.

- Process are independent: states is not shared.
- The same workload is run in pseudo-parallel on multiple processes, but on the finite number of CPU cores.

### I/O Bound Workloads in Python

- CPython is inherently single-threaded.
- For IO bound workloads running code concurrently makes sense, as most of the time is spent waiting for an I/O operation to return sometihing, even if a single thread.

Warnings:
    - Writing multithreaded code is hard.
        - preemptive: we don't know exactly when a thread will be interrupted. Be particularly careful with `shared state`.

----
# Best Practise

In modern computing, scaling limited to a single machine is often insufficient.

It is therefore better to use a `distributed system` to scale the workload across multiple machines.


----
## AsyncIO

Execute a single thread but switch between tasks (_cooperative multitasking_). If one task (function) is waiting for something to happen, the thread can switch to another task (function) and continue working in the interim.

The context switching is `explicit`


#### Asyncronous Programming

Asyncronous programming is not multithreading or multiprocessing. It is a single thread that can switch between tasks. This is called _*cooperative multitasking*_.


#### Objective

Asyncronous programming uses a single thread to switch between tasks (_cooperative multitasking_). If one task (function) is waiting for something to happen, the thread can switch to another task (function) and continue working in the interim.

#### Use Cases

Useful for `I/O bound` tasks, (reading a file or making network requests). This is *_NOT_* useful for `CPU bound` tasks (processing a large amount of data).


Keywords: {`asyncio`,`async`,`await`,`yield`}


#### Python AsyncIO

- Easier and safter than multithreading.
- No need to worry about shared state.
- Both async and multithreading are inherently single-threaded (GIL).
- Safter than preemptive multitasking, but adds complexity to the code.

`NB: 3rd party I/O libraries may not be asyncronous.`

*Asyncronous libraries:*


#### Python Execution

    - Calls to async enabled functions are called `tasks` or `coroutines`.
    - We end up with a collection of tasks that are executed by the `event loop`. (The event loop is a single thread).
    - When a task runs it executes code, at some point it should yield control back ot the event loop.
    - The event loop then decides which task to run next.
    - Tasks that do not yield control will block the event loop, and are thus called `blocking` tasks.
    - To get the most out of asyncronous programming, we need to yield control when performing I/O operations.

*Asyncronous libraries:*

Blocking libraries can be replaced with non-blocking alternatives. 

Replace:
    - `psychopg2`   with `asyncpg` (PostgreSQL)
    - `requests`    with `aiohttp`
    - `queue.Queue` with `asyncio.Queue`
    - `redis-py`    with `aioredis`


----
# Summary

1. Multiprocessing
    - no shared data.
    - passing data between processes is expensive.
    - useful for CPU bound workloads.

2. Multithreading
    - shared data.
    - cared need for shared data (order of operations).
    - preemtive multitasking, OS decides when to switch between threads.
    - Useful for performance improvements in I/O bound workloads.
    - Useful for other multitasking use cases that have nothing to do with performance improvements, or when needing concurrency with blocking code.

3. Async
    - shared data.
    - care needed for shared data (order of operations).
    - cooperative multitasking, programmer decides when to switch between tasks.
    - Useful for performance improvements in I/O bound workloads, but requires I/O code to be async aware (use async libraries).



----
# Python Threading: Issues & Caveats

The GIL prevents parallelism. The fragments will be run in time-sliced execution. 

*CPU Bound*

Attempting to use multithreading to speed up a CPU bound workload will not speed up the runtime as the GIL prevents parallelism. The additional overhead of context switching renders the time-sliced execution slower than a single-threaded execution.

*I/O Bound*

If your workload is `I/O bound` you will benefit from multithreading if implemented properly, however in this case it is recommended to instead use use use `asyncio` - providing the same performance benefit but with less complexity.
 

*Thread-safe*

Some resources are not thread-safe. This means that the resource is not safe to access from multiple threads at the same time. This is because the resource is not protected by a mutex. `print` or `list` to the console is an example of a not thread-safe resource, because they may be interupted by another thread.


#### Example

```python
import asyncio

# example 1: without return value ------------------------------->>
async def base_func_1():
    print('hello')
    # await asyncio.sleep(1) # blocking call
    await function_1()
    print('world!')

async def function_1():
    print('>> function_1 started...')
    await asyncio.sleep(2)
    print('>> function_1 terminated.')

asyncio.run(base_func_1())
print('\n\n')
# example 1: without return value ------------------------------->>


# example 2: with return value(s) ------------------------------->>
async def base_func_2():
    task = asyncio.create_task(function_2())
    print('hello')
    await asyncio.sleep(1) # blocking call
    print('world')
    return_value = await task   # the placement of the `await` is important. Placing above `await asyncio.sleep(1)` will block the execution of the code.
    print('return value:', return_value)
    return return_value

async def function_2():
    print('>> function_2 started...')
    await asyncio.sleep(2)
    print('>> function_2 terminated.')
    return 1

result = asyncio.run(base_func_2())
print('result:', result)
# example 2: with return value(s) ------------------------------->>
```

