# -*- coding: utf-8 -*-

import struct
import copy
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from dendDecrypt import LSdecrypt as dendLs
from dendDecrypt import BSdecrypt as dendBs
from dendDecrypt import CSdecrypt as dendCs
from dendDecrypt import RSdecrypt as dendRs

decryptFile = None
notchContentCnt = 0
varList = []
btnList = []
trainWidget = None

LS = 0
BS = 1
CS = 2
RS = 3

class Scrollbarframe():
    def __init__(self, parent, bar_x = False, bar_y = True):
        self.canvas = Canvas(parent)
        self.frame = Frame(self.canvas, width=parent.winfo_width()-8, height=parent.winfo_height())
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame.pack()

        self.canvas.create_window((0,0), window=self.frame, anchor="nw")

        if bar_x:
            self.scrollbar_x = Scrollbar(parent, orient=HORIZONTAL, command=self.canvas.xview)
            self.scrollbar_x.pack(side=BOTTOM, fill=X)
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        if bar_y:
            self.scrollbar_y = Scrollbar(parent, orient=VERTICAL, command=self.canvas.yview)
            self.scrollbar_y.pack(side=RIGHT, fill=Y)
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class notchWidget():
    global decryptFile
    global notchContentCnt
    
    def __init__(self, i, notchCnt, frame, speed):
        self.notchNum = "ノッチ" + str(i+1)
        self.notchNumLb = Label(frame, text=self.notchNum, font=("", 20), width=10, borderwidth=1, relief="solid")
        self.notchNumLb.grid(rowspan=notchContentCnt, row=notchContentCnt*i, column=0, sticky=N+S)

        self.speedNameLb = Label(frame, text="speed", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.speedNameLb.grid(row=notchContentCnt*i, column=1, sticky=W+E)
        self.varSpeed = DoubleVar()
        self.varSpeed.set(str(speed[i]))
        varList.append(self.varSpeed)
        self.speedLb = Label(frame, textvariable=self.varSpeed, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.speedLb.grid(row=notchContentCnt*i, column=2, sticky=W+E)
        self.speedBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varSpeed, self.varSpeed.get()), state="disabled")
        self.speedBtn.grid(row=notchContentCnt*i, column=3, sticky=W+E)
        btnList.append(self.speedBtn)

        self.tlkNameLb = Label(frame, text="tlk", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.tlkNameLb.grid(row=notchContentCnt*i+1, column=1, sticky=W+E)
        self.varTlk = DoubleVar()
        self.varTlk.set(str(speed[notchCnt + i]))
        varList.append(self.varTlk)
        self.tlkLb = Label(frame, textvariable=self.varTlk, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.tlkLb.grid(row=notchContentCnt*i+1, column=2, sticky=W+E)
        self.tlkBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varTlk, self.varTlk.get()), state="disabled")
        self.tlkBtn.grid(row=notchContentCnt*i+1, column=3, sticky=W+E)
        btnList.append(self.tlkBtn)

        if notchContentCnt > 2:
            self.soundNameLb = Label(frame, text="sound", font=("", 20), width=5, borderwidth=1, relief="solid")
            self.soundNameLb.grid(row=notchContentCnt*i+2, column=1, sticky=W+E)
            self.varSound = IntVar()
            self.varSound.set(str(speed[notchCnt*2 + i]))
            varList.append(self.varSound)
            self.soundLb = Label(frame, textvariable=self.varSound, font=("", 20), width=5, borderwidth=1, relief="solid")
            self.soundLb.grid(row=notchContentCnt*i+2, column=2, sticky=W+E)
            self.soundBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varSound, self.varSound.get(), True), state="disabled")
            self.soundBtn.grid(row=notchContentCnt*i+2, column=3, sticky=W+E)
            btnList.append(self.soundBtn)
            
            self.addNameLb = Label(frame, text="add", font=("", 20), width=5, borderwidth=1, relief="solid")
            self.addNameLb.grid(row=notchContentCnt*i+3, column=1, sticky=W+E)
            self.varAdd = DoubleVar()
            self.varAdd.set(str(speed[notchCnt*3 + i]))
            varList.append(self.varAdd)
            self.addLb = Label(frame, textvariable=self.varAdd, font=("", 20), width=5, borderwidth=1, relief="solid")
            self.addLb.grid(row=notchContentCnt*i+3, column=2, sticky=W+E)
            self.addBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varAdd, self.varAdd.get()), state="disabled")
            self.addBtn.grid(row=notchContentCnt*i+3, column=3, sticky=W+E)
            btnList.append(self.addBtn)

    def editVar(self, var, value, flag = False):
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if result:
            try:
                if flag:
                    try:
                        result = int(result)
                        var.set(result)
                    except:
                        errorMsg = "整数で入力してください。"
                        mb.showerror(title="整数エラー", message=errorMsg)
                else:
                    try:
                        result = float(result)
                        var.set(result)
                    except:
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

class perfWidget():
    global decryptFile
    
    def __init__(self, i, frame, perf):
        self.perfNameLb = Label(frame, text=decryptFile.trainPerfNameList[i], font=("", 20), width=24, borderwidth=1, relief="solid")
        self.perfNameLb.grid(row=i, column=0, sticky=W+E)
        self.varPerf = DoubleVar()
        self.varPerf.set(str(perf[i]))
        varList.append(self.varPerf)
        self.perfLb = Label(frame, textvariable=self.varPerf, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.perfLb.grid(row=i, column=1, sticky=W+E)
        self.perfBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varPerf, self.varPerf.get()), state="disabled")
        self.perfBtn.grid(row=i, column=2, sticky=W+E)
        btnList.append(self.perfBtn)

    def editVar(self, var, value):
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if result:
            try:
                try:
                    result = float(result)
                    var.set(result)
                except:
                    errorMsg = "数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

