# -*- coding: utf-8 -*-

import struct
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from importPy.tkinterTab import *
from importPy.tkinterStageWidget import *

from dendDecrypt import LSdecrypt as dendLs
from dendDecrypt import BSdecrypt as dendBs
from dendDecrypt import CSdecrypt as dendCs
from dendDecrypt import RSdecrypt as dendRs

decryptFile = None
varList = []
btnList = []

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
            decryptFile = dendLs.LSdecrypt(file_path)
            defaultDataRead(LS)
    elif v_radio.get() == BS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA2ND.BIN")])
        if file_path:
            del decryptFile
            decryptFile = dendBs.BSdecrypt(file_path)
            defaultDataRead(BS)
    elif v_radio.get() == CS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA3RD.BIN")])
        if file_path:
            del decryptFile
            decryptFile = dendCs.CSdecrypt(file_path)
            defaultDataRead(CS)
    elif v_radio.get() == RS:
        file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "TRAIN_DATA4TH.BIN")])
        if file_path:
            del decryptFile
            decryptFile = dendRs.RSdecrypt(file_path)
            defaultDataRead(RS)

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    if file_path:        
        if not decryptFile.open():
            decryptFile.printError()
            mb.showerror(title="エラー", message=errorMsg)
            return
        
        deleteWidget()
        initSelect()

def initSelect():
    global decryptFile
    
    cb["values"] = decryptFile.trainNameList
    cb.current(0)
    cb["state"] = "readonly"

    menuCb["values"] = ["速度・性能情報", "数・モデル情報", "レンズフレア"]
    menuCb.current(0)
    menuCb["state"] = "readonly"
    selectInfo(cb.current(), menuCb.current())

    edit_stage_train_button["state"] = "normal"

def selectTrain(idx):
    global decryptFile
    
    try:
        selectInfo(idx, menuCb.current())
    except:
        errorMsg = "選択エラー！データが最新のものではない可能性があります。"
        mb.showerror(title="選択エラー", message=errorMsg)

def selectInfo(trainIdx, index):
    global decryptFile
    deleteWidget()

    widgetList = [
        v_edit,
        cb,
        menuCb,
        edit_stage_train_button
    ]
    game = v_radio.get()
    
    if index == 0:
        tab1AllWidget(tabFrame, decryptFile, trainIdx, varList, btnList, defaultData, widgetList, reloadFile)
    elif index == 1:
        tab2AllWidget(tabFrame, decryptFile, trainIdx, game, widgetList, reloadFile)
    elif index == 2:
        tab3AllWidget(tabFrame, decryptFile, trainIdx, game, widgetList, reloadFile)

def deleteWidget():
    global varList
    global btnList
    
    children = tabFrame.winfo_children()
    for child in children:
        child.destroy()
        
    varList = []
    btnList = []

def reloadFile():
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

    menuCb['state'] = 'disabled'
    menuCb['values'] = []
    menuCb.set("")
    
    edit_stage_train_button['state'] = 'disabled'

def editStageTrain():
    global decryptFile

    index = decryptFile.stageIdx
    if index == -1:
        errorMsg = "指定車両を変更する機能はありません"
        mb.showerror(title="エラー", message=errorMsg)
        return

    game = v_radio.get()
    EditStageInfo(root, "ステージ情報修正", game, decryptFile)

root = Tk()
root.title("電車でD LBCR 性能改造 1.8.0")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
root.config(menu=menubar)

cb = ttk.Combobox(root, width=10, state='disabled')
cb.bind('<<ComboboxSelected>>', lambda e: selectTrain(cb.current()))
cb.place(relx=0.05, rely=0.02, relwidth=0.4, height=25)

menuCb = ttk.Combobox(root, width=10, state='disabled')
menuCb.bind('<<ComboboxSelected>>', lambda e: selectInfo(cb.current(), menuCb.current()))
menuCb.place(relx=0.05, rely=0.07, relwidth=0.2, height=25)

v_radio = IntVar()
v_edit = StringVar()

edit_stage_train_button = ttk.Button(root, text="ステージのデフォルト車両変更", command=editStageTrain, state='disabled')
edit_stage_train_button.place(relx = 0.48, rely=0.07, relwidth=0.2, height=25)

lsRb = Radiobutton(root, text="Lightning Stage", command = selectGame, variable=v_radio, value=LS)
lsRb.place(relx=0.48, rely=0.02)

bsRb = Radiobutton(root, text="Burning Stage", command = selectGame, variable=v_radio, value=BS)
bsRb.place(relx=0.61, rely=0.02)

csRb = Radiobutton(root, text="Climax Stage", command = selectGame, variable=v_radio, value=CS)
csRb.place(relx=0.73, rely=0.02)

rsRb = Radiobutton(root, text="Rising Stage", command = selectGame, variable=v_radio, value=RS)
rsRb.select()
rsRb.place(relx=0.85, rely=0.02)

tabFrame = ttk.Frame(root, borderwidth=1, relief="solid")
tabFrame.place(relx=0.03, rely=0.13, relwidth=0.95, relheight=0.84)

root.mainloop()
