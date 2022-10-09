import copy

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

LS = 0
BS = 1
CS = 2
RS = 3

class EditNotchInfo(sd.Dialog):
    def __init__(self, master, title, cbIdx, game, decryptFile, notchContentCnt):
        self.cbIdx = cbIdx
        self.game = game
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.reloadFlag = False
        super(EditNotchInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        index = self.decryptFile.indexList[self.cbIdx]
        notchNum = self.decryptFile.byteArr[index]

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
        if self.game <= BS:
            if self.notchCb.current() == 2:
                mb.showerror(title="エラー", message="12ノッチを対応できません")
                return False
        warnMsg = "ノッチ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            newNotchNum = -1
            notchIdx = self.notchCb.current()
            if notchIdx == 0:
                newNotchNum = 4
            elif notchIdx == 1:
                newNotchNum = 5
            elif notchIdx == 2:
                newNotchNum = 12

            if not self.decryptFile.saveNotchInfo(self.cbIdx, newNotchNum):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            else:
                return True
    def apply(self):
        mb.showinfo(title="成功", message="ノッチ数を変更しました")
        self.reloadFlag = True

class EditVarInfo(sd.Dialog):
    def __init__(self, master, title, labelList, var, value, defaultValue, flag = False):
        self.labelList = labelList
        self.var = var
        self.value = value
        self.defaultValue = defaultValue
        self.flag = flag
        super(EditVarInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        self.defaultLb = Label(frame, text="デフォルトの値＝" + str(self.defaultValue), font=("", 14))
        self.defaultLb.pack()

        sep = ttk.Separator(frame, orient='horizontal')
        sep.pack(fill=X, ipady=5)

        self.inputLb = Label(frame, text="値を入力してください", font=("", 14))
        self.inputLb.pack()

        v_val = StringVar()
        v_val.set(self.value)
        self.inputEt = Entry(frame, textvariable=v_val, font=("", 14))
        self.inputEt.pack()

    def validate(self):
        result = self.inputEt.get()
        if result:
            try:
                if self.flag:
                    try:
                        result = int(result)
                        if result < 0:
                            errorMsg = "0以上の整数で入力してください。"
                            mb.showerror(title="整数エラー", message=errorMsg)
                            return False
                        self.var.set(result)
                    except:
                        errorMsg = "整数で入力してください。"
                        mb.showerror(title="整数エラー", message=errorMsg)
                        return False
                else:
                    try:
                        result = float(result)
                        self.var.set(result)
                    except:
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
                return False

            if self.defaultValue != None:
                color = ""
                if self.defaultValue < result:
                    color = "red"
                elif self.defaultValue > result:
                    color = "blue"
                else:
                    color = "black"

                for label in self.labelList:
                    label["fg"] = color
            return True


class EditModelInfo(sd.Dialog):
    def __init__(self, master, title, cbIdx, decryptFile, trainWidget):
        self.cbIdx = cbIdx
        self.decryptFile = decryptFile
        self.trainWidget = trainWidget
        super(EditModelInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        modelInfo = self.decryptFile.trainModelList[self.cbIdx]

        self.btnFrame = Frame(frame, pady=5)
        self.btnFrame.pack()
        self.listFrame = Frame(frame)
        self.listFrame.pack()

        self.editableNum = len(self.trainWidget.comboList) // modelInfo["mdlCnt"]

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
        cnt = self.trainWidget.varHensei.get()
        
        if self.selectListNum == 0:
            selectName = "台車モデル"
            if self.trackModelList.size() <= 2:
                mb.showerror(title="エラー", message="台車モデルは2個以上である必要あります")
                return
        elif self.selectListNum == 1:
            selectName = "車両モデル"
            for i in range(cnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum*i].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i+1))
                    return
        elif self.selectListNum == 2:
            selectName = "パンタモデル"
            for i in range(cnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum*i+1].current():
                    mb.showerror(title="エラー", message="選択したモデルは{0}両目で使ってます".format(i+1))
                    return
        elif self.selectListNum == 3:
            selectName = "COLモデル"
            for i in range(cnt):
                if self.selectIndex == self.trainWidget.comboList[self.editableNum*i+2].current():
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
            modelInfo = self.decryptFile.trainModelList[self.cbIdx]

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

            cnt = self.trainWidget.varHensei.get()
            
            for i in range(cnt):
                self.trainWidget.comboList[self.editableNum*i]["values"] = newTrainList
                self.trainWidget.comboList[self.editableNum*i+1]["values"] = newPantaList
                if self.editableNum == 3:
                    self.trainWidget.comboList[self.editableNum*i+2]["values"] = newColList

            self.modelInfo = modelInfo

            for i in range(cnt):
                self.trainWidget.comboList[self.editableNum*i].update()
                self.trainWidget.comboList[self.editableNum*i].current(self.modelInfo["mdlList"][i])
                self.trainWidget.comboList[self.editableNum*i+1].update()
                self.trainWidget.comboList[self.editableNum*i+1].current(self.modelInfo["pantaList"][i])
                if self.editableNum == 3:
                    self.trainWidget.comboList[self.editableNum*i+2].update()
                    self.trainWidget.comboList[self.editableNum*i+2].current(self.modelInfo["colList"][i])
            return True

    def apply(self):
        mb.showinfo(title="成功", message="モデルリストを修正しました\n保存するボタンで確定します")

class EditStageInfo(sd.Dialog):
    def __init__(self, master, title, game, decryptFile):
        self.game = game
        self.decryptFile = decryptFile
        super(EditStageInfo, self).__init__(parent=master, title=title)

    def body(self, master):
        self.train_1pLb = Label(master, text="1P", font=("", 14))
        self.train_1pLb.grid(row=0, column=1, sticky=W+E)
        self.train_2pLb = Label(master, text="2P", font=("", 14))
        self.train_2pLb.grid(row=0, column=2, sticky=W+E)
        self.train_3pLb = Label(master, text="3P", font=("", 14))
        self.train_3pLb.grid(row=0, column=3, sticky=W+E)

        self.trainList = []

        trackComboList = ["標準軌", "狭軌"]

        if self.game > BS:
            self.trackLb = Label(master, text="台車", font=("", 14))
            self.trackLb.grid(row=0, column=4, sticky=W+E)
            
        stageStartIdx = self.decryptFile.stageEditIdx
        self.trainComboList = copy.deepcopy(self.decryptFile.trainNameList)
        self.trainComboList.append("なし")
        for i in range(self.decryptFile.stageCnt):
            info = self.decryptFile.stageList[stageStartIdx+i]
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

            if self.game > BS:
                self.trackCb = ttk.Combobox(master, font=("", 14), width=8, value=trackComboList)
                self.trackCb.grid(row=i+1, column=4, sticky=W+E)
                self.trackCb.current(info[4])
                self.trainList.append(self.trackCb)

    def validate(self):
        warnMsg = "ステージ情報を修正しますか？"
        result = mb.askokcancel(message=warnMsg, icon="warning", parent=self)
        if result:
            index = self.decryptFile.stageIdx
            stageAllCnt = self.decryptFile.byteArr[index]
            index += 1
            stageList = self.decryptFile.stageList

            infoCnt = 4
            if self.game == BS:
                infoCnt = 3

            for i in range(self.decryptFile.stageCnt):
                train_1pCb = self.trainList[infoCnt*i].current()
                if train_1pCb == len(self.trainComboList)-1:
                    train_1pCb = -1
                stageList[self.decryptFile.stageEditIdx+i][1] = train_1pCb

                train_2pCb = self.trainList[infoCnt*i+1].current()
                if train_2pCb == len(self.trainComboList)-1:
                    train_2pCb = -1
                stageList[self.decryptFile.stageEditIdx+i][2] = train_2pCb

                train_3pCb = self.trainList[infoCnt*i+2].current()
                if train_3pCb == len(self.trainComboList)-1:
                    train_3pCb = -1
                stageList[self.decryptFile.stageEditIdx+i][3] = train_3pCb

                if self.game > BS:
                    trackCb = self.trainList[infoCnt*i+3].current()
                    stageList[self.decryptFile.stageEditIdx+i][4] = trackCb

            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            if not self.decryptFile.saveStageInfo(stageList):
                self.decryptFile.printError()
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="ステージ設定を修正しました")
            

