# -*- coding: utf-8 -*-

import struct
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from importPy.tkinterScrollbarFrameClass import *
from importPy.tkinterWidgetClass import *

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

defaultData = []

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("dendData"), relative_path)

def defaultDataRead(game):
    global defaultData

    defaultData = []
    path = ""
    if game == LS:
        path = resource_path("LSdata.txt")
    elif game == BS:
        path = resource_path("BSdata.txt")
    elif game == CS:
        path = resource_path("CSdata.txt")
    elif game == RS:
        path = resource_path("RSdata.txt")

    f = open(path)
    lines = f.readlines()
    f.close()

    count = 1
    mdlCnt = int(lines[0])
    for i in range(mdlCnt):
        name = lines[count].split("\t")[0]
        count += 1

        notchs = [round(float(f), 4) for f in lines[count].split("\t")]
        count += 3

        tlks = [round(float(f), 4) for f in lines[count].split("\t")]
        count += 3

        if game >= CS:
            soundNums = [int(i) for i in lines[count].split("\t")]
            count += 1
            adds = [round(float(f), 4) for f in lines[count].split("\t")]
            count += 3

        attNames = lines[count].split("\t")
        count += 1
        atts = [round(float(f), 5) for f in lines[count].split("\t")]
        count += 3

        if game >= CS:
            hurikos = [int(i) for i in lines[count].split("\t")]
            count += 1

        if game >= CS:
            defaultData.append(
                {
                    "name":name,
                    "notch":notchs,
                    "tlk":tlks,
                    "soundNum":soundNums,
                    "add":adds,
                    "att":atts,
                    "huriko":hurikos,
                })
        else:
            defaultData.append(
                {
                    "name":name,
                    "notch":notchs,
                    "tlk":tlks,
                    "att":atts,
                })

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
            defaultDataRead(LS)
    elif v_radio.get() == BS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA2ND.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            notchContentCnt = 2
            decryptFile = dendBs.BSdecrypt(file_path)
            defaultDataRead(BS)
    elif v_radio.get() == CS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA3RD.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            notchContentCnt = 4
            decryptFile = dendCs.CSdecrypt(file_path)
            defaultDataRead(CS)
    elif v_radio.get() == RS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = None
            notchContentCnt = 4
            decryptFile = dendRs.RSdecrypt(file_path)
            defaultDataRead(RS)

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
    copy_train_info_button['state'] = 'normal'
    set_default_train_info_button['state'] = 'normal'

    speed = decryptFile.trainInfoList[0]
    perf = decryptFile.trainInfoList[1]
    if decryptFile.trainHurikoNameList != "":
        huriko = decryptFile.trainInfoList[2]
    else:
        huriko = ""
    modelInfo = decryptFile.trainModelList[0]
    createWidget(speed, perf, huriko, modelInfo)

def selectTrain(idx):
    global decryptFile
    
    try:
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

    cbIdx = cb.current()
    width = speedLf.winfo_width()
    height = speedLf.winfo_height()
    frame = ScrollbarFrame(speedLf)

    notchCnt = len(speed)//notchContentCnt
    for i in range(notchCnt):
        NotchWidget(root, cbIdx, i, notchCnt, frame.frame, speed, decryptFile, notchContentCnt, varList, btnList, defaultData)

    frame2 = ScrollbarFrame(perfLf)
    perfCnt = len(perf)
    for i in range(perfCnt):
        PerfWidget(root, cbIdx, i, frame2.frame, perf, decryptFile, varList, btnList, defaultData)

    if huriko != "":
        for i in range(len(huriko)):
            HurikoWidget(root, cbIdx, i, perfCnt, frame2.frame, huriko, decryptFile, varList, btnList, defaultData)

    frame3 = ScrollbarFrame(trainLf, True, False)
    game = v_radio.get()
    trainWidget = TrainModelWidget(root, cbIdx, game, frame3.frame, frame3.canvas, modelInfo, decryptFile, notchContentCnt, [reloadFile, editTrain])

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
    copy_train_info_button['state'] = 'disabled'
    set_default_train_info_button['state'] = 'disabled'

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
    result = AllEdit(root, "全車両の性能を一括修正", decryptFile, notchContentCnt)
    if result.reloadFlag:
        reloadFile()

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
    copy_train_info_button['state'] = 'normal'
    set_default_train_info_button['state'] = 'normal'
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

    errorMsg = "保存に失敗しました。\nファイルが他のプログラムによって開かれている\nまたは権限問題の可能性があります"
    if not decryptFile.saveTrainInfo(trainIdx, varList, trainWidget):
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

def selectGame():
    deleteWidget()
    cb['state'] = 'disabled'
    cb['values'] = []
    cb.set("")
    edit_button['command'] = editTrain
    edit_button['state'] = 'disabled'
    edit_all_button['state'] = 'disabled'
    edit_stage_train_button['state'] = 'disabled'
    copy_train_info_button['state'] = 'disabled'
    set_default_train_info_button['state'] = 'disabled'
    v_edit.set("この車両を修正する")

def editStageTrain():
    global decryptFile

    index = decryptFile.stageIdx
    if index == -1:
        errorMsg = "指定車両を変更する機能はありません"
        mb.showerror(title="エラー", message=errorMsg)
        return

    game = v_radio.get()
    EditStageInfo(root, "ステージ情報修正", game, decryptFile)

def copyTrainInfo():
    global decryptFile
    result = TrainInfoEdit(root, "車両性能をコピー", decryptFile)
    if result.reloadFlag:
        reloadFile()

def setDefault():
    global decryptFile
    global defaultData
    result = SetDefaultEdit(root, "車両の性能をデフォルトに戻す", decryptFile, defaultData)
    if result.reloadFlag:
        reloadFile()

root = Tk()
root.title("電車でD LBCR 性能改造 1.7.1")
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

copy_train_info_button = ttk.Button(root, text="車両の性能をコピー", command=copyTrainInfo, state='disabled')
copy_train_info_button.place(relx = 0.05, rely=0.12, relwidth=0.15, height=25)

set_default_train_info_button = ttk.Button(root, text="車両の性能をデフォルトに戻す", command=setDefault, state='disabled')
set_default_train_info_button.place(relx = 0.28, rely=0.12, relwidth=0.15, height=25)

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
