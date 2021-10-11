# -*- coding: utf-8 -*-

import struct
import copy
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

train = []
indexList = []
trainName = []
varList = []
btnList = []
byteArr = []
file_path = ""

CSTrainName = [
    "H2000",
    "H2800",
    "H8200",
    "HS9000",
    "KQ21XX",
    "JR2000",
    "Rapit",
    
    "Old_H2000",
    "Old_H8200",
    
    "Arban21000R",
    "K800",
    "H7001",
    "K8000",
    "H8000",
    "KQ2199",
    "JR223",
    "H2300",
    "AE86",
    "Deki3",
    "K80"
]

RSTrainName = [
    "H2000",
    "Pano",
    "H8200",
    "Mu2000",
    "T50000",
    "T200",
    "DRC",
    
    "X200",
    "H4050",
    "H7011",
    "E233",
    
    "H2800",
    "HS9000",
    "KQ21XX",
    "JR2000",
    "Rapit",
    "Arban21000R",
    "K800",
    "H7001",
    "K8000",
    "H8000",
    "KQ2199",
    "JR223",
    "H2300",
    "AE86",
    "Deki3",
    "K80"
]

perfName = [
    "None_Tlk",
    "Add_Best",
    "UpHill",
    "DownHill",
    "Weight",
    "First_break",
    "【推測】Second_Breake",
    "SpBreake",
    "CompPower",
    "D_Speed",
    "【推測】One_Speed",
    "OutParam",
    "D_Add",
    "D_Add2",
    "【推測】D_AddFrame",
    "未詳",
    "Jump",
    "ChangeFrame",
    "OutRun_Top",
    "OutRun_Other",
    "OutRun_Frame",
    "OutRun_Speed",
    "OutRun_JumpFrame",
    "OutRun_JumpHeight",
    "LightningFullNotch_per",
    "LightningFullNotch_Speed",
    "LightningFullNotch_Frame"
]