class AllEdit(sd.Dialog):
    def __init__(self, master, title, decryptFile, notchContentCnt):
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.reloadFlag = False
        super(AllEdit, self).__init__(parent=master, title=title)
    
    def body(self, master):
        self.eleLb = Label(master, text="要素", width=5, font=("", 14))
        self.eleLb.grid(row=0, column=0, sticky=N+S, padx=3)
        self.v_ele = StringVar()
        self.eleCb = ttk.Combobox(master, textvariable=self.v_ele, width=24, value=self.decryptFile.trainPerfNameList)
        self.eleCb.grid(row=0, column=1, sticky=N+S, padx=3)
        self.v_ele.set(self.decryptFile.trainPerfNameList[0])

        self.allLb = Label(master, text="を全部", width=5, font=("", 14))
        self.allLb.grid(row=0, column=2, sticky=N+S, padx=3)

        self.v_num = DoubleVar()
        self.v_num.set(1.0)
        self.numEt = Entry(master, textvariable=self.v_num, width=6, font=("", 14), justify="right")
        self.numEt.grid(row=0, column=3, sticky=N+S, padx=3)

        calcList = ["倍にする", "にする"]
        self.v_ele2 = StringVar()
        self.eleCb2 = ttk.Combobox(master, textvariable=self.v_ele2, font=("", 14), width=8, value=calcList)
        self.v_ele2.set(calcList[0])
        
        self.eleCb2.grid(row=0, column=4, sticky=N+S, padx=3)

    def validate(self):
        try:
            result = float(self.v_num.get())
            if self.eleCb2.current() == 0:
                warnMsg = "全車両同じ倍率で変更され、すぐ保存されます。\nそれでもよろしいですか？"
            else:
                warnMsg = "全車両同じ数値で変更され、すぐ保存されます。\nそれでもよろしいですか？"
            result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)
            
            if result:
                perfIndex = self.eleCb.current()
                num = self.v_num.get()

                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                if not self.decryptFile.saveAllEdit(perfIndex, num, self.eleCb2.current()):
                    self.decryptFile.printError()
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False
                return True
        except:
            errorMsg = "数字で入力してください。"
            mb.showerror(title="数字エラー", message=errorMsg, parent=self)

    def apply(self):
        mb.showinfo(title="成功", message="全車両を改造しました")
        self.reloadFlag = True

