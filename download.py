'''
Created on Dec 22, 2011

@author: nev3rm0re
'''

import Queue
import threading
import urllib, urllib2
import time

urls = [('http://cs1104.vkontakte.ru/u5199746/audio/2e1bc7e28b70.mp3','file1.mp3'),
        ('http://cs1325.vkontakte.ru/u5199746/audio/ba5ca2561b61.mp3', 'file2.mp3'),
        ('http://cs5009.vkontakte.ru/u2142991/audio/23dc3f83353e.mp3', 'file3.mp3'),
        ('http://cs4661.vkontakte.ru/u38108564/audio/5521f7990a1b.mp3', 'file4.mp3'),
        ('http://cs4697.vkontakte.ru/u18861176/audio/781e472dc2f3.mp3', 'file5.mp3'),
        ('http://cs552.vkontakte.ru/u6295979/audio/a1d2294364f6.mp3', 'file6.mp3'),
        ('http://cs4614.vkontakte.ru/u552631/audio/0b91e11ef0d9.mp3', 'file7.mp3'),
        ('http://cs4625.vkontakte.ru/u2136339/audio/e36abb3d2243.mp3', 'file8.mp3'),
        ('http://cs4700.vkontakte.ru/u2449878/audio/e8f519aaf56a.mp3', 'file9.mp3'),
        ('http://cs4700.vkontakte.ru/u1213200/audio/537007ab2c7c.mp3', 'file10.mp3'),
        ('http://cs4502.vkontakte.ru/u6420401/audio/f8bb388d9655.mp3', 'file11.mp3')]

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        
    def run(self):
        while True:
            (url, filename) = self.queue.get()
            print "Downloading %s and saving it as %s" % (url.split("/")[-1], filename),
            urllib.urlretrieve(url, filename)
            print " %s done." % url.split("/")[-1]
            self.queue.task_done()
            
            
class Downloader():
    def __init__(self, url_list):
        self.queue = Queue.Queue()
        
        for url in url_list:
            self.queue.put(url)
        
    def startDownload(self):
        print "Starting download"
        for dummy in range(5):
            t = ThreadUrl(self.queue)
            t.setDaemon(True)
            t.start()
            
        self.queue.join();
            
if __name__ == "__main__":
    downloader = Downloader(urls[1:3])
    downloader.startDownload()