class hurikoWidget():
    global decryptFile
    
    def __init__(self, i, perfCnt, frame, huriko):
        self.hurikoNameLb = Label(frame, text=decryptFile.trainHurikoNameList[i], font=("", 20), width=24, borderwidth=1, relief="solid")
        self.hurikoNameLb.grid(row=perfCnt+i, column=0, sticky=W+E)
        self.varHuriko = IntVar()
        self.varHuriko.set(str(huriko[i]))
        varList.append(self.varHuriko)
        self.hurikoLb = Label(frame, textvariable=self.varHuriko, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.hurikoLb.grid(row=perfCnt+i, column=1, sticky=W+E)
        self.hurikoBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varHuriko, self.varHuriko.get()), state="disabled")
        self.hurikoBtn.grid(row=perfCnt+i, column=2, sticky=W+E)
        btnList.append(self.hurikoBtn)

    def editVar(self, var, value):
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if result:
            try:
                try:
                    result = int(result)
                    var.set(result)
                except:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="整数エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

class trainModelWidget():
    global decryptFile
    global trainWidget
    global notchContentCnt

    def __init__(self, frame, canvas, modelInfo):
        self.frame = frame
        self.txtFrame = Frame(frame, padx=5, pady=5)
        self.txtFrame.place(relx=0, rely=0)
        self.notchLb = Label(self.txtFrame, text="ノッチ", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.notchLb.grid(row=0, column=0, sticky=W+E)

        idx = cb.current()
        index = decryptFile.indexList[idx]
        notchNum = decryptFile.byteArr[index]
        
        self.varNotch = IntVar()
        self.varNotch.set(notchNum)
        self.notchTextLb = Label(self.txtFrame, textvariable=self.varNotch, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.notchTextLb.grid(row=0, column=1, sticky=W+E)
        self.notchBtn = Button(self.txtFrame, text="修正", font=("", 14), command=lambda:self.editNotchVar(self.varNotch, self.varNotch.get()), state="disabled")
        self.notchBtn.grid(row=0, column=2, sticky=W+E)
        
        self.henseiLb = Label(self.txtFrame, text="編成数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.henseiLb.grid(row=1, column=0, sticky=W+E)
        self.varHensei = IntVar()
        self.varHensei.set(modelInfo["mdlCnt"])
        self.henseiTextLb = Label(self.txtFrame, textvariable=self.varHensei, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.henseiTextLb.grid(row=1, column=1, sticky=W+E)
        self.henseiBtn = Button(self.txtFrame, text="修正", font=("", 14), command=lambda:self.editHenseiVar(self.varHensei, self.varHensei.get()), state="disabled")
        self.henseiBtn.grid(row=1, column=2, sticky=W+E)

        self.colorLb = Label(self.txtFrame, text="カラー数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.colorLb.grid(row=2, column=0, sticky=W+E)
        self.varColor = IntVar()
        self.varColor.set(modelInfo["colorCnt"])
        self.colorTextLb = Label(self.txtFrame, textvariable=self.varColor, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.colorTextLb.grid(row=2, column=1, sticky=W+E)
        self.colorBtn = Button(self.txtFrame, text="修正", font=("", 14), command=lambda:self.editVar(self.varColor, self.varColor.get()), state="disabled")
        self.colorBtn.grid(row=2, column=2, sticky=W+E)
        
        self.mdlInfoBtn = Button(self.txtFrame, text="モデル情報を修正", font=("", 14), command=self.editModel, state="disabled")
        self.mdlInfoBtn.grid(columnspan=3, row=3, column=0, sticky=W+E)

        self.mdlFrame = Frame(frame, padx=5, pady=5)
        self.mdlFrame.place(x=300, y=0)

        self.trainLb = Label(self.mdlFrame, text="車両", font=("", 20), width=6, borderwidth=1, relief="solid")
        self.trainLb.grid(row=0, column=0)
        self.modelLb = Label(self.mdlFrame, text="モデル", font=("", 20), width=6, borderwidth=1, relief="solid")
        self.modelLb.grid(row=1, column=0)
        if len(modelInfo["pantaNames"]) > 0:
            self.pantaLb = Label(self.mdlFrame, text="パンタ", font=("", 20), width=6, borderwidth=1, relief="solid")
            self.pantaLb.grid(row=2, column=0)
        if len(modelInfo["colList"]) > 0:
            self.colLb = Label(self.mdlFrame, text="COL", font=("", 20), width=6, borderwidth=1, relief="solid")
            self.colLb.grid(row=3, column=0)

        self.mdlNoLbList = []
        self.comboList = []
        
        for i in range(modelInfo["mdlCnt"]):
            self.mdlNoLb = Label(self.mdlFrame, text=str(i+1), font=("", 20), width=16, borderwidth=1, relief="solid")
            self.mdlNoLb.grid(row=0, column=i+1)
            self.mdlNoLbList.append(self.mdlNoLb)
            
            self.mdlCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["mdlNames"], state="disabled")
            self.mdlCb.grid(row=1, column=i+1)
            if modelInfo["mdlList"][i] == -1:
                self.mdlCb.current(len(modelInfo["mdlNames"])-1)
            else:
                self.mdlCb.current(modelInfo["mdlList"][i])
            self.comboList.append(self.mdlCb)

            if len(modelInfo["pantaNames"]) > 0:
                self.pantaCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["pantaNames"], state="disabled")
                self.pantaCb.grid(row=2, column=i+1)
                if modelInfo["pantaList"][i] == -1:
                    self.pantaCb.current(len(modelInfo["pantaNames"])-1)
                else:
                    self.pantaCb.current(modelInfo["pantaList"][i])
                self.comboList.append(self.pantaCb)

            if len(modelInfo["colList"]) > 0:
                self.colCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["colNames"], state="disabled")
                self.colCb.grid(row=3, column=i+1)
                if modelInfo["colList"][i] == -1:
                    self.colCb.current(len(modelInfo["colNames"])-1)
                else:
                    self.colCb.current(modelInfo["colList"][i])
                self.comboList.append(self.colCb)


        self.frame.update()
        if 300 + self.mdlFrame.winfo_width() > self.frame["width"]:
            self.frame["width"] = 300 + self.mdlFrame.winfo_width()
            self.frame.update()
        
    def editVar(self, var, value):
        if v_radio.get() in [LS, BS]:
            title = ""
            if v_radio.get() == LS:
                title = "LS"
            else:
                title = "BS"
            errorMsg = "{0}はカラー修正をサポートしません".format(title)
            mb.showerror(title="エラー", message=errorMsg)
            return
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if result:
            try:
                try:
                    result = int(result)
                    if result <= 0:
                        errorMsg = "1以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return
                    var.set(result)
                except:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def editNotchVar(self, var, value):
        editNotchInfo(root, "ノッチ情報修正")

    def editHenseiVar(self, var, value):
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if result:
            result = int(result)
            if result <= 0:
                errorMsg = "1以上の数字で入力してください。"
                mb.showerror(title="数字エラー", message=errorMsg)
                return
            
            mb.showinfo(title="成功", message="編成数を修正しました")
            oldCnt = var.get()
            editableNum = len(self.comboList) // oldCnt
            var.set(result)
            idx = cb.current()
            modelInfo = decryptFile.trainModelList[idx]

            modelInfo["mdlCnt"] = result
            if result > oldCnt:
                diff = result - oldCnt
                for i in range(diff):
                    mdlNoLb = Label(self.mdlFrame, text=str(oldCnt+i+1), font=("", 20), width=16, borderwidth=1, relief="solid")
                    mdlNoLb.grid(row=0, column=oldCnt+i+1, sticky=W+E)
                    self.mdlNoLbList.append(mdlNoLb)
                    modelInfo["mdlList"].append(0)
                    mdlCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["mdlNames"])
                    mdlCb.grid(row=1, column=oldCnt+i+1, sticky=W+E)
                    mdlCb.current(0)
                    self.comboList.append(mdlCb)
                    if len(modelInfo["pantaNames"]) > 0:
                        modelInfo["pantaList"].append(0)
                        pantaCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["pantaNames"])
                        pantaCb.grid(row=2, column=oldCnt+i+1, sticky=W+E)
                        pantaCb.current(0)
                        self.comboList.append(pantaCb)
                    if editableNum == 3:
                        modelInfo["colList"].append(0)
                        colCb = ttk.Combobox(self.mdlFrame, font=("", 14), width=20, value=modelInfo["colNames"])
                        colCb.grid(row=3, column=oldCnt+i+1, sticky=W+E)
                        colCb.current(0)
                        self.comboList.append(colCb)
            elif result < oldCnt:
                diff = oldCnt - result
                for i in range(diff):
                    mdlNoLb = self.mdlNoLbList.pop()
                    mdlNoLb.destroy()
                    modelInfo["mdlList"].pop()
                    combo = self.comboList.pop()
                    width = combo.winfo_width()
                    combo.destroy()
                    if len(modelInfo["pantaNames"]) > 0:
                        modelInfo["pantaList"].pop()
                        combo = self.comboList.pop()
                        combo.destroy()
                    if editableNum == 3:
                        modelInfo["colList"].pop()
                        combo = self.comboList.pop()
                        combo.destroy()

                    self.mdlFrame["width"] -= width
                    self.frame["width"] -= width

            self.mdlFrame.update()
            self.frame.update()
            if 300 + self.mdlFrame.winfo_width() > self.frame["width"]:
                self.frame["width"] = 300 + self.mdlFrame.winfo_width()
                self.frame.update()

            #LSは自動編成される
            if v_radio.get() == LS:
                for i in range(len(modelInfo["mdlList"])):
                    modelInfo["mdlList"][i] = 1
                modelInfo["mdlList"][0] = 0
                modelInfo["mdlList"][-1] = len(modelInfo["mdlNames"])-1

                cIdx = 0
                for i in range(len(self.comboList)):
                    #TAKUMIの場合
                    if len(modelInfo["pantaNames"]) == 0:
                        self.comboList[i].current(modelInfo["mdlList"][cIdx])
                        self.comboList[i]["state"] = "disabled"
                        cIdx += 1
                    else:
                        if i % 2 == 0:
                            self.comboList[i].current(modelInfo["mdlList"][cIdx])
                            self.comboList[i]["state"] = "disabled"
                            cIdx += 1

            decryptFile.trainModelList[idx] = modelInfo
    def editModel(self):
        if v_radio.get() not in [LS, BS]:
            editModelInfo(root, "モデル情報修正")
        else:
            title = ""
            if v_radio.get() == LS:
                title = "LS"
            else:
                title = "BS"
            errorMsg = "{0}はモデル修正をサポートしません".format(title)
            mb.showerror(title="エラー", message=errorMsg)

class editNotchInfo(sd.Dialog):
    global decryptFile
    global trainWidget
    global notchContentCnt
    
    def __init__(self, master, title):
        super(editNotchInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        idx = cb.current()
        index = decryptFile.indexList[idx]
        notchNum = decryptFile.byteArr[index]

        if notchNum == 4:
            notchIdx = 0
        elif notchNum == 5:
            notchIdx = 1
        elif notchNum == 12:
            notchIdx = 2
        
        self.notchLb = Label(frame, text="ノッチ情報を修正してください")
        self.notchLb.grid(row=0, column=0)
        notchList = ["４ノッチ", "５ノッチ", "１２ノッチ"]
        self.notchCb = ttk.Combobox(frame, width=12, value=notchList, state="readonly")
        self.notchCb.current(notchIdx)
        self.notchCb.grid(row=1, column=0)

    def validate(self):
        if v_radio.get() <= BS:
            if self.notchCb.current() == 2:
                mb.showerror(title="エラー", message="12ノッチを対応できません")
                return False
        warnMsg = "ノッチ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            idx = cb.current()
            
            newNotchNum = -1
            notchIdx = self.notchCb.current()
            if notchIdx == 0:
                newNotchNum = 4
            elif notchIdx == 1:
                newNotchNum = 5
            elif notchIdx == 2:
                newNotchNum = 12

            if not decryptFile.saveNotchInfo(idx, newNotchNum):
                decryptFile.printError()
                return False
            else:
                return True
    def apply(self):
        errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
        if not decryptFile.saveTrain():
            decryptFile.printError()
            mb.showerror(title="保存エラー", message=errorMsg)
        else:
            mb.showinfo(title="成功", message="ノッチ数を変更しました")
            reloadFile()
            editTrain()

class editModelInfo(sd.Dialog):
    global decryptFile
    global cb
    global trainWidget

    def __init__(self, master, title):
        super(editModelInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        idx = cb.current()
        modelInfo = decryptFile.trainModelList[idx]

        self.btnFrame = Frame(frame, pady=5)
        self.btnFrame.pack()
        self.listFrame = Frame(frame)
        self.listFrame.pack()

        self.editableNum = len(trainWidget.comboList) // modelInfo["mdlCnt"]

        self.selectListNum = 0
        self.selectIndex = 0
        self.selectValue = ""
        self.modelInfo = None
        
        self.modifyBtn = Button(self.btnFrame, font=("", 14), text="修正", state="disabled", command=self.modify)
        self.modifyBtn.grid(padx=10, row=0, column=0, sticky=W+E)
        self.insertBtn = Button(self.btnFrame, font=("", 14), text="挿入", state="disabled", command=self.insert)
        self.insertBtn.grid(padx=10, row=0, column=1, sticky=W+E)
        self.deleteBtn = Button(self.btnFrame, font=("", 14), text="削除", state="disabled", command=self.delete)
        self.deleteBtn.grid(padx=10, row=0, column=2, sticky=W+E)
        
        self.trackModelLb = Label(self.listFrame, font=("", 14), text="台車モデル")
        self.trackModelLb.grid(row=0, column=0, sticky=W+E)
        self.v_trackModel = StringVar(value=modelInfo["trackNames"])
        self.trackModelList = Listbox(self.listFrame, font=("", 14), listvariable=self.v_trackModel)
        self.trackModelList.grid(row=1, column=0, sticky=W+E)
        self.trackModelList.bind('<<ListboxSelect>>', lambda e:self.buttonActive(e, 0, self.trackModelList.curselection()))

        self.padLb = Label(self.listFrame, width=3)
        self.padLb.grid(row=0, column=1, sticky=W+E)
        
        self.trainModelLb = Label(self.listFrame, font=("", 14), text="車両モデル")
        self.trainModelLb.grid(row=0, column=2, sticky=W+E)
        trainModelList = copy.deepcopy(modelInfo["mdlNames"])
        trainModelList.pop()
        self.v_trainModel = StringVar(value=trainModelList)
        self.trainModelList = Listbox(self.listFrame, font=("", 14), listvariable=self.v_trainModel)
        self.trainModelList.grid(row=1, column=2, sticky=W+E)
        self.trainModelList.bind('<<ListboxSelect>>', lambda e:self.buttonActive(e, 1, self.trainModelList.curselection()))

        self.padLb = Label(self.listFrame, width=3)
        self.padLb.grid(row=0, column=3, sticky=W+E)

        self.pantaModelLb = Label(self.listFrame, font=("", 14), text="パンタモデル")
        self.pantaModelLb.grid(row=0, column=4, sticky=W+E)
        pantaModelList = copy.deepcopy(modelInfo["pantaNames"])
        pantaModelList.pop()
        self.v_pantaModel = StringVar(value=pantaModelList)
        self.pantaModelList = Listbox(self.listFrame, font=("", 14), listvariable=self.v_pantaModel)
        self.pantaModelList.grid(row=1, column=4, sticky=W+E)
        self.pantaModelList.bind('<<ListboxSelect>>', lambda e:self.buttonActive(e, 2, self.pantaModelList.curselection()))

        if self.editableNum == 3:
            self.padLb = Label(self.listFrame, width=3)
            self.padLb.grid(row=0, column=5, sticky=W+E)
            
            self.colModelLb = Label(self.listFrame, font=("", 14), text="COLモデル")
            self.colModelLb.grid(row=0, column=6, sticky=W+E)
            colModelList = copy.deepcopy(modelInfo["colNames"])
            colModelList.pop()
            self.v_colModel = StringVar(value=colModelList)
            self.colModelList = Listbox(self.listFrame, font=("", 14), listvariable=self.v_colModel)
            self.colModelList.grid(row=1, column=6, sticky=W+E)
            self.colModelList.bind('<<ListboxSelect>>', lambda e:self.buttonActive(e, 3, self.colModelList.curselection()))

    def buttonActive(self, event, num, value):
        if len(value) == 0:
            return
        self.selectListNum = num
        self.selectIndex = value[0]
        if num == 0:
            self.selectValue = self.trackModelList.get(value[0])
        elif num == 1:
            self.selectValue = self.trainModelList.get(value[0])
        elif num == 2:
            self.selectValue = self.pantaModelList.get(value[0])
        elif num == 3:
            self.selectValue = self.colModelList.get(value[0])
            
        self.modifyBtn["state"] = "normal"
        self.insertBtn["state"] = "normal"
        self.deleteBtn["state"] = "normal"

    def modify(self):
        result = sd.askstring(title="変更", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            if self.selectListNum == 0:
                self.trackModelList.delete(self.selectIndex)
                self.trackModelList.insert(self.selectIndex, result)
            elif self.selectListNum == 1:
                self.trainModelList.delete(self.selectIndex)
                self.trainModelList.insert(self.selectIndex, result)
            elif self.selectListNum == 2:
                self.pantaModelList.delete(self.selectIndex)
                self.pantaModelList.insert(self.selectIndex, result)
            elif self.selectListNum == 3:
                self.colModelList.delete(self.selectIndex)
                self.colModelList.insert(self.selectIndex, result)

    def insert(self):
        result = sd.askstring(title="挿入", prompt="入力してください", initialvalue=self.selectValue, parent=self)

        if result:
            if self.selectListNum == 0:
                self.trackModelList.insert(END, result)
            elif self.selectListNum == 1:
                self.trainModelList.insert(END, result)
            elif self.selectListNum == 2:
                self.pantaModelList.insert(END, result)
            elif self.selectListNum == 3:
                self.colModelList.insert(END, result)

    def delete(self):
        selectName = ""
        cnt = trainWidget.varHensei.get()
        
        if self.selectListNum == 0:
            selectName = "台車モデル"
            if self.trackModelList.size() <= 2:
                mb.showerror(title="エラー", message="台車モデルは2個以上である必要あります")
                return
        elif self.selectListNum == 1:
            selectName = "車両モデル"
            for i in range(cnt):
                if self.selectIndex == trainWidget.comboList[self.editableNum*i].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i+1))
                    return
        elif self.selectListNum == 2:
            selectName = "パンタモデル"
            for i in range(cnt):
                if self.selectIndex == trainWidget.comboList[self.editableNum*i+1].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i+1))
                    return
        elif self.selectListNum == 3:
            selectName = "COLモデル"
            for i in range(cnt):
                if self.selectIndex == trainWidget.comboList[self.editableNum*i+2].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i+1))
                    return

        warnMsg = "{0}の{1}番目を削除します。\nそれでもよろしいですか？".format(selectName, self.selectIndex+1)
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)

        if result:
            if self.selectListNum == 0:
                self.trackModelList.delete(self.selectIndex)
                self.trackModelList.select_set(END)
            elif self.selectListNum == 1:
                self.trainModelList.delete(self.selectIndex)
                self.trainModelList.select_set(END)
            elif self.selectListNum == 2:
                self.pantaModelList.delete(self.selectIndex)
                self.pantaModelList.select_set(END)
            elif self.selectListNum == 3:
                self.colModelList.delete(self.selectIndex)
                self.colModelList.select_set(END)

    def validate(self):
        warnMsg = "モデル情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            idx = cb.current()
            modelInfo = decryptFile.trainModelList[idx]

            newTrackList = []
            for i in range(self.trackModelList.size()):
                newTrackList.append(self.trackModelList.get(i))
            modelInfo["trackNames"] = newTrackList

            newTrainList = []
            for i in range(self.trainModelList.size()):
                newTrainList.append(self.trainModelList.get(i))
            newTrainList.append("なし")
            modelInfo["mdlNames"] = newTrainList

            newPantaList = []
            for i in range(self.pantaModelList.size()):
                newPantaList.append(self.pantaModelList.get(i))
            newPantaList.append("なし")
            modelInfo["pantaNames"] = newPantaList

            if self.editableNum == 3:
                newColList = []
                for i in range(self.colModelList.size()):
                    newColList.append(self.colModelList.get(i))
                newColList.append("なし")
                modelInfo["colNames"] = newColList
            else:
                newColList = []
                colName = modelInfo["colNames"][0]
                for i in range(self.trainModelList.size()):
                    newColList.append(colName)
                newColList.append("なし")
                modelInfo["colNames"] = newColList

            cnt = trainWidget.varHensei.get()
            
            for i in range(cnt):
                trainWidget.comboList[self.editableNum*i]["values"] = newTrainList
                trainWidget.comboList[self.editableNum*i+1]["values"] = newPantaList
                if self.editableNum == 3:
                    trainWidget.comboList[self.editableNum*i+2]["values"] = newColList

            decryptFile.trainModelList[idx] = modelInfo
            self.modelInfo = modelInfo
            return True

    def apply(self):
        mb.showinfo(title="成功", message="モデルリストを修正しました")

        cnt = trainWidget.varHensei.get()
        for i in range(cnt):
            trainWidget.comboList[self.editableNum*i].update()
            trainWidget.comboList[self.editableNum*i].current(self.modelInfo["mdlList"][i])
            trainWidget.comboList[self.editableNum*i+1].update()
            trainWidget.comboList[self.editableNum*i+1].current(self.modelInfo["pantaList"][i])
            if self.editableNum == 3:
                trainWidget.comboList[self.editableNum*i+2].update()
                trainWidget.comboList[self.editableNum*i+2].current(self.modelInfo["colList"][i])