class TrainInfoEdit(sd.Dialog):
    def __init__(self, master, title, decryptFile):
        self.decryptFile = decryptFile
        self.reloadFlag = False
        super(TrainInfoEdit, self).__init__(parent=master, title=title)
    
    def body(self, master):
        self.copySrcCb = ttk.Combobox(master, width=12, font=("", 14), value=self.decryptFile.trainNameList)
        self.copySrcCb.grid(row=0, column=0, sticky=N+S, padx=3)
        self.copySrcCb.current(0)

        self.v_info1 = IntVar()
        self.v_info1.set(1)
        self.infoCb = Checkbutton(master, text="ノッチ", font=("", 14), variable=self.v_info1)
        self.infoCb.grid(row=0, column=1, sticky=N+S, padx=3)

        self.v_info2 = IntVar()
        self.v_info2.set(1)
        self.infoCb2 = Checkbutton(master, text="性能", font=("", 14), variable=self.v_info2)
        self.infoCb2.grid(row=1, column=1, sticky=N+S, padx=3)

        self.copyDistCb = ttk.Combobox(master, width=12, font=("", 14), value=self.decryptFile.trainNameList)
        self.copyDistCb.grid(row=2, column=1, sticky=N+S, padx=3)
        self.copyDistCb.current(0)

        self.info2Lb = Label(master, text="にコピーする", width=12, font=("", 14))
        self.info2Lb.grid(row=2, column=2, sticky=N+S, padx=3)

    def validate(self):
        if self.v_info1.get() == 0 and self.v_info2.get() == 0:
            mb.showerror(title="エラー", message="コピー項目を選択してください")
            return False
        srcIdx = self.copySrcCb.current()
        distIdx = self.copyDistCb.current()

        srcIndex = self.decryptFile.indexList[srcIdx]
        srcNotchNum = self.decryptFile.byteArr[srcIndex]
        distIndex = self.decryptFile.indexList[distIdx]
        distNotchNum = self.decryptFile.byteArr[distIndex]

        srcSpeed = None
        distSpeed = None
        srcPerf = None
        distPerf = None
        srcHuriko = None
        distHuriko = None
        warnMsg = ""
        
        if self.decryptFile.trainHurikoNameList != "":
            srcSpeed = self.decryptFile.trainInfoList[3*srcIdx]
            srcPerf = self.decryptFile.trainInfoList[3*srcIdx+1]
            srcHuriko = self.decryptFile.trainInfoList[3*srcIdx+2]
            distSpeed = self.decryptFile.trainInfoList[3*distIdx]
            distPerf = self.decryptFile.trainInfoList[3*distIdx+1]
            distHuriko = self.decryptFile.trainInfoList[3*distIdx+2]
        else:
            srcSpeed = self.decryptFile.trainInfoList[2*srcIdx]
            srcPerf = self.decryptFile.trainInfoList[2*srcIdx+1]
            distSpeed = self.decryptFile.trainInfoList[2*distIdx]
            distPerf = self.decryptFile.trainInfoList[2*distIdx+1]

        if self.v_info1.get() == 1:
            if srcNotchNum > distNotchNum:
                warnMsg += "※{0}のノッチ情報を{1}ノッチまでコピーします。\n".format(self.decryptFile.trainNameList[srcIdx], distNotchNum)
            elif srcNotchNum < distNotchNum:
                warnMsg += "※{0}のノッチ情報を{1}ノッチまでコピーします。\n".format(self.decryptFile.trainNameList[srcIdx], srcNotchNum)

        if self.v_info1.get() == 1:
            warnMsg += "「ノッチ」"
        if self.v_info2.get() == 1:
            warnMsg += "「性能」"
        warnMsg += "を全部コピーしますか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)
            
        if result:
            srcList = [srcIndex, srcNotchNum, srcSpeed, srcPerf, srcHuriko]
            distList = [distIndex, distNotchNum, distSpeed, distPerf, distHuriko]
            checkStatusList = [self.v_info1.get(), self.v_info2.get()]
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            if not self.decryptFile.copyTrainInfo(distIdx, srcList, distList, checkStatusList):
                self.decryptFile.printError()
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True

    def apply(self):
        mb.showinfo(title="成功", message="車両を改造しました")
        self.reloadFlag = True

