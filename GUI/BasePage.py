import tkinter as tk

class BasePage:

    page:tk.Tk = None

    width = 640

    height = 480

    system = None

    def __init__(self, title:str, width:int = 0, height:int = 0, fullscreen:bool = False):
        self.page = tk.Tk()

        self.page.title(title)

        self.page.attributes("-fullscreen", fullscreen)

        if width == 0 or height == 0:
            # 自动获取宽高
            self.page.update()
            self.width = self.page.winfo_screenwidth()
            self.height = self.page.winfo_screenheight()
        else:
            self.width = width
            self.height = height
        
        if not fullscreen:
            self.page.geometry(str(width) + "x" + str(height))

    def placeWidget(self, widget:tk.BaseWidget, x:int, y:int, width:int = 0, height:int = 0) -> tk.BaseWidget:
        ''' 放置控件, x, y为控件左上角的位置, width,height为控件的宽高, 缺省则自适应 '''
        if height == 0:
            if width == 0:
                widget.place(x = self.width * x // 100, y = self.height * y // 100)
            else:
                widget.place(x = self.width * x // 100, y = self.height * y // 100, width = self.width * width // 100)
        else:
            widget.place(x = self.width * x // 100, y = self.height * y // 100, width = self.width * width // 100, height = self.height * height // 100)
        return widget

    def getFont(self, size:int):
        ''' 获取指定大小的字体 '''
        return ('Arial', round((self.height * size // 100 - 8) * 3 // 4))