class editStageInfo(sd.Dialog):
    global decryptFile
    global cb
    global trainWidget

    def __init__(self, master, title):
        super(editStageInfo, self).__init__(parent=master, title=title)

    def body(self, master):
        self.train_1pLb = Label(master, text="1P", font=("", 14))
        self.train_1pLb.grid(row=0, column=1, sticky=W+E)
        self.train_2pLb = Label(master, text="2P", font=("", 14))
        self.train_2pLb.grid(row=0, column=2, sticky=W+E)
        self.train_3pLb = Label(master, text="3P", font=("", 14))
        self.train_3pLb.grid(row=0, column=3, sticky=W+E)

        self.trainList = []

        trackComboList = ["標準軌", "狭軌"]

        if v_radio.get() > BS:
            self.trackLb = Label(master, text="台車", font=("", 14))
            self.trackLb.grid(row=0, column=4, sticky=W+E)
            
        stageStartIdx = decryptFile.stageEditIdx
        self.trainComboList = copy.deepcopy(decryptFile.trainNameList)
        self.trainComboList.append("なし")
        for i in range(decryptFile.stageCnt):
            info = decryptFile.stageList[stageStartIdx+i]
            self.stageLb = Label(master, text="{0}ステージ".format(i+1), font=("", 14))
            self.stageLb.grid(row=i+1, column=0, sticky=W+E)

            self.train_1pCb = ttk.Combobox(master, font=("", 14), width=8, value=self.trainComboList)
            self.train_1pCb.grid(row=i+1, column=1, sticky=W+E)
            self.train_1pCb.current(info[1])
            self.trainList.append(self.train_1pCb)
            self.train_2pCb = ttk.Combobox(master, font=("", 14), width=8, value=self.trainComboList)
            self.train_2pCb.grid(row=i+1, column=2, sticky=W+E)
            self.train_2pCb.current(info[2])
            self.trainList.append(self.train_2pCb)
            self.train_3pCb = ttk.Combobox(master, font=("", 14), width=8, value=self.trainComboList)
            self.train_3pCb.grid(row=i+1, column=3, sticky=W+E)
            if info[3] == -1:
                self.train_3pCb.current(len(self.trainComboList)-1)
            else:
                self.train_3pCb.current(info[3])
            self.trainList.append(self.train_3pCb)

            if v_radio.get() > BS:
                self.trackCb = ttk.Combobox(master, font=("", 14), width=8, value=trackComboList)
                self.trackCb.grid(row=i+1, column=4, sticky=W+E)
                self.trackCb.current(info[4])
                self.trainList.append(self.trackCb)

    def validate(self):
        warnMsg = "ステージ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            index = decryptFile.stageIdx
            stageAllCnt = decryptFile.byteArr[index]
            index += 1
            stageList = decryptFile.stageList

            infoCnt = 4
            if v_radio.get() == BS:
                infoCnt = 3

            for i in range(decryptFile.stageCnt):
                train_1pCb = self.trainList[infoCnt*i].current()
                if train_1pCb == len(self.trainComboList)-1:
                    train_1pCb = -1
                stageList[decryptFile.stageEditIdx+i][1] = train_1pCb

                train_2pCb = self.trainList[infoCnt*i+1].current()
                if train_2pCb == len(self.trainComboList)-1:
                    train_2pCb = -1
                stageList[decryptFile.stageEditIdx+i][2] = train_2pCb

                train_3pCb = self.trainList[infoCnt*i+2].current()
                if train_3pCb == len(self.trainComboList)-1:
                    train_3pCb = -1
                stageList[decryptFile.stageEditIdx+i][3] = train_3pCb

                if v_radio.get() > BS:
                    trackCb = self.trainList[infoCnt*i+3].current()
                    stageList[decryptFile.stageEditIdx+i][4] = trackCb

            decryptFile.stageList = stageList

            for i in range(stageAllCnt):
                if v_radio.get() > BS:
                    index += 2
                else:
                    index += 1

                if stageList[i][1] == -1:
                    decryptFile.byteArr[index] = 0xFF
                else:
                    decryptFile.byteArr[index] = stageList[i][1]
                index += 1

                if stageList[i][2] == -1:
                    decryptFile.byteArr[index] = 0xFF
                else:
                    decryptFile.byteArr[index] = stageList[i][2]
                index += 1

                if stageList[i][3] == -1:
                    decryptFile.byteArr[index] = 0xFF
                else:
                    decryptFile.byteArr[index] = stageList[i][3]
                index += 1

                if v_radio.get() > BS:
                    decryptFile.byteArr[index] = stageList[i][4]
                    index += 1
            return True

    def apply(self):
        errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
        if not decryptFile.saveTrain():
            decryptFile.printError()
            mb.showerror(title="保存エラー", message=errorMsg)
        else:
            mb.showinfo(title="成功", message="ステージ設定を修正しました")
            

