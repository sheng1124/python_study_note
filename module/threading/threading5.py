import threading, time

#主執行續暫停、停止執行續

class Some:
    def __init__(self):
        self.is_continue = True

    #關閉執行續的方法需要自己實作
    def terminate(self):
        self.is_continue = False
    
    def run(self):
        while self.is_continue:
            print("running")
            time.sleep(1)
        print('bye')

def sleep_3_sec():
    print("s3 start")
    time.sleep(3)
    print("s3 done")

#執行執行續 s3
s3 = threading.Thread(target=sleep_3_sec)
s3.start()

#主執行續等待 s3 完成
print("wait thread")
s3.join()
print("wait done")


#執行執行緒 endl
s = Some()
endl = threading.Thread(target= s.run)
endl.start()

#主執行續暫停2秒
time.sleep(2)

#關閉無盡的執行緒 endl
#關閉執行續的方法需要自己實作
s.terminate()



