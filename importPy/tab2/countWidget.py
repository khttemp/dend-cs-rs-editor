from tkinter import *
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

LS = 0
BS = 1
CS = 2
RS = 3

class CountWidget():
    def __init__(self, root, trainIdx, game, frame, decryptFile, reloadFunc):
        self.root = root
        self.trainIdx = trainIdx
        self.game = game
        self.frame = frame
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        self.reloadFunc = reloadFunc

        index = self.decryptFile.indexList[self.trainIdx]
        notchNum = self.decryptFile.byteArr[index]
        
        modelInfo = self.decryptFile.trainModelList[self.trainIdx]

        self.countFrame = ttk.Frame(self.frame)
        self.countFrame.pack(anchor=NW, side=LEFT, padx=15, pady=5)

        self.notchLb = Label(self.countFrame, text="ノッチ", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.notchLb.grid(row=0, column=0, sticky=W+E)
        self.varNotch = IntVar()
        self.varNotch.set(notchNum)
        self.notchTextLb = Label(self.countFrame, textvariable=self.varNotch, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.notchTextLb.grid(row=0, column=1, sticky=W+E)
        self.notchBtn = Button(self.countFrame, text="修正", font=("", 14), command=lambda:self.editNotchVar(self.varNotch, self.varNotch.get()))
        self.notchBtn.grid(row=0, column=2, sticky=W+E)
        
        self.henseiLb = Label(self.countFrame, text="編成数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.henseiLb.grid(row=1, column=0, sticky=W+E)
        self.varHensei = IntVar()
        self.varHensei.set(modelInfo["mdlCnt"])
        self.henseiTextLb = Label(self.countFrame, textvariable=self.varHensei, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.henseiTextLb.grid(row=1, column=1, sticky=W+E)
        self.henseiBtn = Button(self.countFrame, text="修正", font=("", 14), command=lambda:self.editHenseiVar(self.varHensei, self.varHensei.get()))
        self.henseiBtn.grid(row=1, column=2, sticky=W+E)

        self.colorLb = Label(self.countFrame, text="カラー数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.colorLb.grid(row=2, column=0, sticky=W+E)
        self.varColor = IntVar()
        self.varColor.set(modelInfo["colorCnt"])
        self.colorTextLb = Label(self.countFrame, textvariable=self.varColor, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.colorTextLb.grid(row=2, column=1, sticky=W+E)
        self.colorBtn = Button(self.countFrame, text="修正", font=("", 14), command=lambda:self.editVar(self.varColor, self.varColor.get()))
        self.colorBtn.grid(row=2, column=2, sticky=W+E)

    def editNotchVar(self, var, value):
        result = EditNotchInfo(self.root, "ノッチ情報修正", self.trainIdx, self.game, self.decryptFile, self.notchContentCnt)
        if result.reloadFlag:
            self.reloadFunc()

    def editHenseiVar(self, var, value):
        resultValue = sd.askstring(title="値変更", prompt="値を入力してください", initialvalue=value)

        if resultValue:
            try:
                try:
                    resultValue = int(resultValue)
                except:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return
                
                if resultValue <= 0:
                    errorMsg = "1以上の数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return

                if resultValue < value:
                    msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                    result = mb.askokcancel(title="警告", message=msg, icon="warning")
                    if not result:
                        return

                if not self.decryptFile.saveHenseiNum(self.trainIdx, resultValue):
                    self.decryptFile.printError()
                    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False

                mb.showinfo(title="成功", message="編成数を修正しました")
                self.reloadFunc()
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

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
                except:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return
                    
                if result < 0:
                    errorMsg = "0以上の数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
                    return

                if not self.decryptFile.saveColor(self.trainIdx, result):
                    self.decryptFile.printError()
                    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                    mb.showerror(title="保存エラー", message=errorMsg)
                    return False

                mb.showinfo(title="成功", message="カラー数を修正しました")
                self.reloadFunc()
                
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)
    
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

class EditNotchInfo(sd.Dialog):
    def __init__(self, master, title, trainIdx, game, decryptFile, notchContentCnt):
        self.trainIdx = trainIdx
        self.game = game
        self.decryptFile = decryptFile
        self.notchContentCnt = notchContentCnt
        self.reloadFlag = False
        super(EditNotchInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        index = self.decryptFile.indexList[self.trainIdx]
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

            if not self.decryptFile.saveNotchInfo(self.trainIdx, newNotchNum):
                self.decryptFile.printError()
                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                mb.showerror(title="保存エラー", message=errorMsg)
                return False
            else:
                return True
    def apply(self):
        mb.showinfo(title="成功", message="ノッチ数を変更しました")
        self.reloadFlag = True

class EditModelInfo(sd.Dialog):
    def __init__(self, master, title, trainIdx, decryptFile, trainWidget):
        self.trainIdx = trainIdx
        self.decryptFile = decryptFile
        self.trainWidget = trainWidget
        super(EditModelInfo, self).__init__(parent=master, title=title)

    def body(self, frame):
        modelInfo = self.decryptFile.trainModelList[self.trainIdx]

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
                if self.modelInfo["mdlList"][i] != -1:
                    self.trainWidget.comboList[self.editableNum*i].current(self.modelInfo["mdlList"][i])
                self.trainWidget.comboList[self.editableNum*i+1].update()

                if self.modelInfo["pantaList"][i] != -1:
                    self.trainWidget.comboList[self.editableNum*i+1].current(self.modelInfo["pantaList"][i])

                if self.editableNum == 3:
                    self.trainWidget.comboList[self.editableNum*i+2].update()
                    if self.modelInfo["colList"][i] != -1:
                        self.trainWidget.comboList[self.editableNum*i+2].current(self.modelInfo["colList"][i])
            return True

    def apply(self):
        mb.showinfo(title="成功", message="モデルリストを修正しました\n保存するボタンで確定します")