class allEdit(sd.Dialog):
    global decryptFile
    global notchContentCnt
    
    def body(self, master):
        self.eleLb = Label(master, text="要素", width=5, font=("", 14))
        self.eleLb.grid(row=0, column=0, sticky=N+S, padx=3)
        self.v_ele = StringVar()
        self.eleCb = ttk.Combobox(master, textvariable=self.v_ele, width=24, value=decryptFile.trainPerfNameList)
        self.eleCb.grid(row=0, column=1, sticky=N+S, padx=3)
        self.v_ele.set(decryptFile.trainPerfNameList[0])

        self.allLb = Label(master, text="を全部", width=5, font=("", 14))
        self.allLb.grid(row=0, column=2, sticky=N+S, padx=3)

        self.v_num = DoubleVar()
        self.v_num.set(1.0)
        self.numEt = Entry(master, textvariable=self.v_num, width=6, font=("", 14), justify="right")
        self.numEt.grid(row=0, column=3, sticky=N+S, padx=3)
        self.numLb = Label(master, text="倍にする", width=8, font=("", 14))
        self.numLb.grid(row=0, column=4, sticky=N+S, padx=3)

    def buttonbox(self):
        box = Frame(self, padx=5, pady=5)
        self.okBtn = Button(box, text="OK", width=10, command=self.allEdit)
        self.okBtn.grid(row=0, column=0, padx=5)
        self.cancelBtn = Button(box, text="Cancel", width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=1, padx=5)
        box.pack()

    def allEdit(self):
        try:
            result = float(self.v_num.get())
            warnMsg = "全車両同じ倍率で変更され、すぐ保存されます。\nそれでもよろしいですか？"
            result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)
            
            if result:
                perfIndex = self.eleCb.current()
                self.ok()
                num = self.v_num.get()

                for index in decryptFile.indexList:
                    idx = index
                    notchCnt = decryptFile.byteArr[index]
                    idx += 1
                    #speed
                    for i in range(notchCnt):
                        idx += 4
                    #tlk
                    for i in range(notchCnt):
                        idx += 4
                    if notchContentCnt > 2:
                        #sound
                        for i in range(notchCnt):
                            idx += 1
                        #add
                        for i in range(notchCnt):
                            idx += 4

                    idx = idx + 4*perfIndex

                    originPerf = struct.unpack("<f", decryptFile.byteArr[idx:idx+4])[0]
                    originPerfparentFrame *= num

                    perf = struct.pack("<f", originPerf)
                    for n in perf:
                        decryptFile.byteArr[idx] = n
                        idx += 1

                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                if not decryptFile.saveTrain():
                    decryptFile.printError()
                    mb.showerror(title="保存エラー", message=errorMsg)
                else:
                    mb.showinfo(title="成功", message="全車両を改造しました")
                    reloadFile()
                    
        except:
            errorMsg = "数字で入力してください。"
            mb.showerror(title="数字エラー", message=errorMsg, parent=self)
        

