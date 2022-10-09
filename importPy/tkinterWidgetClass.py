from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

from importPy.tkinterEditClass import *

LS = 0
BS = 1
CS = 2
RS = 3

class NotchWidget():
    def __init__(self, root, cbIdx, i, notchCnt, frame, speed, decryptFile, notchContentCnt, varList, btnList, defaultData):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData
        
        self.notchNum = "ノッチ" + str(i+1)
        self.notchNumLb = Label(frame, text=self.notchNum, font=("", 20), width=10, borderwidth=1, relief="solid")
        self.notchNumLb.grid(rowspan=self.notchContentCnt, row=self.notchContentCnt*i, column=0, sticky=N+S)

        try:
            color = ""
            if self.defaultData[self.cbIdx]["notch"][i] < speed[i]:
                color = "red"
            elif self.defaultData[self.cbIdx]["notch"][i] > speed[i]:
                color = "blue"
            else:
                color = "black"
            speedDefaultValue = self.defaultData[self.cbIdx]["notch"][i]
        except:
            color = "green"
            speedDefaultValue = None

        self.speedNameLb = Label(frame, text="speed", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.speedNameLb.grid(row=self.notchContentCnt*i, column=1, sticky=W+E)
        self.varSpeed = DoubleVar()
        self.varSpeed.set(str(speed[i]))        
        
        self.varList.append(self.varSpeed)
        self.speedLb = Label(frame, textvariable=self.varSpeed, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.speedLb.grid(row=self.notchContentCnt*i, column=2, sticky=W+E)
        self.speedBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar([self.speedNameLb, self.speedLb], self.varSpeed, self.varSpeed.get(), speedDefaultValue), state="disabled")
        self.speedBtn.grid(row=self.notchContentCnt*i, column=3, sticky=W+E)
        self.btnList.append(self.speedBtn)

        self.speedNameLb["fg"] = color
        self.speedLb["fg"] = color

        try:
            color = ""
            if self.defaultData[self.cbIdx]["tlk"][i] < speed[notchCnt + i]:
                color = "red"
            elif self.defaultData[self.cbIdx]["tlk"][i] > speed[notchCnt + i]:
                color = "blue"
            else:
                color = "black"
            tlkDefaultValue = self.defaultData[self.cbIdx]["tlk"][i]
        except:
            color = "green"
            tlkDefaultValue = None

        self.tlkNameLb = Label(frame, text="tlk", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.tlkNameLb.grid(row=self.notchContentCnt*i+1, column=1, sticky=W+E)
        self.varTlk = DoubleVar()
        self.varTlk.set(str(speed[notchCnt + i]))
        self.varList.append(self.varTlk)
        self.tlkLb = Label(frame, textvariable=self.varTlk, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.tlkLb.grid(row=self.notchContentCnt*i+1, column=2, sticky=W+E)
        self.tlkBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar([self.tlkNameLb, self.tlkLb], self.varTlk, self.varTlk.get(), tlkDefaultValue), state="disabled")
        self.tlkBtn.grid(row=self.notchContentCnt*i+1, column=3, sticky=W+E)
        self.btnList.append(self.tlkBtn)
            
        self.tlkNameLb["fg"] = color
        self.tlkLb["fg"] = color

        if self.notchContentCnt > 2:
            try:
                color = ""
                if self.defaultData[self.cbIdx]["soundNum"][i] < speed[notchCnt*2 + i]:
                    color = "red"
                elif self.defaultData[self.cbIdx]["soundNum"][i] > speed[notchCnt*2 + i]:
                    color = "blue"
                else:
                    color = "black"
                soundDefaultValue = self.defaultData[self.cbIdx]["soundNum"][i]
            except:
                color = "green"
                soundDefaultValue = None
                
            self.soundNameLb = Label(frame, text="sound", font=("", 20), width=5, borderwidth=1, relief="solid")
            self.soundNameLb.grid(row=self.notchContentCnt*i+2, column=1, sticky=W+E)
            self.varSound = IntVar()
            self.varSound.set(str(speed[notchCnt*2 + i]))
            self.varList.append(self.varSound)
            self.soundLb = Label(frame, textvariable=self.varSound, font=("", 20), width=5, borderwidth=1, relief="solid")
            self.soundLb.grid(row=self.notchContentCnt*i+2, column=2, sticky=W+E)
            self.soundBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar([self.soundNameLb, self.soundLb], self.varSound, self.varSound.get(), soundDefaultValue, True), state="disabled")
            self.soundBtn.grid(row=self.notchContentCnt*i+2, column=3, sticky=W+E)
            self.btnList.append(self.soundBtn)

            self.soundNameLb["fg"] = color
            self.soundLb["fg"] = color

            try:
                color = ""
                if self.defaultData[self.cbIdx]["add"][i] < speed[notchCnt*3 + i]:
                    color = "red"
                elif self.defaultData[self.cbIdx]["add"][i] > speed[notchCnt*3 + i]:
                    color = "blue"
                else:
                    color = "black"
                addDefaultValue = self.defaultData[self.cbIdx]["add"][i]
            except:
                color = "green"
                addDefaultValue = None
                
            self.addNameLb = Label(frame, text="add", font=("", 20), width=5, borderwidth=1, relief="solid")
            self.addNameLb.grid(row=self.notchContentCnt*i+3, column=1, sticky=W+E)
            self.varAdd = DoubleVar()
            self.varAdd.set(str(speed[notchCnt*3 + i]))
            self.varList.append(self.varAdd)
            self.addLb = Label(frame, textvariable=self.varAdd, font=("", 20), width=5, borderwidth=1, relief="solid")
            self.addLb.grid(row=self.notchContentCnt*i+3, column=2, sticky=W+E)
            self.addBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar([self.addNameLb, self.addLb], self.varAdd, self.varAdd.get(), addDefaultValue), state="disabled")
            self.addBtn.grid(row=self.notchContentCnt*i+3, column=3, sticky=W+E)
            self.btnList.append(self.addBtn)

            self.addNameLb["fg"] = color
            self.addLb["fg"] = color

    def editVar(self, labelList, var, value, defaultValue, flag = False):
        EditVarInfo(self.root, "値変更", labelList, var, value, defaultValue, flag)

