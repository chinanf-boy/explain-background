from background import background
import sys 
import time

print('this running show get task two and 2s show again')


@background.task
def work():
    # Do something expensive here.
    print('get task')
    time.sleep(2)
    print('get task')
    
for _ in range(2):
    work()

