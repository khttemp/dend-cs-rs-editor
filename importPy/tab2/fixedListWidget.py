from functools import partial

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

class FixedListWidget:
    def __init__(self, frame, trainIdx, decryptFile, text, elseList, ver, reloadFunc):
        self.frame = frame
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.ver = ver
        self.reloadFunc = reloadFunc

        self.elseLf = ttk.LabelFrame(self.frame, text=text)
        self.elseLf.pack(side=LEFT, anchor=NW, padx=10)

        self.txtFrame = ttk.Frame(self.elseLf)
        self.txtFrame.pack(anchor=NW)
        
        for i in range(len(self.elseList)):
            elseInfo = self.elseList[i]
            self.varTemp = StringVar()
            self.varTemp.set(elseInfo)
            self.tempTextLb = Label(self.txtFrame, textvariable=self.varTemp, font=("", 20), borderwidth=1, relief="solid")
            self.tempTextLb.grid(row=i, column=0, sticky=W+E, ipadx=15)
            self.tempBtn = Button(self.txtFrame, text="修正", font=("", 14), command=partial(self.editVar, i, elseInfo))
            self.tempBtn.grid(row=i, column=1,  sticky=W+E)

    def editVar(self, i, elseInfo):
        resultValue = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=elseInfo)
        if resultValue:
            self.elseList[i] = resultValue
            if not self.decryptFile.saveElseList(self.trainIdx, self.ver, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="情報を修正しました")

            self.reloadFunc()
