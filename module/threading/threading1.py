#執行續入門 第一次使用

import threading
import random
import os
import time

#定義要執行的執行續
#執行續1
def tortoise (total_step):
    step = 0
    while step < total_step:
        step += 1
        print("t run {}".format(step))
        time.sleep(1)

#執行續2
def hare(total_step):
    step = 0
    sleep = [True, False]
    while step < total_step:
        ind = int(random.random() * 10) % 2
        issleep = sleep[ind]
        if issleep:
            print("r is sleep")
        else:
            step += 2
            print("r run {}".format(step))
        time.sleep(1)

#使用執行續- threading.Thread(target= func, args=(, )) args 使用的是 tuple type
t = threading.Thread(target=tortoise, args=(10,))

h = threading.Thread(target=hare, args=(10,))

#如何執行
t.start()

h.start()