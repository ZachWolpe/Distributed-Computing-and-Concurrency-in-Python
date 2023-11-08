# Distributed Computations with Python & Redis

```
: 08.11.23
: zach.wolpe@medibio.com.au
```

Using a message `queue` (`Redis`) to distribute computationally intensive (`CPU bound`) tasks to multiple `workers` (`Python`). Example instance in the `distributed-computation` directory.

----
## Architecture

1. Main App: pushes tasks/messages to `queue`.
2. Workers: pull tasks from `queue` and process them.

It is important that the order of tasks is irrelevant.

The `queue` should be `thread-safe` and `atomic` (Redis is both).
    - `atomic`: the `queue` will not be corrupted if multiple `workers` try to pull a task at the same time.
    - `thread-safe`: the `queue` will not be corrupted if multiple `workers` try to push a task at the same time.

----
## Redis

Redis is an `in-memory` data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries and streams.

Redis gaurantees that a multiple clients will not be able to corrupt the `queue` when pushing or pulling tasks.

*Relisance to runtime crashes*

If we need relisance to runtime crashes, Redis requires addtional configuration. Using `Rabbit` or `SQS` solve this problem.

An `I/O bound` workload can benefit from threading, but it's simplier to use `async`.

----
## Getting Started

All code and examples are in the `distributed-computation` directory.

### Navigate to the `distributed-computation` directory

```bash
cd distributed\ computation
```

### 1. Install Redis

I use the official `redis` docker image. Using the `docker-compose` file:

```bash
docker-compose up -d
```
This builds a docker image from redis:latest, and launches a container in the background.

### 2. Launch the Redis CLI

In a new shell, launch the Redis CLI to interact with the Redis server.

```bash
docker compose run redis redis-cli -h redis -a dummy-pass -n 0
```

You can now interact with the Redis server. For example,

- list all keys:                `KEY *`
- get a key:                    `GET <key>`
- list all items in a queue:    `LRANGE <queue> 0 -1`


Note: use these after launching the main script to push to the queue.

### 3. Launch the main app

Launch the main app to add to the queue.

```bash
python app/main.py
```

Run `LRANGE <queue> ` In our case `${queue} = distributed-queue` thus run `lrange distributed-queue 0 -1`.

### 4. Launch worker(s)

```bash
python worker/main.py
```

The worker(s) will pull tasks from the queue and process them. Take note of the failure rate, items that fail are re-added to the queue and processed again.

----
## Improvements

- `Relisance`: Use `RabbitMQ` or `SQS` for relisance to runtime crashes.
- `de-duplicate messages`: Use another Redis database to de-duplicate messages (as a safety measure). Store a successfully processsed message ID (with some TTL), and double check that the message was not already handled successfully before handling it. TTL stands for Time To Live, and is a way to set an expiration time on a key. After the expiration time, the key will be automatically deleted.
- `monitoring`: Use another Redis queue as a DLQ (dead letter queue (DLQ) is a service implementation to store messages that the messaging system cannot or should not deliver), and monitor that for messages that cannot be handled. 
- `monitoring`: Use another Redis queue to store "in-process" items, and processing - see the Redis documentation for Pattern: Reliable Queue for more details. Prevent the loss of a message if a worker is killed after popping from the queue, but before completing its work. A more complete solution like RabbitMQ or SQS/ElasticMQ is better suited for this.