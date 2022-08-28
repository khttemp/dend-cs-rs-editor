# -*- coding: utf-8 -*-

import struct

BSTrainName = [
    "H2000",
    "K8000",
    "H8200",
    "UV21000",
    "H8008",
    "K2199",
    "K21XX",
    "H7001",
    "K800",
    "JR223",
]

perfName = [
    "None_Tlk",
    "add",
    "UpHill",
    "DownHill",
    "Weight",
    "First_break",
    "【推測】Second_Breake",
    "【推測】SpBreake",
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
]

hurikoName = ""

class BSdecrypt():
    def __init__(self, filePath):
        self.filePath = filePath
        self.trainNameList = BSTrainName
        self.trainPerfNameList = perfName
        self.trainHurikoNameList = hurikoName
        self.trainInfoList = []
        self.indexList = []
        self.byteArr = []
        self.error = ""
        self.trainModelList = []
        self.colorIdx = -1
        self.stageIdx = -1
        self.stageList = []
        self.stageEditIdx = 0
        self.stageCnt = 6

    def open(self):
        try:
            f = open(self.filePath, "rb")
            line = f.read()
            f.close()
            self.decrypt(line)
            self.byteArr = bytearray(line)
            return True
        except Exception as e:
            self.error = str(e)
            return False
    def printError(self):
        f = open("error_log.txt", "w")
        f.write(self.error)
        f.close()
    def decrypt(self, line):
        self.trainInfoList = []
        self.indexList = []
        self.error = ""
        self.trainModelList = []
        self.stageList = []
        
        index = 0
        trainCnt = line[index]
        index += 1

        for i in range(trainCnt):
            trainNameCnt = line[index]
            index += 1
            trainName = line[index:index+trainNameCnt].decode("shift-jis")
            index += trainNameCnt

            self.indexList.append(index)
            train_speed = []
            notchCnt = int(line[index])
            index += 1
            for j in range(2):
                for k in range(notchCnt):
                    speed = struct.unpack("<f", line[index:index+4])[0]
                    speed = round(speed, 4)
                    train_speed.append(speed)
                    index += 4
            self.trainInfoList.append(train_speed)

            train_perf = []
            for j in range(len(perfName)):
                perf = struct.unpack("<f", line[index:index+4])[0]
                perf = round(perf, 5)
                train_perf.append(perf)
                index += 4
            self.trainInfoList.append(train_perf)

            train = {
                "trackNames":[],
                "mdlCnt":0,
                "mdlNames":[],
                "colNames":[],
                "pantaNames":[],
                "mdlList":[],
                "pantaList":[],
                "colList":[],
                "colorCnt":0
            }
            
            daishaCnt = line[index]
            index += 1

            daishaModelNameCnt = line[index]
            index += 1
            daishaModelName = line[index:index+daishaModelNameCnt].decode("shift-jis")
            train["trackNames"].append(daishaModelName)
            index += daishaModelNameCnt

            henseiCnt = line[index]
            train["mdlCnt"] = henseiCnt
            index += 1

            modelCnt = line[index]
            index += 1
            for j in range(modelCnt):
                modelNameCnt = line[index]
                index += 1
                modelName = line[index:index+modelNameCnt].decode("shift-jis")
                train["mdlNames"].append(modelName)
                index += modelNameCnt

            train["mdlNames"].append("なし")

            for j in range(modelCnt):
                colNameCnt = line[index]
                index += 1
                colName = line[index:index+colNameCnt].decode("shift-jis")
                train["colNames"].append(colName)
                index += colNameCnt

            train["colNames"].append("なし")

            pantaModelCnt = line[index]
            index += 1
            
            if pantaModelCnt > 0:
                for j in range(pantaModelCnt):
                    pantaModelNameCnt = line[index]
                    index += 1
                    pantaModelName = line[index:index+pantaModelNameCnt].decode("shift-jis")
                    train["pantaNames"].append(pantaModelName)
                    index += pantaModelNameCnt

                train["pantaNames"].append("なし")
                    
            #mdlList
            for j in range(henseiCnt):
                idx = line[index]
                if idx == 0xFF:
                    train["mdlList"].append(-1)
                else:
                    train["mdlList"].append(idx)
                index += 1

            if pantaModelCnt > 0:
                for j in range(henseiCnt):
                    idx = line[index]
                    if idx == 0xFF:
                        train["pantaList"].append(-1)
                    else:
                        train["pantaList"].append(idx)
                    index += 1

            for j in range(2):
                seLen = line[index]
                index += 1
                seFileName = line[index:index+seLen].decode("shift-jis")
                index += seLen

            seLen = line[index]
            index += 1
            seFileName = line[index:index+seLen].decode("shift-jis")
            index += seLen

            sstLen = line[index]
            index += 1
            sstFileName = line[index:index+sstLen].decode("shift-jis")
            index += sstLen

            seLen = line[index]
            index += 1
            seFileName = line[index:index+seLen].decode("shift-jis")
            index += seLen

            for j in range(2):
                seFileCnt = line[index]
                index += 1
                seLen = line[index]
                index += 1
                seFileName = line[index:index+seLen].decode("shift-jis")
                index += seLen

            cnt = line[index]
            index += 1
            for j in range(cnt):
                for k in range(2):
                    tgaLen = line[index]
                    index += 1
                    tgaFileName = line[index:index+tgaLen].decode("shift-jis")
                    index += tgaLen
                for k in range(2):
                    index += 4
                index += 4
                
            tailModelCnt = line[index]
            index += 1
            for j in range(tailModelCnt):
                tailModelNameCnt = line[index]
                index += 1
                tailModelName = line[index:index+tailModelNameCnt].decode("shift-jis")
                index += tailModelNameCnt

            for j in range(tailModelCnt):
                index += 1

            for j in range(tailModelCnt):
                for k in range(2):
                    tgaLen = line[index]
                    index += 1
                    tgaFileName = line[index:index+tgaLen].decode("shift-jis")
                    index += tgaLen
                for k in range(2):
                    index += 4
                index += 4

            for j in range(modelCnt):
                index += 1

            #カラー設定は設定しているモデルに依存
            colorCnt = line[index]
            train["colorCnt"] = colorCnt
            index += 1
            for color in range(colorCnt):
                for model in range(modelCnt):
                    cnt = line[index]
                    index += 1
                    for j in range(cnt):
                        index += 1
                        index += 1
                        txtLen = line[index]
                        index += 1
                        txt = line[index:index+txtLen].decode("shift-jis")
                        index += txtLen

            self.trainModelList.append(train)
        self.stageIdx = index
        
        stageCnt = line[index]
        index += 1
        for i in range(stageCnt):
            stageNum = line[index]
            index += 1
            train_1pIdx = line[index]
            if train_1pIdx == 0xFF:
                train_1pIdx = -1
            index += 1
            train_2pIdx = line[index]
            if train_2pIdx == 0xFF:
                train_2pIdx = -1
            index += 1
            train_3pIdx = line[index]
            if train_3pIdx == 0xFF:
                train_3pIdx = -1
            index += 1
            self.stageList.append([stageNum, train_1pIdx, train_2pIdx, train_3pIdx])
    def saveNotchInfo(self, trainIdx, newNotchNum):
        try:
            newByteArr = bytearray()
            index = self.indexList[trainIdx]
            speed = self.trainInfoList[2*trainIdx]
            notchContentCnt = 2
            oldNotchNum = len(speed) // notchContentCnt

            diff = newNotchNum - oldNotchNum
            newSpeed = []
            if diff <= 0:
                for i in range(notchContentCnt):
                    for j in range(newNotchNum):
                        newSpeed.append(speed[oldNotchNum * i + j])
            else:
                for i in range(notchContentCnt):
                    for j in range(oldNotchNum):
                        newSpeed.append(speed[oldNotchNum * i + j])
                    for j in range(diff):
                        newSpeed.append(0)
            
            newByteArr.extend(self.byteArr[0:index])
            newByteArr.append(newNotchNum)
            index += 1
            
            for i in range(len(newSpeed)):
                byteF = struct.pack("<f", newSpeed[i])
                newByteArr.extend(byteF)
            
            for i in range(len(speed)):
                index += 4

            newByteArr.extend(self.byteArr[index:])
            self.byteArr = newByteArr
            return True
        except Exception as e:
            self.error = str(e)
            return False
    def saveTrainInfo(self, trainIdx, index, trainWidget):
        try:            
            modelInfo = self.trainModelList[trainIdx]
            daishaCnt = self.byteArr[index]
            index += 1

            daishaModelNameCnt = self.byteArr[index]
            index += 1
            index += daishaModelNameCnt
