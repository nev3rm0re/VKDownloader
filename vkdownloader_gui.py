import wx

import login


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)
        
        self.init_ui()
        
    def init_ui(self):
        self.song_list = wx.CheckListBox(self, 100, size=(150, 100))
        
        self.button = wx.Button(self)
        self.Bind(wx.EVT_BUTTON, self.on_load_click)
        self.Show(True)
        
    def on_load_click(self):
        
    
    
def main():
    app = wx.App()
    MyFrame(None)
    app.MainLoop()
    
if __name__ == "__main__":
    main()