def openFile():
    global decryptFile
    global notchContentCnt

    if v_radio.get() == LS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            notchContentCnt = 2
            decryptFile = dendLs.LSdecrypt(file_path)
    elif v_radio.get() == BS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA2ND.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            notchContentCnt = 2
            decryptFile = dendBs.BSdecrypt(file_path)
    elif v_radio.get() == CS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA3RD.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            notchContentCnt = 4
            decryptFile = dendCs.CSdecrypt(file_path)
    elif v_radio.get() == RS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            notchContentCnt = 4
            decryptFile = dendRs.RSdecrypt(file_path)

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if file_path:        
        if not decryptFile.open():
            decryptFile.printError()
            mb.showerror(title="エラー", message=errorMsg)
            return
        
        deleteWidget()
        initSelect(v_radio.get())
        edit_button["command"] = editTrain

def initSelect(value):
    global decryptFile
    
    cb['values'] = decryptFile.trainNameList
    cb.current(0)
    cb['state'] = 'readonly'

    edit_button['state'] = 'normal'
    edit_all_button['state'] = 'normal'
    edit_stage_train_button['state'] = 'normal'

    speed = decryptFile.trainInfoList[0]
    perf = decryptFile.trainInfoList[1]
    if decryptFile.trainHurikoNameList != "":
        huriko = decryptFile.trainInfoList[2]
    else:
        huriko = ""
    modelInfo = decryptFile.trainModelList[0]
    createWidget(speed, perf, huriko, modelInfo)