class SetDefaultEdit(sd.Dialog):
    def __init__(self, master, title, decryptFile, defaultData):
        self.decryptFile = decryptFile
        self.defaultData = defaultData
        self.reloadFlag = False
        super(SetDefaultEdit, self).__init__(parent=master, title=title)
    
    def body(self, master):
        self.copySrcCb = ttk.Combobox(master, width=12, font=("", 14), value=self.decryptFile.trainNameList)
        self.copySrcCb.grid(row=0, column=0, sticky=N+S, padx=3)
        self.copySrcCb.current(0)

        self.v_info1 = IntVar()
        self.v_info1.set(1)
        self.infoCb = Checkbutton(master, text="ノッチ", font=("", 14), variable=self.v_info1)
        self.infoCb.grid(row=0, column=1, sticky=N+S, padx=3)

        self.v_info2 = IntVar()
        self.v_info2.set(1)
        self.infoCb2 = Checkbutton(master, text="性能", font=("", 14), variable=self.v_info2)
        self.infoCb2.grid(row=1, column=1, sticky=N+S, padx=3)

        self.info2Lb = Label(master, text="をデフォルトに戻す", font=("", 14))
        self.info2Lb.grid(row=1, column=2, sticky=N+S, padx=3)

    def validate(self):
        if self.v_info1.get() == 0 and self.v_info2.get() == 0:
            mb.showerror(title="エラー", message="コピー項目を選択してください")
            return False

        srcIdx = self.copySrcCb.current()

        srcIndex = self.decryptFile.indexList[srcIdx]
        srcNotchNum = self.decryptFile.byteArr[srcIndex]
        distData = self.defaultData[srcIdx]
        distNotchNum = len(distData["notch"])

        srcSpeed = None
        srcPerf = None
        srcHuriko = None
        warnMsg = ""
        
        if self.decryptFile.trainHurikoNameList != "":
            srcSpeed = self.decryptFile.trainInfoList[3*srcIdx]
            srcPerf = self.decryptFile.trainInfoList[3*srcIdx+1]
            srcHuriko = self.decryptFile.trainInfoList[3*srcIdx+2]
        else:
            srcSpeed = self.decryptFile.trainInfoList[2*srcIdx]
            srcPerf = self.decryptFile.trainInfoList[2*srcIdx+1]

        if self.v_info1.get() == 1:
            if srcNotchNum > distNotchNum:
                warnMsg += "※{0}のノッチ情報を{1}ノッチまで戻します。\n".format(self.decryptFile.trainNameList[srcIdx], distNotchNum)
            elif srcNotchNum < distNotchNum:
                warnMsg += "※{0}のノッチ情報を{1}ノッチまで戻します。\n".format(self.decryptFile.trainNameList[srcIdx], srcNotchNum)

        if self.v_info1.get() == 1:
            warnMsg += "「ノッチ」"
        if self.v_info2.get() == 1:
            warnMsg += "「性能」"
        warnMsg += "を全部元に戻しますか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning", parent=self)
            
        if result:
            srcList = [srcIndex, srcNotchNum, srcSpeed, srcPerf, srcHuriko]
            checkStatusList = [self.v_info1.get(), self.v_info2.get()]
            errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
            if not self.decryptFile.setDefaultTrainInfo(srcList, distData, checkStatusList):
                self.decryptFile.printError()
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            return True
    def apply(self):
        mb.showinfo(title="成功", message="データを元に戻しました")
        self.reloadFlag = True
