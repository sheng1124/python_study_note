#執行續2 使用繼承 threading.Thread 方式 可自行定義 run
# 書上說不推薦適用 因為使得流程與 thread.Thread 產生相依性

import threading
import random
import os
import time

# Thread 繼承方式使用範本
#範本1
class Tortoise(threading.Thread):
    def __init__(self, total_step):
        super().__init__()
        self.total_step = total_step

    def run(self):
        step = 0
        while step < self.total_step:
            step += 1
            print("t run {}".format(step))
            time.sleep(1)
        print("t finish")

#範本2
class Hare(threading.Thread):
    def __init__(self, total_step):
        super().__init__()
        self.total_step = total_step
    
    def run(self):
        step = 0
        sleep = [True, False]
        while step < self.total_step:
            ind = int(random.random() * 10) % 2
            issleep = sleep[ind]
            if issleep:
                print("r is sleep")
            else:
                step += 2
                print("r run {}".format(step))
            time.sleep(1)
        print("r finish")


# Thread 使用
Tortoise(10).start()

Hare(10).start()