def selectTrain(idx):
    try:
        global decryptFile
        if decryptFile.trainHurikoNameList != "":
            speed = decryptFile.trainInfoList[3*idx]
            perf = decryptFile.trainInfoList[3*idx+1]
            huriko = decryptFile.trainInfoList[3*idx+2]
        else:
            speed = decryptFile.trainInfoList[2*idx]
            perf = decryptFile.trainInfoList[2*idx+1]
            huriko = ""
        modelInfo = decryptFile.trainModelList[idx]
        deleteWidget()
        createWidget(speed, perf, huriko, modelInfo)
    except:
        errorMsg = "選択エラー！データが最新のものではない可能性があります。"
        mb.showerror(title="選択エラー", message=errorMsg)

def createWidget(speed, perf, huriko, modelInfo):
    global decryptFile
    global notchContentCnt
    global varList
    global btnList
    global frame3
    global trainWidget
    
    width = speedLf.winfo_width()
    height = speedLf.winfo_height()
    frame = Scrollbarframe(speedLf)

    notchCnt = len(speed)//notchContentCnt
    for i in range(notchCnt):
        notchWidget(i, notchCnt, frame.frame, speed)

    frame2 = Scrollbarframe(perfLf)
    perfCnt = len(perf)
    for i in range(perfCnt):
        perfWidget(i, frame2.frame, perf)

    if huriko != "":
        for i in range(len(huriko)):
            hurikoWidget(i, perfCnt, frame2.frame, huriko)

    frame3 = Scrollbarframe(trainLf, True, False)
    trainWidget = trainModelWidget(frame3.frame, frame3.canvas, modelInfo)

