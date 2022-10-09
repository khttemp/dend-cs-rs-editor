# -*- coding: utf-8 -*-

import struct
import traceback

LSTrainName = [
    "H2000",
    "H8200",
    "H2300",
    "JR223",
    "21000R",
    "K800",
    "H7000",
    "DEKI",
    "TAKUMI",
    "K80",
    "S300"
]

perfName = [
    "None_Tlk",
    "add1",
    "add2",
    "add3",
    "UpHill",
    "DownHill",
    "Weight",
    "CompPower",
    "First_break",
    "未詳",
    "Second_Breake",
    "未詳",
    "未詳",
    "未詳",
    "未詳",
    "未詳",
    "未詳",
    "【推測】D_Speed",
    "One_Speed",
    "OutParam",
    "D_Add",
    "未詳",
    "未詳",
    "SpBreake",
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

class LSdecrypt():
    def __init__(self, filePath):
        self.filePath = filePath
        self.trainNameList = LSTrainName
        self.trainPerfNameList = perfName
        self.trainHurikoNameList = hurikoName
        self.trainInfoList = []
        self.indexList = []
        self.byteArr = []
        self.error = ""
        self.trainModelList = []
        self.colorIdx = -1
        self.stageIdx = -1

    def open(self):
        try:
            f = open(self.filePath, "rb")
            line = f.read()
            f.close()
            self.decrypt(line)
            self.byteArr = bytearray(line)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
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

            for j in range(3):
                modelNameCnt = line[index]
                index += 1
                modelName = line[index:index+modelNameCnt].decode("shift-jis")
                train["mdlNames"].append(modelName)
                index += modelNameCnt

            for j in range(3):
                colNameCnt = line[index]
                index += 1
                colName = line[index:index+colNameCnt].decode("shift-jis")
                train["colNames"].append(colName)
                index += colNameCnt

            #LSは固定で自動編成
            for i in range(henseiCnt):
                train["mdlList"].append(1)
            train["mdlList"][0] = 0
            train["mdlList"][-1] = len(train["mdlNames"])-1

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
                
                for j in range(henseiCnt):
                    idx = line[index]
                    if idx == 0xFF:
                        train["pantaList"].append(-1)
                    else:
                        train["pantaList"].append(idx)
                    index += 1

            for j in range(9):
                idx = line[index]
                index += 1

            for j in range(4):
                seLen = line[index]
                index += 1
                seFileName = line[index:index+seLen].decode("shift-jis")
                index += seLen

            seLen = line[index]
            index += 1
            seFileName = line[index:index+seLen].decode("shift-jis")
            index += seLen
            tempF = struct.unpack("<f", line[index:index+4])[0]
            tempF = "%.4f" % (tempF)
            index += 4

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
                    tempF = struct.unpack("<f", line[index:index+4])[0]
                    tempF = "%.4f" % (tempF)
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
                    tempF = struct.unpack("<f", line[index:index+4])[0]
                    tempF = "%.4f" % (tempF)
                    index += 4
                index += 4

            self.trainModelList.append(train)
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

            self.saveTrain()
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False
    def saveTrainInfo(self, trainIdx, varList, trainWidget):
        try:
            index = self.indexList[trainIdx]
            notchCnt = self.byteArr[index]
            index += 1
            
            newByteArr = self.byteArr[0:index]
            notchContentCnt = 2
            
            for i in range(notchCnt):
                speed = struct.pack("<f", varList[notchContentCnt*i].get())
                newByteArr.extend(speed)
                index += 4
            for i in range(notchCnt):
                tlk = struct.pack("<f", varList[notchContentCnt*i+1].get())
                newByteArr.extend(tlk)
                index += 4

            perfCnt = len(self.trainPerfNameList)
            for i in range(perfCnt):
                perf = struct.pack("<f", varList[notchCnt*notchContentCnt+i].get())
                newByteArr.extend(perf)
                index += 4
                
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

            for j in range(3):
                modelNameCnt = self.byteArr[index]
                index += 1
                index += modelNameCnt

            for j in range(3):
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

            #pantaList
            if pantaModelCnt > 0:
                for i in range(newCnt):
                    idx = trainWidget.comboList[2*i+1].current()
                    if idx == len(trainWidget.comboList[2*i+1]["values"])-1:
                        idx = 255
                    newByteArr.append(idx)
###
            #pantaList
            if pantaModelCnt > 0:
                for i in range(oldCnt):
                    index += 1
###
            newIndex = len(newByteArr)
            newByteArr.extend(self.byteArr[index:])
            diff = newIndex - index
            index = newIndex

            self.byteArr = newByteArr

            self.saveTrain()
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def saveAllEdit(self, perfIndex, num, calcIndex):
        try:
            for index in self.indexList:
                idx = index
                notchCnt = self.byteArr[index]
                idx += 1
                #speed
                for i in range(notchCnt):
                    idx += 4
                #tlk
                for i in range(notchCnt):
                    idx += 4

                idx = idx + 4*perfIndex

                originPerf = struct.unpack("<f", self.byteArr[idx:idx+4])[0]
                if calcIndex == 0:
                    originPerf *= num
                else:
                    originPerf = num

                perf = struct.pack("<f", originPerf)
                for n in perf:
                    self.byteArr[idx] = n
                    idx += 1
            self.saveTrain()
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def copyTrainInfo(self, distIdx, srcList, distList, checkStatusList):
        srcIndex=  srcList[0]
        srcNotchNum = srcList[1]
        srcSpeed = srcList[2]
        srcPerf = srcList[3]
        distIndex = distList[0]
        distNotchNum = distList[1]
        distSpeed = distList[2]
        distPerf = distList[3]
        notchCheckStatus = checkStatusList[0]
        perfCheckStatus = checkStatusList[1]
        
        try:
            loopCnt = 0
            if srcNotchNum > distNotchNum:
                loopCnt = distNotchNum
            else:
                loopCnt = srcNotchNum
                
            for i in range(len(distPerf)):
                distPerf[i] = srcPerf[i]
                    
            for i in range(2):
                for j in range(loopCnt):
                    distSpeed[i*distNotchNum+j] = srcSpeed[i*srcNotchNum+j]

            index = self.indexList[distIdx]
            index += 1
            for i in range(distNotchNum):
                if notchCheckStatus:
                    speed = struct.pack("<f", distSpeed[0*distNotchNum+i])
                    for n in speed:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4
            for i in range(distNotchNum):
                if notchCheckStatus:
                    tlk = struct.pack("<f", distSpeed[1*distNotchNum+i])
                    for n in tlk:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4

            perfCnt = len(distPerf)
            for i in range(perfCnt):
                if perfCheckStatus:
                    perf = struct.pack("<f", distPerf[i])
                    for n in perf:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4
                    
            self.saveTrain()
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def setDefaultTrainInfo(self, srcList, distData, checkStatusList):
        srcIndex = srcList[0]
        srcNotchNum = srcList[1]
        srcSpeed = srcList[2]
        srcPerf = srcList[3]
        distNotchNum = len(distData["notch"])
        notchCheckStatus = checkStatusList[0]
        perfCheckStatus = checkStatusList[1]
        
        try:
            loopCnt = 0
            if srcNotchNum > distNotchNum:
                loopCnt = distNotchNum
            else:
                loopCnt = srcNotchNum

            index = srcIndex
            index += 1

            for i in range(len(srcPerf)):
                srcPerf[i] = distData["att"][i]
            
            for i in range(2):
                if i == 0:
                    data = distData["notch"]
                elif i == 1:
                    data = distData["tlk"]
                    
                for j in range(loopCnt):
                    srcSpeed[i*srcNotchNum+j] = data[j]
                    
            for i in range(srcNotchNum):
                if notchCheckStatus:
                    speed = struct.pack("<f", srcSpeed[0*srcNotchNum+i])
                    for n in speed:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4
            for i in range(srcNotchNum):
                if notchCheckStatus:
                    tlk = struct.pack("<f", srcSpeed[1*srcNotchNum+i])
                    for n in tlk:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4

            for i in range(len(distData["att"])):
                if perfCheckStatus:
                    perf = struct.pack("<f", srcPerf[i])
                    for n in perf:
                        self.byteArr[index] = n
                        index += 1
                else:
                    index += 4
                    
            self.saveTrain()
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False
        
    def saveTrain(self):
        w = open(self.filePath, "wb")
        w.write(self.byteArr)
        w.close()
