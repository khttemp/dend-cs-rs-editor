# -*- coding: utf-8 -*-

import struct
import copy
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from dendDecrypt import LSdecrypt as dendLs
from dendDecrypt import CSdecrypt as dendCs
from dendDecrypt import RSdecrypt as dendRs

decryptFile = None
notchContentCnt = 0
varList = []
btnList = []

LS = 0
BS = 1
CS = 2
RS = 3

class Scrollbarframe():
    def __init__(self, parent):
        self.canvas = Canvas(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.frame = Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollbar = Scrollbar(parent, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack()

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
                    originPerf *= num

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

def initSelect(value):
    global decryptFile
    
    cb['values'] = decryptFile.trainNameList
    v.set(decryptFile.trainNameList[0])
    cb['state'] = 'readonly'

    edit_button['state'] = 'normal'
    edit_all_button['state'] = 'normal'

    speed = decryptFile.trainInfoList[0]
    perf = decryptFile.trainInfoList[1]
    if decryptFile.trainHurikoNameList != "":
        huriko = decryptFile.trainInfoList[2]
    else:
        huriko = ""
    createWidget(speed, perf, huriko)

def selectTrain(name):
    global decryptFile
    try:
        idx = decryptFile.trainNameList.index(name)
        if decryptFile.trainHurikoNameList != "":
            speed = decryptFile.trainInfoList[3*idx]
            perf = decryptFile.trainInfoList[3*idx+1]
            huriko = decryptFile.trainInfoList[3*idx+2]
        else:
            speed = decryptFile.trainInfoList[2*idx]
            perf = decryptFile.trainInfoList[2*idx+1]
            huriko = ""
        deleteWidget()
        createWidget(speed, perf, huriko)
    except:
        errorMsg = "選択エラー！データが最新のものではない可能性があります。"
        mb.showerror(title="選択エラー", message=errorMsg)

def createWidget(speed, perf, huriko):
    global decryptFile
    global notchContentCnt
    global varList
    global btnList
    
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

def editTrain():
    global btnList
    for btn in btnList:
        btn['state'] = 'normal'

    v_edit.set("保存する")
    edit_button["command"] = saveTrain
    cb['state'] = 'disabled'
    edit_all_button['state'] = 'disabled'

def editAllTrain():
    global train
    allEdit(root)

def saveTrain():
    global v
    global v_edit
    global varList
    global btnList
    global decryptFile
    global notchContentCnt
    
    v_edit.set("この車両を修正する")
    edit_button["command"] = editTrain
    edit_all_button['state'] = 'normal'
    cb['state'] = 'readonly'
    for btn in btnList:
        btn['state'] = 'disabled'
    idx = decryptFile.trainNameList.index(v.get())
    index = decryptFile.indexList[idx]

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

    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
    if not decryptFile.saveTrain():
        decryptFile.printError()
        mb.showerror(title="保存エラー", message=errorMsg)
    else:
        mb.showinfo(title="成功", message="車両を改造しました")
        reloadFile()

def reloadFile():
    global v
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if not decryptFile.open():
        decryptFile.printError()
        mb.showerror(title="エラー", message=errorMsg)
        return
    
    deleteWidget()
    selectTrain(v.get())

def deleteWidget():
    global speedLf
    global perfLf
    global varList
    global btnList
    children = speedLf.winfo_children()
    for child in children:
        child.destroy()

    children = perfLf.winfo_children()
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
    v_edit.set("この車両を修正する")
        
root = Tk()
root.title("電車でD LS CS RS 性能改造 1.2.0")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
root.config(menu=menubar)

v = StringVar()
cb = ttk.Combobox(root, textvariable=v, width=10, state='disabled')
cb.bind('<<ComboboxSelected>>', lambda e: selectTrain(v.get()))
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

lsRb = Radiobutton(root, text="Lightning Stage", command = selectGame, variable=v_radio, value=0)
lsRb.place(relx=0.7, rely=0.02)

csRb = Radiobutton(root, text="Climax Stage", command = selectGame, variable=v_radio, value=2)
csRb.place(relx=0.7, rely=0.07)

rsRb = Radiobutton(root, text="Rising Stage", command = selectGame, variable=v_radio, value=3)
rsRb.select()
rsRb.place(relx=0.85, rely=0.07)

speedLf = ttk.LabelFrame(root, text="速度")
speedLf.place(relx=0.05, rely=0.12, relwidth=0.38, relheight=0.8)

perfLf = ttk.LabelFrame(root, text="性能")
perfLf.place(relx=0.45, rely=0.12, relwidth=0.52, relheight=0.8)

root.mainloop()
