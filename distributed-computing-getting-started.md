# Building a distributed computing environment

```
: 10.11.23
: zach.wolpe@medibio.com.au
```

A complete build is available here.

1. Main App: pushes tasks/messages to queue.
2. Workers: pull tasks from queue and process them.

NB: It is important that the order of tasks is irrelevant.

The queue should be thread-safe and atomic (Redis is both). - atomic: the queue will not be corrupted if multiple workers try to pull a task at the same time. - thread-safe: the queue will not be corrupted if multiple workers try to push a task at the same time.

### Redis

Redis is an in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries and streams.

Redis guarantees that multiple clients will not be able to corrupt the queue when pushing or pulling tasks.
Resilience to runtime crashes
If we need resilience to runtime crashes, Redis requires additional configuration. Using Rabbit or SQS solve this problem.

# Getting Started

## 1. Setup

Setup a directory `distributed-computation/` which contains:

- `app/`: subdirectory.
- `worker/`: subdirectory.

`docker-compose.yml`: a docker-compose file used to build a Redis docker image and launch a container.


## 2. Build and launch the Redis Image

```docker-compose up -d```

## 3. Build the App

```python app/main.py```

## 4. Launch the Redis CLI

```docker compose run redis redis-cli -h redis -a dummy-pass -n 0```