def editTrain():
    global decryptFile
    global btnList
    global trainWidget
    for btn in btnList:
        btn['state'] = 'normal'

    trainWidget.notchBtn['state'] = 'normal'
    trainWidget.henseiBtn['state'] = 'normal'
    trainWidget.colorBtn['state'] = 'normal'
    trainWidget.mdlInfoBtn['state'] = 'normal'
    for combo in trainWidget.comboList:
        combo['state'] = 'normal'

    v_edit.set("保存する")
    edit_button["command"] = saveTrain
    cb['state'] = 'disabled'
    edit_all_button['state'] = 'disabled'
    edit_stage_train_button['state'] = 'disabled'

    if v_radio.get() == LS:
        idx = cb.current()
        modelInfo = decryptFile.trainModelList[idx]
        for i in range(len(trainWidget.comboList)):
            if len(modelInfo["pantaNames"]) == 0:
                trainWidget.comboList[i]['state'] = 'disabled'
            else:
                if i % 2 == 0:
                    trainWidget.comboList[i]['state'] = 'disabled'

def editAllTrain():
    global train
    allEdit(root)

def saveTrain():
    global cb
    global v_edit
    global varList
    global btnList
    global trainWidget
    global decryptFile
    global notchContentCnt
    
    v_edit.set("この車両を修正する")
    edit_button["command"] = editTrain
    edit_all_button['state'] = 'normal'
    edit_stage_train_button['state'] = 'normal'
    cb['state'] = 'readonly'
    for btn in btnList:
        btn['state'] = 'disabled'

    trainWidget.notchBtn['state'] = 'disabled'
    trainWidget.henseiBtn['state'] = 'disabled'
    trainWidget.colorBtn['state'] = 'disabled'
    trainWidget.mdlInfoBtn['state'] = 'disabled'
    for combo in trainWidget.comboList:
        combo['state'] = 'disabled'
        
    trainIdx = cb.current()
    index = decryptFile.indexList[trainIdx]

    notchCnt = decryptFile.byteArr[index]
    index += 1
    for i in range(notchCnt):
        speed = struct.pack("<f", varList[notchContentCnt*i].get())
        for n in speed:
            decryptFile.byteArr[index] = n
            index += 1
    for i in range(notchCnt):
        tlk = struct.pack("<f", varList[notchContentCnt*i+1].get())
        for n in tlk:
            decryptFile.byteArr[index] = n
            index += 1
    if notchContentCnt > 2:
        for i in range(notchCnt):
            sound = struct.pack("<c", varList[notchContentCnt*i+2].get().to_bytes(1, 'big'))
            for n in sound:
                decryptFile.byteArr[index] = n
                index += 1
        for i in range(notchCnt):
            add = struct.pack("<f", varList[notchContentCnt*i+3].get())
            for n in add:
                decryptFile.byteArr[index] = n
                index += 1

    perfCnt = len(decryptFile.trainPerfNameList)
    for i in range(perfCnt):
        perf = struct.pack("<f", varList[notchCnt*notchContentCnt+i].get())
        for n in perf:
            decryptFile.byteArr[index] = n
            index += 1
            
    if decryptFile.trainHurikoNameList != "":
        for i in range(2):
            huriko = struct.pack("<c", varList[notchCnt*notchContentCnt+perfCnt+i].get().to_bytes(1, 'big'))
            for n in huriko:
                decryptFile.byteArr[index] = n
                index += 1

    errorMsg = "予想外のエラーです"
    if not decryptFile.saveTrainInfo(trainIdx, index, trainWidget):
        decryptFile.printError()
        mb.showerror(title="保存エラー", message=errorMsg)
        return

    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
    if not decryptFile.saveTrain():
        decryptFile.printError()
        mb.showerror(title="保存エラー", message=errorMsg)
        return
    
    mb.showinfo(title="成功", message="車両を改造しました")
    reloadFile()

