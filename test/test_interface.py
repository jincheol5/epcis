import asyncio

async def task1():
    print("task1 start")
    await asyncio.sleep(2)
    print("task1 end")

async def task2():
    print("task2 start")
    await asyncio.sleep(1)
    print("task2 end")

async def main_1():
    await task1()
    await task2()

async def main_2():
    t1=asyncio.create_task(task1())
    t2=asyncio.create_task(task2())
    await t1
    await t2

async def main_3():
    await asyncio.gather(task1(),task2())

print(f"<<main_1>>")
asyncio.run(main_1())
print(f"\n<<main_2>>")
asyncio.run(main_2())
print(f"\n<<main_3>>")
asyncio.run(main_3())