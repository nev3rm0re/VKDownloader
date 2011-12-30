import sys, time
import wx
import urllib
import random

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)
        
        self.InitUI()
        
    def InitUI(self):
        self.gauges = list()
        self.labels = list()
        
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        fitem = filemenu.Append(wx.ID_EXIT, 'Exit', 'Exit application')
        menubar.Append(filemenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
                       
        
        for x in xrange(5):
            gauge = wx.Gauge(parent=self, 
                             range = 100, 
                             pos = (175, 100 + x * 15), 
                             size=(200, 15))
            gauge.SetValue(x * 20)
            gauge.SetBezelFace(3)
            gauge.SetShadowWidth(2)
            
            label = wx.StaticText(self)
            
            self.labels.append(label)
            self.gauges.append(gauge)
            
#       buttons
        self.btn1 = wx.Button(self, wx.ID_OK)
        self.btn1.SetLabel("Start")
        
        self.Bind(wx.EVT_BUTTON, self.onok, self.btn1)
        
        self.Show(True)
        
            
    def OnQuit(self, event):
        self.Close()

    def onok(self, event):
        number = int(random.uniform(0, 4))
        urllib.urlretrieve('http://cs4246.vkontakte.ru/u31558245/audio/cc41ab8ba4bd.mp3',
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
    app = wx.App()
    MyFrame(None)
    app.MainLoop()
    

if __name__ == "__main__":
    main()