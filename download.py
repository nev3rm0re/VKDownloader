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

def dlProgress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    print "...%d%%" % percent

class DownloadQueue(Queue.Queue):
    def get(self, block=True, timeout=None):
        item = Queue.Queue.get(self, block, timeout)
        print 'got %r' % (item,)
        return item
    def put(self, item, block=True, timeout=None):
        Queue.Queue.put(self, item, block, timeout)
        print 'new (of %s jobs): %r' % (self.unfinished_tasks, item)
        
    def task_done(self):
        Queue.Queue.task_done(self)
        print 'job count: %s' % self.unfinished_tasks

queue = DownloadQueue()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        
    def run(self):
        while True:
#            grabs host from queue
            (url, filename) = self.queue.get()
            
            
            u = urllib2.urlopen(url)
            meta = u.info()
#            filename = url.split("/")[-1]
            
            print "Downloading %s and saving it as %s" % (url, filename)
            
            urllib.urlretrieve(url, filename, reporthook=dlProgress)
            
            localfile = open(filename, 'wb');
            localfile.write(u.read())
            localfile.close()
            
            print "Done with %s" % filename
            self.queue.task_done()
            
start= time.time()
def main():
    for url in urls[1:3]:
        queue.put(url)
        
    for i in range(5):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    queue.join()
    
main()
print "Elapsed time: %s" % (time.time() - start)
