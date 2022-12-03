from tkinter import *
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

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
        EditNotchVarInfo(self.root, "値変更", labelList, var, value, defaultValue, flag)

class EditNotchVarInfo(sd.Dialog):
    def __init__(self, master, title, labelList, var, value, defaultValue, flag = False):
        self.labelList = labelList
        self.var = var
        self.value = value
        self.defaultValue = defaultValue
        self.flag = flag
        super(EditNotchVarInfo, self).__init__(parent=master, title=title)

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
