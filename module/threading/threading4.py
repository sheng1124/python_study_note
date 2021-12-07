import threading
import time

#Daemon 執行緒
#預設的 main thread 會等所有執行緒完成才終止程式
#可以指定參數 daemon=True 執行緒不需要等待執行完才加入主執行緒
#主執行緒會直接終止 

def test():
    time.sleep(10)
    print("ddddddddaaaaa")

x = threading.Thread(target=test , daemon=True)

x.start()
print("exit")