###
            newByteArr = bytearray()
            newByteArr.extend(self.byteArr[0:index])

            newCnt = modelInfo["mdlCnt"]
            newByteArr.append(newCnt)
###
            oldCnt = self.byteArr[index]
            index += 1

            startIdx = index

            modelCnt = self.byteArr[index]
            index += 1
            for j in range(modelCnt):
                modelNameCnt = self.byteArr[index]
                index += 1
                index += modelNameCnt

            for j in range(modelCnt):
                colNameCnt = self.byteArr[index]
                index += 1
                index += colNameCnt

            pantaModelCnt = self.byteArr[index]
            index += 1
            
            if pantaModelCnt > 0:
                for j in range(pantaModelCnt):
                    pantaModelNameCnt = self.byteArr[index]
                    index += 1
                    index += pantaModelNameCnt

            newByteArr.extend(self.byteArr[startIdx:index])
###
            #mdlList
            for i in range(newCnt):
                idx = trainWidget.comboList[2*i].current()
                if idx == len(trainWidget.comboList[2*i]["values"])-1:
                    idx = 255
                newByteArr.append(idx)

            #pantaList
            if pantaModelCnt > 0:
                for i in range(newCnt):
                    idx = trainWidget.comboList[2*i+1].current()
                    if idx == len(trainWidget.comboList[2*i+1]["values"])-1:
                        idx = 255
                    newByteArr.append(idx)
###
            #mdlList
            for i in range(oldCnt):
                index += 1
            #pantaList
            for i in range(oldCnt):
                index += 1
###
            newIndex = len(newByteArr)
            newByteArr.extend(self.byteArr[index:])
            diff = newIndex - index
            index = newIndex

            self.byteArr = newByteArr
            return True
        except Exception as e:
            self.error = str(e)
            return False
    def saveTrain(self):
        try:
            w = open(self.filePath, "wb")
            w.write(self.byteArr)
            w.close()
            return True
        except Exception as e:
            self.error = str(e)
            return False