def reloadFile():
    global cb
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title="エラー", message=errorMsg)
        return
    
    deleteWidget()
    selectTrain(cb.current())

def deleteWidget():
    global speedLf
    global perfLf
    global trainLf
    global varList
    global btnList
    children = speedLf.winfo_children()
    for child in children:
        child.destroy()

    children = perfLf.winfo_children()
    for child in children:
        child.destroy()

    children = trainLf.winfo_children()
    for child in children:
        child.destroy()
        
    varList = []
    btnList = []
    v_edit.set("この車両を修正する")

def selectGame():
    deleteWidget()
    cb['state'] = 'disabled'
    cb['values'] = []
    cb.set("")
    edit_button['command'] = editTrain
    edit_button['state'] = 'disabled'
    edit_all_button['state'] = 'disabled'
    edit_stage_train_button['state'] = 'disabled'
    v_edit.set("この車両を修正する")

def editStageTrain():
    global decryptFile

    index = decryptFile.stageIdx
    if index == -1:
        errorMsg = "指定車両を変更する機能はありません"
        mb.showerror(title="エラー", message=errorMsg)
        return

    editStageInfo(root, "ステージ情報修正")

root = Tk()
root.title("電車でD LBCR 性能改造 1.5.0")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
root.config(menu=menubar)

cb = ttk.Combobox(root, width=10, state='disabled')
cb.bind('<<ComboboxSelected>>', lambda e: selectTrain(cb.current()))
cb.place(relx=0.05, rely=0.02, relwidth=0.4, height=25)

v_edit = StringVar()
v_edit.set("この車両を修正する")
edit_button = ttk.Button(root, textvariable=v_edit, command=editTrain, state='disabled')
edit_button.place(relx = 0.48, rely=0.02, relwidth=0.2, height=25)

v_all_edit = StringVar()
v_all_edit.set("同じ倍率で全部修正する")
edit_all_button = ttk.Button(root, textvariable=v_all_edit, command=editAllTrain, state='disabled')
edit_all_button.place(relx = 0.48, rely=0.07, relwidth=0.2, height=25)

v_radio = IntVar()

edit_stage_train_button = ttk.Button(root, text="ステージのデフォルト車両変更", command=editStageTrain, state='disabled')
edit_stage_train_button.place(relx = 0.48, rely=0.12, relwidth=0.2, height=25)

lsRb = Radiobutton(root, text="Lightning Stage", command = selectGame, variable=v_radio, value=LS)
lsRb.place(relx=0.7, rely=0.02)

bsRb = Radiobutton(root, text="Burning Stage", command = selectGame, variable=v_radio, value=BS)
bsRb.place(relx=0.85, rely=0.02)

csRb = Radiobutton(root, text="Climax Stage", command = selectGame, variable=v_radio, value=CS)
csRb.place(relx=0.7, rely=0.07)

rsRb = Radiobutton(root, text="Rising Stage", command = selectGame, variable=v_radio, value=RS)
rsRb.select()
rsRb.place(relx=0.85, rely=0.07)

speedLf = ttk.LabelFrame(root, text="速度")
speedLf.place(relx=0.05, rely=0.17, relwidth=0.38, relheight=0.5)

perfLf = ttk.LabelFrame(root, text="性能")
perfLf.place(relx=0.45, rely=0.17, relwidth=0.52, relheight=0.5)

trainLf = ttk.LabelFrame(root, text="車両")
trainLf.place(relx=0.05, rely=0.68, relwidth=0.92, relheight=0.3)

root.mainloop()
