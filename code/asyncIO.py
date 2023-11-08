"""
----------------------------------------------------------------------------------------------------
asyncIO.py

Examples of using the `asyncio` library. asyncIO is a library to write concurrent code using the async/await syntax.

: 08 Nov 23
: zach wolpe
: zach.wolpe@medibio.com.au
----------------------------------------------------------------------------------------------------
"""

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
