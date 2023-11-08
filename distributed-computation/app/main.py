"""
------------------------------------------------------------------------
Main application file.

Push messages to into the redis queue.


: 08.11.23
: zach wolpe
: zach.wolpe@medibio.com.au
------------------------------------------------------------------------
"""

import  datetime
import  random
import  config
import  json
import  time
import  uuid

from redis_module import redis_access

def main(num_messages:int, delay:float=1):
    """
    Generate random messages and push to redis queue.

    Arguments:
        num_messages: number of messages to generate
    
    Return: None
    """

    db = redis_access.redis_db(config=config)

    for i in range(num_messages):
        # generate random message
        id = str(i) + '_xv1'
        message = {
            'id':           str(uuid.uuid4()),
            'timestamp':    str(datetime.datetime.now()),
            'value':        random.randint(0, 100),
            'data': {
                'message_no':   id,
                'message':      f'Hello world {id}:{random.randint(0, 100)}'
            }
        }

        message_json = json.dumps(message)

        # push to redis queue
        _msg_sample = message['data']['message'][:4] + '...'
        print(f'Pushing message number {i} (id: {id}): message={_msg_sample}')
        redis_access.redis_queue_push(config, db, message_json)

        time.sleep(delay)
    

if __name__ == '__main__':
    print('Launching main application...')
    main(num_messages=20, delay=1)
    print('Main application completed.')