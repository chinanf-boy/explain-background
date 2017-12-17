import time

from background import background

# Use 40 background threads.
background.n = 40


@background.task
def work():
    print('get')
    time.sleep(2)


@background.callback
def work_callback(future):
    print(future)


for _ in range(2):
    work()