import sys, time
import wx
import urllib
import random

class MyApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, args, kwargs)
        
        self.frame = wx.Frame(None, wx.ID_ANY, "Hello world")
        self.frame.Show(True)
        
        self.gauges = list()
        self.labels = list()
        
        for x in xrange(5):
            gauge = wx.Gauge(parent=self.frame, 
                             range = 100, 
                             pos = (175, 100 + x * 15), 
                             size=(200, 15))
            gauge.SetValue(x * 20)
            gauge.SetBezelFace(3)
            gauge.SetShadowWidth(2)
            
            label = wx.StaticText(self.frame)
            
            self.labels.append(label)
            self.gauges.append(gauge)
            
#       buttons
        self.btn1 = wx.Button(self.frame, wx.ID_OK)
        self.btn1.SetLabel("Start")
        
        self.frame.Bind(wx.EVT_BUTTON, self.onok, self.btn1)
            
    def onok(self, event):
        number = int(random.uniform(0, 4))
        urllib.urlretrieve('http://cs4647.vkontakte.ru/u73018045/audio/874fed1e35e2.mp3',
                           "file.mp3",
                           reporthook=lambda bc, bs, ts, number=number: self.reporthook(bc, bs, ts, number))
    
    def reporthook(self, block_count, block_size, total_size, number):
        percent = 100 * block_count * block_size / total_size
        self.setGaugeValue(number, int(percent))
        self.labels[number].SetLabel("Downloading")
    
    def setGaugeValue(self, number, value):
        self.gauges[number].SetValue(value)
        self.Yield()
def main():
    app = MyApp(False)
    app.MainLoop()
    

if __name__ == "__main__":
    main()