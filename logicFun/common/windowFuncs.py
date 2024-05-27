"""
pip install tkwebview2
pip install pythonnet   ----clr
"""

from tkinter import Frame,Tk
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')

import sys
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart

if not have_runtime():
    install_runtime()

class HtmlWindow():
    
    def __init__(self,width:int=300,height:int=500,title:str='MyJob',url:str=None) -> None:
        self.tk = Tk()
        self.tk.geometry(f"{width}x{height}")
        self.tk.attributes("-topmost",1)
        self.tk.iconbitmap('./resources/smiling-face.ico')
    
        self.tk.resizable(height=False, width=False)
        self.tk.title(title)

        frame=WebView2(self.tk,width,height)
        frame.load_url(url)
        frame.pack()
        
    def start(self):
        self.tk.mainloop()

def run():
    w=HtmlWindow(url='http://127.0.0.1:10801',title="票据核销")
    w.start()

if __name__ =='__main__':
     
    t = Thread(ThreadStart(run))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()