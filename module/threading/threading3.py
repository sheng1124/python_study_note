#執行續3
#python 直譯器同時間只允許執行一個執行緒，不是真的平行化，每個執行緒輪流執行
#有時速度快到像是同時處理

import threading
from urllib.request import urlopen
import time

def download(url, file):
    with urlopen(url) as url, open(file, 'wb') as f:
        f.write(url.read())
        print(file, " writed")

urls = [
    'https://openhome.cc/Gossip/Go/',
    'https://openhome.cc/Gossip/CGossip/',
    'https://openhome.cc/Gossip/CppGossip/',
    'https://openhome.cc/Gossip/GTKGossip/'
]

filenames1 = [
    'a.html',
    'b.html',
    'c.html',
    'd.html'
]

filenames2 = [
    'a2.html',
    'b2.html',
    'c2.html',
    'd2.html'
]

#阻斷
#有時候需要等待輸入或連線，這個行為叫做阻斷 
#如果沒有可以切換的執行緒，直譯器會等待目前的阻斷作業
#以下是需要阻斷的程式碼 下載檔案並寫入
start = time.perf_counter()
for url, filename in zip(urls, filenames1):
    download(url, filename)
print("block ", time.perf_counter() - start) #2.2272031

#以下是使用多執行續
start = time.perf_counter()
threads=[]
for url, filename in zip(urls, filenames2):
    t = threading.Thread(target=download, args=(url, filename))
    t.start()
    threads.append(t)

#等所有執行緒完成
for t in threads:
    t.join()
print("threads ", time.perf_counter() - start) #0.7187613000000002 
