import cv2

import win32api
import win32con
import win32gui
import win32print

import numpy as np
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import font, filedialog

import Core
from GUI.BasePage import BasePage

class MainPage(BasePage):

    basicSize = 0

    colorL = "white"

    colorR = "white"

    # 读入的图片
    cv2Image:np.ndarray = None

    # 图片容器
    imgLabel:tk.Label = None

    # 算式文本
    formulaText:tk.Text = None

    # 结果容器
    resultContent:tk.StringVar = None

    def __init__(self):
        super().__init__("手写数字识别")

        hDC = win32gui.GetDC(0)

        resolutionRatio_physical = (win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES), win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES))
        resolutionRatio_logical = (win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN))

        self.basicSize = round(resolutionRatio_physical[0] / resolutionRatio_logical[0], 2)

        self.page.geometry(str(resolutionRatio_logical[0] // 2) + "x" + str(resolutionRatio_logical[1] // 2))

        self.page.resizable(0,0)

        #设置字体
        ft1 = font.Font(family = '微软雅黑', size = self.Fontsize(17), weight = "bold")
        ft2 = font.Font(family = '微软雅黑', size = self.Fontsize(11))
        ft3 = font.Font(family = '微软雅黑', size = self.Fontsize(8))

        resultContent = tk.StringVar()

        frame_L = tk.Frame(self.page, borderwidth = 2, bg = self.colorL)
        frame_L.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 1)

        frame_L_T = tk.Frame(frame_L)
        frame_L_T.place(relx = 0.02 , rely = 0.02, relwidth=0.96, relheight = 0.84)

        frame_L_B =tk.Frame(frame_L)
        frame_L_B.place(relx = 0.02, rely = 0.88, relwidth = 0.96, relheight = 0.1)

        self.imgLabel = tk.Label(frame_L_T, text = "打开图像进行识别", font = ft1, bg = self.colorL)
        self.imgLabel.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        button_open = tk.Button(frame_L_B, text = "打开图片", font=ft2, command = self.Open)
        button_open.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 1)

        button_identifi = tk.Button(frame_L_B, text = "识别", font = ft2, command = self.Recognize)
        button_identifi.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)

        frame_R = tk.Frame(self.page, borderwidth = 2)
        frame_R.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)

        self.formulaText = tk.Text(frame_R, font = ft1, bd = self.basicSize * 2)
        self.formulaText.place(relx = 0.02, rely = 0.02, relwidth = 0.96, relheight = 0.54)

        button_calculate = tk.Button(frame_R, text = "计算", font = ft3, command = self.Calculate)
        button_calculate.place(relx = 0.02, rely = 0.58, relwidth = 0.96, relheight = 0.06)

        entry_result = tk.Entry(frame_R, font = ft1, justify = tk.CENTER, state = "readonly", textvariable = resultContent, bd = self.basicSize * 2)
        entry_result.place(relx = 0.02, rely = 0.66, relwidth = 0.96, relheight = 0.24)

        button_save = tk.Button(frame_R, text = "保存", font = ft3, command = self.Save)
        button_save.place(relx = 0.02, rely = 0.92, relwidth = 0.96, relheight = 0.06)


    def Open(self):
        '''
        打开图片
        '''
        self.ImagelabelUpdate(cv2.imdecode(np.fromfile(filedialog.askopenfilename(), dtype = np.uint8), 1))


    def ImagelabelUpdate(self, cv2img):
        '''
        更新图片
        '''
        self.cv2Image = cv2img

        img_tk = self.Cv2Tk(cv2img)

        self.imgLabel.configure(image = img_tk)
        self.imgLabel.image = img_tk
        self.imgLabel.update()


    def Cv2Tk(self, image, size:tuple = (500, 500)) -> ImageTk:
        '''
        返回将cv2转化为tk后的文件文件
        '''
        k = min((size[0] / image.shape[0]), (size[1] / image.shape[1]))

        resized = cv2.resize(image, (int(image.shape[1] * k), int(image.shape[0] * k)))

        return ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)))


    #图像识别
    def Recognize(self):
        formula = Core.recognizer.recognize(self.cv2Image)

        self.formulaText.delete(0.0, tk.END)
        self.formulaText.insert(0.0, formula)

        # Imagelabel_Update(img1_cv2)
        # SV_result.set(result)
        
    
    #公式计算
    def Calculate(self):
        self.resultContent.set(Core.Analyzer.FourArithmetic().analyze(self.formulaText.get(0.0, tk.END)))


    def Save(self):
        path = str(filedialog.askdirectory()) + "/" + "识别内容及计算结果.txt"

        formulaText = self.formulaText.get(0.0, tk.END).split('\n')
        reslutText = self.resultContent.get().split('\n')
        
        text = ''

        for i in range(len(formulaText)):
            text += formulaText[i] + ' = ' + reslutText[i] + '\n'

        with open(path, mode = "w") as fi:
            fi.write(text)


    def Fontsize(self, ftsize:int):
        return int(self.basicSize * ftsize)
        
