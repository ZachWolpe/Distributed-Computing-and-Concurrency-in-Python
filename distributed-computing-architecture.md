
# Distributed Computing with Redis

```
: 10.11.23
: zach.wolpe@medibio.com.au
```


# Distributed Computing with Redis

A better solution is to skip trying to optimize runtime on one machine and build to scale horizontally. Here is an example of a simple scalable architecture:

_*Using a message queue (`Redis`) to distribute computationally intensive (CPU bound) tasks to multiple workers (`Python`).*_


## Architecture

**1. Decouple your code into several microservices.**

In a machine learning context, we perform inference at multiple stages when deploying an algorithm (feature engineering, exclusions, business logic etc). Decoupling these logically isolated units means we can use cache results when runtime matters and spin up different module stages simultaneously. These microservices are also called "workers" in this context.

**2. Build a Queue to handle communication between microservices.**

Microservices need a way to communicate. We can use a queue to decentralize this communication. We'll use Redis (an in-memory database) to build our queue.

**3. Build a main app to handle requests.**

You'll need some front-end logic to handle requests. Normally this handles incoming web app traffic, but the same approach can be used to handle request launch ML training/inference modules. This becomes your API gateway to either:

- Interact with the front end (usually through a load balancer).
Launch training/inference jobs.
- This main app does not handle the request, it only receives them.

**4. Connect the main app to the microservers.**

- *Receive Requests*: The core app receives requests (API enpoints, launching training jobs etc) and filters, and channel them to the correct queue.
- *Push to Redis*: The core app then pushes the requests to the Redis queue/s.
- *Workers listen to the Queue*: These workers listen to the queue/s and fetch and process requests as they become available.

*_Workers can then be spun up and shut down as required._*
