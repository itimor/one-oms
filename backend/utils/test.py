import asyncio
import time


async def first_fun(delay):
    print('开始执行 first_fun 函数。')
    await asyncio.sleep(delay)
    print("*****" * delay)
    print('first_fun 函数执行结束。')
    return "*****" * delay


async def main():
    a = [1,2,3]
    print(f"started at {time.strftime('%X')}")
    for i in a:
        print('=============')
        asyncio.create_task(first_fun(i))
    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
