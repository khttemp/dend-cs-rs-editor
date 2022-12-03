from functools import partial

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from importPy.tkinterScrollbarFrameClass import *

class LensListWidget:
    def __init__(self, frame, decryptFile, trainIdx, lensList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.trainIdx = trainIdx
        self.lensList = lensList
        self.reloadFunc = reloadFunc

        self.lensListLf = ttk.LabelFrame(self.frame, text="レンズフレア情報")
        self.lensListLf.pack(anchor=NW, padx=10, expand=True, fill=BOTH)

        scrollbarFrame = ScrollbarFrame(self.lensListLf)

        self.txtFrame = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame.pack(anchor=NW)

        self.lensCntNameLb = Label(self.txtFrame, text="lens情報数", font=("", 20), width=12, borderwidth=1, relief="solid")
        self.lensCntNameLb.grid(row=0, column=0, sticky=W+E)
        self.varLensCnt = IntVar()
        self.varLensCnt.set(len(self.lensList))
        self.lensCntTextLb = Label(self.txtFrame, textvariable=self.varLensCnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.lensCntTextLb.grid(row=0, column=1, sticky=W+E)
        self.lensCntBtn = Button(self.txtFrame, text="修正", font=("", 14), command=lambda :self.editLensCnt(self.varLensCnt.get()))
        self.lensCntBtn.grid(row=0, column=2, sticky=W+E)

        for i in range(len(self.lensList)):
            self.txtFrame2 = ttk.Frame(scrollbarFrame.frame)
            self.txtFrame2.pack(anchor=NW, pady=5)

            self.nameFrame = ttk.Frame(self.txtFrame2)
            self.nameFrame.pack(anchor=NW)
            self.eleFrame = ttk.Frame(self.txtFrame2)
            self.eleFrame.pack(anchor=NW, padx=53)

            lensInfo = self.lensList[i]

            for j in range(len(lensInfo)):
                self.tempBtn = Button(self.nameFrame, text="修正", font=("", 14), command=partial(self.editLensList, i, lensInfo))
                self.tempBtn.grid(row=i, column=0, sticky=W+E)
                self.nameLb = Label(self.nameFrame, text="name", font=("", 20), width=7, borderwidth=1, relief="solid")
                self.nameLb.grid(row=i, column=1, sticky=W+E)
                self.f1Lb = Label(self.eleFrame, text="f1", font=("", 20), width=7, borderwidth=1, relief="solid")
                self.f1Lb.grid(row=i, column=1, sticky=W+E)
                self.b1Lb = Label(self.eleFrame, text="b1", font=("", 20), width=7, borderwidth=1, relief="solid")
                self.b1Lb.grid(row=i+1, column=1, sticky=W+E)
                
                if j in [0, 1]:
                    self.varTemp = StringVar()
                    self.varTemp.set(lensInfo[j])
                    self.temphTextLb = Label(self.nameFrame, textvariable=self.varTemp, font=("", 20), borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i, column=j+2, sticky=W+E, ipadx=10)
                elif j in [2, 3]:
                    self.varTempF = DoubleVar()
                    self.varTempF.set(round(float(lensInfo[j]), 3))
                    self.temphTextLb = Label(self.eleFrame, textvariable=self.varTempF, width = 7, font=("", 20), borderwidth=1, relief="solid")
                    self.temphTextLb.grid(row=i, column=j, sticky=W+E)
                elif j == 4:
                    for k in range(len(lensInfo[j])):
                        self.varTemp = IntVar()
                        self.varTemp.set(int(lensInfo[j][k]))
                        self.temphTextLb = Label(self.eleFrame, textvariable=self.varTemp, width = 7, font=("", 20), borderwidth=1, relief="solid")
                        self.temphTextLb.grid(row=i+1, column=k+2, sticky=W+E)

    def editLensCnt(self, val):
        result = EditLensCntWidget(self.frame, "lens情報数の変更", self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveLensCnt(self.trainIdx, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="lens情報数を修正しました")
            self.reloadFunc()
            
    def editLensList(self, i, valList):
        result = EditLensWidget(self.frame, "lens情報の変更", self.decryptFile, valList)
        if result.reloadFlag:
            self.lensList[i] = result.resultValueList
            if not self.decryptFile.saveLensList(self.trainIdx, self.lensList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="lens情報を修正しました")
            self.reloadFunc()

class EditLensCntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditLensCntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varLensCnt = IntVar()
        self.varLensCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varLensCnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varLensCnt.get())
                    if res <= 0:
                        errorMsg = "1以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValue = res
                except:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

            if self.resultValue < self.val:
                msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True

class EditLensWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, lensInfo):
        self.decryptFile = decryptFile
        self.lensInfo = lensInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditLensWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        lensInfoLbList = [
            "name1",
            "name2",
            "f1",
            "f2",
            "b1",
            "b2",
            "b3",
            "b4",
        ]
        for i in range(len(self.lensInfo)):
            if i in [0, 1]:
                self.lensLb = ttk.Label(master, text=lensInfoLbList[i], font=("", 14))
                self.lensLb.grid(row=i, column=0, sticky=W+E)
                self.varTemp = StringVar()
                self.varTemp.set(self.lensInfo[i])
                self.varList.append(self.varTemp)
                self.lensEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
                self.lensEt.grid(row=i, column=1, sticky=W+E)
            elif i in [2, 3]:
                self.lensLb = ttk.Label(master, text=lensInfoLbList[i], font=("", 14))
                self.lensLb.grid(row=i, column=0, sticky=W+E)
                self.varTemp = DoubleVar()
                self.varTemp.set(round(float(self.lensInfo[i]), 3))
                self.varList.append(self.varTemp)
                self.lensEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
                self.lensEt.grid(row=i, column=1, sticky=W+E)
            elif i == 4:
                varList = []
                for j in range(len(self.lensInfo[i])):
                    self.lensLb = ttk.Label(master, text=lensInfoLbList[i+j], font=("", 14))
                    self.lensLb.grid(row=i+j, column=0, sticky=W+E)
                    self.varTemp = IntVar()
                    self.varTemp.set(self.lensInfo[i][j])
                    varList.append(self.varTemp)
                    self.lensEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
                    self.lensEt.grid(row=i+j, column=1, sticky=W+E)
                self.varList.append(varList)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i in [0, 1]:
                            res = self.varList[i].get()
                        elif i in [2, 3]:
                            res = float(self.varList[i].get())
                        elif i == 4:
                            res = []
                            varList = self.varList[i]
                            for j in range(len(varList)):
                                var = int(varList[j].get())
                                res.append(var)
                        self.resultValueList.append(res)
                    return True
                except:
                    errorMsg = "数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception as e:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
