from tkinter import Frame,Tk
from tkwebview2.tkwebview2 import WebView2
        
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

