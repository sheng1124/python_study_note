import threading
import time

#threading 競速 鎖定 死結

#發生 競速 共享的參數是可變動資料(自己需要修改) 就可能發生
def set_to_1(data):
    for i in range(1000000):
        data[0] = 1
        if data[0] != 1:
            print("set to 1 error data[0] = ", data[0], "i = ", i)

def set_to_2(data):
    for i in range(1000000):
        data[0] = 2
        if data[0] != 2:
            print("set to 2 error data[0] = ", data[0], "i = ", i)

data = [0]
print("race condition test")
start = time.perf_counter()
t1 = threading.Thread(target=set_to_1, args=(data, ))
t2 = threading.Thread(target=set_to_2, args=(data, ))
t1.start()
t2.start()
t1.join()
t2.join()
print("race condition test done, t = ", time.perf_counter() - start)

#鎖定共享資源 一次只讓一個執行緒存取共用參數
def set_to_1_lock(data, lock):
    for i in range(1000000):
        #鎖定資源 若再次使用acquire 會進入阻斷狀態，等到呼叫了 release() 
        lock.acquire()
        data[0] = 1
        if data[0] != 1:
            print("set to 1 error data[0] = ", data[0], "i = ", i)
        else:
            #釋放lock 若不正確的使用release()會呼叫 runtime error
            lock.release()

def set_to_1_lock_with(data, lock):
    for i in range(1000000):
        #thread.lock 實做了情境管理器 可以搭配 with 簡化 acquire() 和 release() 的呼叫
        with lock:
            data[0] = 1
            if data[0] != 1:
                print("set to 1 error data[0] = ", data[0], "i = ", i)

def set_to_2_lock(data, lock):
    for i in range(1000000):
        lock.acquire()
        data[0] = 2
        if data[0] != 2:
            print("set to 2 error data[0] = ", data[0], "i = ", i)
        else:
            lock.release()

print("resource lock test")
start = time.perf_counter()
lock = threading.Lock()
t1 = threading.Thread(target=set_to_1_lock, args=(data, lock, ))
t2 = threading.Thread(target=set_to_2_lock, args=(data, lock, ))

t1.start()
t2.start()

t1.join()
t2.join()
print("resource lock test done t = ", time.perf_counter() - start)

#死結 不正確使用 lock 會導致效能低落另一個問題是死結
#簡單來說就是 你不解除 res1 的鎖定 我就不放開 res2 的鎖定

class Resource:
    def __init__(self, name, data):
        self.name = name
        self.lock = threading.Lock()
        #自己的資源，使用此資源要避免競速
        self.resource = data
    
    #使用 lock 存取資源，避免競速
    def action2(self):
        print("action2_need_{}_lock".format(self.name))
        with self.lock:
            print("{}_lock_in_action2".format(self.name))
            self.resource += 1
        print("action2_release_{}_lock".format(self.name))
        return self.resource

    #先鎖住自己 再佔據其他人的資源(會鎖別人)
    def occupid_other1(self, other_res):
        print("occupid_other1_need_{}_lock".format(self.name))
        with self.lock:
            print("{}_lock_in_occupid_other1".format(self.name))
            other_res.action2()
        print("occupid_other1_release_{}_lock".format(self.name))

#使用資源， 會要用A再用B 會先鎖A再鎖B
def a_need_b(res_a, res_b):
    while True:
        res_a.occupid_other1(res_b)

res1 = Resource('gold', 100)
res2 = Resource('water', 20)

t1 = threading.Thread(target = a_need_b, args = (res1, res2))
t2 = threading.Thread(target = a_need_b, args = (res2, res1))

t1.start()
t2.start()