class PerfWidget():
    def __init__(self, root, cbIdx, i, frame, perf, decryptFile, varList, btnList, defaultData):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData
        
        self.perfNameLb = Label(frame, text=self.decryptFile.trainPerfNameList[i], font=("", 20), width=24, borderwidth=1, relief="solid")
        self.perfNameLb.grid(row=i, column=0, sticky=W+E)
        self.varPerf = DoubleVar()
        self.varPerf.set(str(perf[i]))
        self.varList.append(self.varPerf)
        self.perfLb = Label(frame, textvariable=self.varPerf, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.perfLb.grid(row=i, column=1, sticky=W+E)
        self.perfBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar([self.perfNameLb, self.perfLb], self.varPerf, self.varPerf.get(), self.defaultData[self.cbIdx]["att"][i]), state="disabled")
        self.perfBtn.grid(row=i, column=2, sticky=W+E)
        self.btnList.append(self.perfBtn)

        color = ""
        if self.defaultData[self.cbIdx]["att"][i] < perf[i]:
            color = "red"
        elif self.defaultData[self.cbIdx]["att"][i] > perf[i]:
            color = "blue"
        else:
            color = "black"
        self.perfNameLb["fg"] = color
        self.perfLb["fg"] = color

    def editVar(self, labelList, var, value, defaultValue, flag = False):
        EditVarInfo(self.root, "値変更", labelList, var, value, defaultValue, flag)


class HurikoWidget():
    def __init__(self, root, cbIdx, i, perfCnt, frame, huriko, decryptFile, varList, btnList, defaultData):
        self.root = root
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.varList = varList
        self.btnList = btnList
        self.defaultData = defaultData
        
        self.hurikoNameLb = Label(frame, text=self.decryptFile.trainHurikoNameList[i], font=("", 20), width=24, borderwidth=1, relief="solid")
        self.hurikoNameLb.grid(row=perfCnt+i, column=0, sticky=W+E)
        self.varHuriko = IntVar()
        self.varHuriko.set(str(huriko[i]))
        self.varList.append(self.varHuriko)
        self.hurikoLb = Label(frame, textvariable=self.varHuriko, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.hurikoLb.grid(row=perfCnt+i, column=1, sticky=W+E)
        self.hurikoBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar([self.hurikoNameLb, self.hurikoLb], self.varHuriko, self.varHuriko.get(), self.defaultData[self.cbIdx]["huriko"][i]), state="disabled")
        self.hurikoBtn.grid(row=perfCnt+i, column=2, sticky=W+E)
        self.btnList.append(self.hurikoBtn)

        color = ""
        if self.defaultData[self.cbIdx]["huriko"][i] < huriko[i]:
            color = "red"
        elif self.defaultData[self.cbIdx]["huriko"][i] > huriko[i]:
            color = "blue"
        else:
            color = "black"
        self.hurikoNameLb["fg"] = color
        self.hurikoLb["fg"] = color

    def editVar(self, labelList, var, value, defaultValue, flag = True):
        EditVarInfo(self.root, "値変更", labelList, var, value, defaultValue, flag)


class TrainModelWidget():
    def __init__(self, root, cbIdx, game, frame, canvas, modelInfo, decryptFile, notchContentCnt, funcList):
        self.root = root
        self.cbIdx = cbIdx
        self.game = game
        self.frame = frame
        self.modelInfo = modelInfo
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.funcList = funcList
        
        self.txtFrame = Frame(self.frame, padx=5, pady=5)
        self.txtFrame.place(relx=0, rely=0)
        self.notchLb = Label(self.txtFrame, text="ノッチ", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.notchLb.grid(row=0, column=0, sticky=W+E)

        index = self.decryptFile.indexList[self.cbIdx]
        notchNum = self.decryptFile.byteArr[index]
        
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

        self.mdlFrame = Frame(self.frame, padx=5, pady=5)
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
        if self.game in [LS, BS]:
            title = ""
            if self.game == LS:
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
                    if result < 0:
                        errorMsg = "0以上の数字で入力してください。"
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
        result = EditNotchInfo(self.root, "ノッチ情報修正", self.cbIdx, self.game, self.decryptFile, self.notchContentCnt)
        if result.reloadFlag:
            for func in self.funcList:
                func()

    def editHenseiVar(self, var, value):
        result = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if result:
            result = int(result)
            if result <= 0:
                errorMsg = "1以上の数字で入力してください。"
                mb.showerror(title="数字エラー", message=errorMsg)
                return
            
            oldCnt = var.get()
            editableNum = len(self.comboList) // oldCnt
            var.set(result)
            
            modelInfo = self.decryptFile.trainModelList[self.cbIdx]

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
            if self.game == LS:
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

            mb.showinfo(title="成功", message="編成数を修正しました\n保存するボタンで編成を確定します")

    def editModel(self):
        if self.game not in [LS, BS]:
            EditModelInfo(self.root, "モデル情報修正", self.cbIdx, self.decryptFile, self)
        else:
            title = ""
            if self.game == LS:
                title = "LS"
            else:
                title = "BS"
            errorMsg = "{0}はモデル修正をサポートしません".format(title)
            mb.showerror(title="エラー", message=errorMsg)
