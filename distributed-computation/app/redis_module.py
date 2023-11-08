"""
------------------------------------------------------------------------
Redis module

Helper module to
    - Access redis db
    - pull from a redis queue
    - push to a redis queue

: 08.11.23
: zach wolpe
: zach.wolpe@medibio.com.au
------------------------------------------------------------------------
"""
import redis

class redis_access:

    @staticmethod
    def redis_db(config):
        db = redis.Redis(
            host        = config.redis_host,
            port        = config.redis_port,
            db          = config.redis_db,
            password    = config.redis_password
        )
        # query access
        db.ping()
        return db

    @staticmethod
    def redis_queue_push(config, db, message):
        """push to tail of the queue (left of list)"""
        db.lpush(config.redis_queue_name, message)

    @staticmethod
    def redis_queue_pop(config, db):
        """
        pop from head of the queue (right of list)
        the `b` in `brpop` indicates this is a blocking call (waits until an item becomes available).
        """
        _, message_json = db.brpop(config.redis_queue_name)
        return message_json

    