hurikoName = [
    "振り子の曲げる段階",
    "振り子の曲げる角度(°)"
]

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
    def __init__(self, i, notchCnt, frame, speed):
        self.notchNum = "ノッチ" + str(i+1)
        self.notchNumLb = Label(frame, text=self.notchNum, font=("", 20), width=10, borderwidth=1, relief="solid")
        self.notchNumLb.grid(rowspan=4, row=4*i, column=0, sticky=N+S)

        self.speedNameLb = Label(frame, text="speed", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.speedNameLb.grid(row=4*i, column=1, sticky=W+E)
        self.varSpeed = DoubleVar()
        self.varSpeed.set(str(speed[i]))
        varList.append(self.varSpeed)
        self.speedLb = Label(frame, textvariable=self.varSpeed, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.speedLb.grid(row=4*i, column=2, sticky=W+E)
        self.speedBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varSpeed, self.varSpeed.get()), state="disabled")
        self.speedBtn.grid(row=4*i, column=3, sticky=W+E)
        btnList.append(self.speedBtn)

        self.tlkNameLb = Label(frame, text="tlk", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.tlkNameLb.grid(row=4*i+1, column=1, sticky=W+E)
        self.varTlk = DoubleVar()
        self.varTlk.set(str(speed[notchCnt + i]))
        varList.append(self.varTlk)
        self.tlkLb = Label(frame, textvariable=self.varTlk, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.tlkLb.grid(row=4*i+1, column=2, sticky=W+E)
        self.tlkBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varTlk, self.varTlk.get()), state="disabled")
        self.tlkBtn.grid(row=4*i+1, column=3, sticky=W+E)
        btnList.append(self.tlkBtn)

        self.soundNameLb = Label(frame, text="sound", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.soundNameLb.grid(row=4*i+2, column=1, sticky=W+E)
        self.varSound = IntVar()
        self.varSound.set(str(speed[notchCnt*2 + i]))
        varList.append(self.varSound)
        self.soundLb = Label(frame, textvariable=self.varSound, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.soundLb.grid(row=4*i+2, column=2, sticky=W+E)
        self.soundBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varSound, self.varSound.get(), True), state="disabled")
        self.soundBtn.grid(row=4*i+2, column=3, sticky=W+E)
        btnList.append(self.soundBtn)
        
        self.addNameLb = Label(frame, text="add", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.addNameLb.grid(row=4*i+3, column=1, sticky=W+E)
        self.varAdd = DoubleVar()
        self.varAdd.set(str(speed[notchCnt*3 + i]))
        varList.append(self.varAdd)
        self.addLb = Label(frame, textvariable=self.varAdd, font=("", 20), width=5, borderwidth=1, relief="solid")
        self.addLb.grid(row=4*i+3, column=2, sticky=W+E)
        self.addBtn = Button(frame, text="修正", font=("", 14), command=lambda:self.editVar(self.varAdd, self.varAdd.get()), state="disabled")
        self.addBtn.grid(row=4*i+3, column=3, sticky=W+E)
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
    def __init__(self, i, frame, perf):
        self.perfNameLb = Label(frame, text=perfName[i], font=("", 20), width=24, borderwidth=1, relief="solid")
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
    def __init__(self, i, perfCnt, frame, huriko):
        self.hurikoNameLb = Label(frame, text=hurikoName[i], font=("", 20), width=24, borderwidth=1, relief="solid")
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
    def body(self, master):
        self.eleLb = Label(master, text="要素", width=5, font=("", 14))
        self.eleLb.grid(row=0, column=0, sticky=N+S, padx=3)
        self.v_ele = StringVar()
        self.eleCb = ttk.Combobox(master, textvariable=self.v_ele, width=24, value=perfName)
        self.eleCb.grid(row=0, column=1, sticky=N+S, padx=3)
        self.v_ele.set(perfName[0])

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
                self.ok()
                num = self.v_num.get()

                for index in indexList:
                    idx = index
                    notchCnt = byteArr[index]
                    idx += 1
                    #speed
                    for i in range(notchCnt):
                        idx += 4
                    #tlk
                    for i in range(notchCnt):
                        idx += 4
                    #sound
                    for i in range(notchCnt):
                        idx += 1
                    #add
                    for i in range(notchCnt):
                        idx += 4

                    selectPerf = self.v_ele.get()
                    perfIndex = perfName.index(selectPerf)
                    idx = idx + 4*perfIndex

                    originPerf = struct.unpack("<f", byteArr[idx:idx+4])[0]
                    originPerf *= num

                    perf = struct.pack("<f", originPerf)
                    for n in perf:
                        byteArr[idx] = n
                        idx += 1

                errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
                try:
                    w = open(file_path, "wb")
                    w.write(byteArr)
                    w.close()
                    mb.showinfo(title="成功", message="全車両を改造しました", parent=self)
                    reloadFile()
                except Exception as e:
                    print(e)
                    mb.showerror(title="保存エラー", message=errorMsg, parent=self)
                    
        except:
            errorMsg = "数字で入力してください。"
            mb.showerror(title="数字エラー", message=errorMsg, parent=self)
        

def openFile():
    global byteArr
    global file_path
    if v_radio.get() == 0:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA3RD.BIN")])
    elif v_radio.get() == 1:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA4TH.BIN")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            file = open(file_path, "rb")
            line = file.read()
            byteArr = bytearray(line)
            try:
                deleteWidget()
            except:
                mb.showerror(title="エラー", message=errorMsg)
            decryptDend(line, v_radio.get())
            file.close()
            initSelect(v_radio.get())
        except Exception as e:
            print(e)
            mb.showerror(title="エラー", message=errorMsg)

def decryptDend(line, value):
    global train
    global indexList
    train = []
    indexList = []
    index = 0
    trainCnt = line[index]
    index += 1

    ######
    if value == 0:
        #[S300], [Yokohama], [S500]のデータは使わない
        trainCnt -= 3
    elif value == 1:
        #[Yuri], [S300]のデータは使わない
        trainCnt -= 2
    ######

    for i in range(trainCnt):
        indexList.append(index)
        train_speed = []
        notchCnt = line[index]
        index += 1
        for j in range(4):
            if j == 2:
                for k in range(notchCnt):
                    train_speed.append(line[index])
                    index += 1
            else:
                for k in range(notchCnt):
                    speed = struct.unpack("<f", line[index:index+4])[0]
                    speed = round(speed, 4)
                    train_speed.append(speed)
                    index += 4
        train.append(train_speed)

        train_perf = []
        for j in range(27):
            perf = struct.unpack("<f", line[index:index+4])[0]
            perf = round(perf, 4)
            train_perf.append(perf)
            index += 4
        train.append(train_perf)
        
        train_huriko = []
        for j in range(2):
            train_huriko.append(line[index])
            index += 1
        train.append(train_huriko)
        
        smfCnt = line[index]
        index += 1
        for j in range(smfCnt):
            b = line[index]
            index += 1
            index += b

        mdlCnt = line[index]
        index += 1

        mdlSmfCnt = line[index]
        index += 1
        for j in range(mdlSmfCnt):
            b = line[index]
            index += 1
            index += b

        ######
        if value == 0:
            for j in range(mdlSmfCnt):
                b = line[index]
                index += 1
                index += b
        elif value == 1:
            colCnt = line[index]
            index += 1
            for j in range(colCnt):
                b = line[index]
                index += 1
                index += b
        ######

        pantaCnt = line[index]
        index += 1
        for j in range(pantaCnt):
            b = line[index]
            index += 1
            index += b
        for j in range(4):
            b = line[index]
            index += 1
            index += b

        #mdlList
        for j in range(mdlCnt):
            index += 1
        #pantaList
        pantaList = []
        for j in range(mdlCnt):
            pantaList.append(line[index])
            index += 1

        ######
        if value == 1:
            #colList
            for j in range(mdlCnt):
                index += 1
        ######
            
        ###
        for j in range(5):
            b = line[index]
            index += 1
            index += b
        ###
        cnta = line[index]
        index += 1
        b = line[index]
        index += 1
        index += b
        ###
        cntb = line[index]
        index += 1
        b = line[index]
        index += 1
        index += b
        ###

        lensCnt = line[index]
        index += 1
        for j in range(lensCnt):
            b = line[index]
            index += 1
            index += b

            b = line[index]
            index += 1
            index += b

            index += 0xC
        ###
        tailCnt = line[index]
        index += 1
        for j in range(tailCnt):
            b = line[index]
            index += 1
            index += b
        ###
        index += 2
        ###
        for j in range(2):
            b = line[index]
            index += 1
            index += b
            b = line[index]
            index += 1
            index += b
            index += 0xC

def initSelect(value):
    global train
    global trainName

    if value == 0:
        trainName = CSTrainName
    elif value == 1:
        trainName = RSTrainName

    cb['values'] = trainName
    v.set(trainName[0])
    cb['state'] = 'readonly'

    edit_button['state'] = 'normal'
    edit_all_button['state'] = 'normal'

    speed = train[0]
    perf = train[1]
    huriko = train[2]
    createWidget(speed, perf, huriko)

def selectTrain(name):
    try:
        global trainName
        idx = trainName.index(name)
        speed = train[3*idx]
        perf = train[3*idx+1]
        huriko = train[3*idx+2]
        deleteWidget()
        createWidget(speed, perf, huriko)
    except:
        errorMsg = "選択エラー！データが最新のものではない可能性があります。"
        mb.showerror(title="選択エラー", message=errorMsg)

def createWidget(speed, perf, huriko):
    global trainName
    global varList
    global btnList
    width = speedLf.winfo_width()
    height = speedLf.winfo_height()
    frame = Scrollbarframe(speedLf)

    notchCnt = len(speed)//4
    for i in range(notchCnt):
        notchWidget(i, notchCnt, frame.frame, speed)

    frame2 = Scrollbarframe(perfLf)
    perfCnt = len(perf)
    for i in range(perfCnt):
        perfWidget(i, frame2.frame, perf)

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
    global byteArr
    v_edit.set("この車両を修正する")
    edit_button["command"] = editTrain
    edit_all_button['state'] = 'normal'
    cb['state'] = 'readonly'
    for btn in btnList:
        btn['state'] = 'disabled'
    idx = trainName.index(v.get())
    index = indexList[idx]

    notchCnt = byteArr[index]
    index += 1
    for i in range(notchCnt):
        speed = struct.pack("<f", varList[4*i].get())
        for n in speed:
            byteArr[index] = n
            index += 1
    for i in range(notchCnt):
        tlk = struct.pack("<f", varList[4*i+1].get())
        for n in tlk:
            byteArr[index] = n
            index += 1
    for i in range(notchCnt):
        sound = struct.pack("<c", varList[4*i+2].get().to_bytes(1, 'big'))
        for n in sound:
            byteArr[index] = n
            index += 1
    for i in range(notchCnt):
        add = struct.pack("<f", varList[4*i+3].get())
        for n in add:
            byteArr[index] = n
            index += 1

    perfCnt = len(perfName)
    for i in range(perfCnt):
        perf = struct.pack("<f", varList[notchCnt*4+i].get())
        for n in perf:
            byteArr[index] = n
            index += 1
    for i in range(2):
        huriko = struct.pack("<c", varList[notchCnt*4+perfCnt+i].get().to_bytes(1, 'big'))
        for n in huriko:
            byteArr[index] = n
            index += 1

    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
    try:
        w = open(file_path, "wb")
        w.write(byteArr)
        w.close()
        mb.showinfo(title="成功", message="車両を改造しました")
        reloadFile()
    except Exception as e:
        print(e)
        mb.showerror(title="保存エラー", message=errorMsg)

def reloadFile():
    global byteArr
    global file_path
    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            file = open(file_path, "rb")
            line = file.read()
            byteArr = bytearray(line)
            try:
                deleteWidget()
            except:
                mb.showerror(title="エラー", message=errorMsg)
            decryptDend(line, v_radio.get())
            file.close()
            selectTrain(v.get())
        except Exception as e:
            print(e)
            mb.showerror(title="エラー", message=errorMsg)

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
root.title("電車でD CS RS 性能改造 1.1.2")
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
csRb = Radiobutton(root, text="Climax Stage", command = selectGame, variable=v_radio, value=0)
csRb.place(relx=0.7, rely=0.02)

rsRb = Radiobutton(root, text="Rising Stage", command = selectGame, variable=v_radio, value=1)
rsRb.select()
rsRb.place(relx=0.85, rely=0.02)

speedLf = ttk.LabelFrame(root, text="速度")
speedLf.place(relx=0.05, rely=0.12, relwidth=0.38, relheight=0.8)

perfLf = ttk.LabelFrame(root, text="性能")
perfLf.place(relx=0.45, rely=0.12, relwidth=0.52, relheight=0.8)

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

root.mainloop()
