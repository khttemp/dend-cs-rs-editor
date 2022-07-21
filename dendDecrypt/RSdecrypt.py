# -*- coding: utf-8 -*-

import struct

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

class RSdecrypt():
    def __init__(self, filePath):
        self.filePath = filePath
        self.trainNameList = RSTrainName
        self.trainPerfNameList = perfName
        self.trainHurikoNameList = hurikoName
        self.trainInfoList = []
        self.indexList = []
        self.byteArr = []
        self.error = ""
        self.trainModelList = []
        self.colorIdx = 0

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
        
        index = 0
        trainCnt = line[index]
        index += 1

        for i in range(trainCnt):
            self.indexList.append(index)
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
            self.trainInfoList.append(train_speed)

            train_perf = []
            for j in range(len(perfName)):
                perf = struct.unpack("<f", line[index:index+4])[0]
                perf = round(perf, 4)
                train_perf.append(perf)
                index += 4
            self.trainInfoList.append(train_perf)
            
            train_huriko = []
            for j in range(2):
                train_huriko.append(line[index])
                index += 1
            self.trainInfoList.append(train_huriko)

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
            
            smfTrackCnt = line[index]
            index += 1
            for j in range(smfTrackCnt):
                b = line[index]
                index += 1
                train["trackNames"].append(line[index:index+b].decode("shift-jis"))
                index += b

            mdlCnt = line[index]
            train["mdlCnt"] = mdlCnt
            index += 1

            mdlSmfCnt = line[index]
            index += 1
            for j in range(mdlSmfCnt):
                b = line[index]
                index += 1
                train["mdlNames"].append(line[index:index+b].decode("shift-jis"))
                index += b

            train["mdlNames"].append("なし")

            colCnt = line[index]
            index += 1
            for j in range(colCnt):
                b = line[index]
                index += 1
                train["colNames"].append(line[index:index+b].decode("shift-jis"))
                index += b

            train["colNames"].append("なし")

            pantaCnt = line[index]
            index += 1
            for j in range(pantaCnt):
                b = line[index]
                index += 1
                train["pantaNames"].append(line[index:index+b].decode("shift-jis"))
                index += b

            train["pantaNames"].append("なし")
                
            for j in range(4):
                b = line[index]
                index += 1
                index += b

            #mdlList
            for j in range(mdlCnt):
                if line[index] == 0xFF:
                    train["mdlList"].append(-1)
                else:
                    train["mdlList"].append(line[index])
                index += 1
            #pantaList
            for j in range(mdlCnt):
                if line[index] == 0xFF:
                    train["pantaList"].append(-1)
                else:
                    train["pantaList"].append(line[index])
                index += 1

            #colList
            for j in range(mdlCnt):
                if line[index] == 0xFF:
                    train["colList"].append(-1)
                else:
                    train["colList"].append(line[index])
                index += 1

            for j in range(5):
                b = line[index]
                index += 1
                index += b

            cnta = line[index]
            index += 1
            b = line[index]
            index += 1
            index += b

            cntb = line[index]
            index += 1
            b = line[index]
            index += 1
            index += b
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
            tailCnt = line[index]
            index += 1
            
            for j in range(tailCnt):
                b = line[index]
                index += 1
                index += b
            index += 2
            
            for j in range(2):
                b = line[index]
                index += 1
                index += b
                b = line[index]
                index += 1
                index += b
                index += 0xC

            self.trainModelList.append(train)

        self.colorIdx = index
        for i in range(len(RSTrainName)+2):
            trainName = ""
            if i == len(RSTrainName):
                trainName = "Yuri"
            elif i == len(RSTrainName)+1:
                trainName = "S300"
            else:
                trainName = RSTrainName[i]
                self.trainModelList[i]["colorCnt"] = line[index]
            index += 1
    def saveTrainInfo(self, trainIdx, index, trainWidget):
        try:
            newByteArr = bytearray()
            newByteArr.extend(self.byteArr[0:index])
            
            modelInfo = self.trainModelList[trainIdx]
            newTrackList = modelInfo["trackNames"]
            
            newByteArr.append(len(newTrackList))
            for newTrack in newTrackList:
                newByteArr.append(len(newTrack))
                newByteArr.extend(newTrack.encode("shift-jis"))

            newCnt = modelInfo["mdlCnt"]
            newByteArr.append(newCnt)

            newMdlList = trainWidget.comboList[0]
            newPantaList = trainWidget.comboList[1]
            newColList = trainWidget.comboList[2]

            newByteArr.append(len(newMdlList["value"])-1)
            for newMdl in newMdlList["value"]:
                if newMdl == "なし":
                    continue
                newByteArr.append(len(newMdl))
                newByteArr.extend(newMdl.encode("shift-jis"))

            newByteArr.append(len(newColList["value"])-1)
            for newCol in newColList["value"]:
                if newCol == "なし":
                    continue
                newByteArr.append(len(newCol))
                newByteArr.extend(newCol.encode("shift-jis"))
            
            newByteArr.append(len(newPantaList["value"])-1)
            for newPanta in newPantaList["value"]:
                if newPanta == "なし":
                    continue
                newByteArr.append(len(newPanta))
                newByteArr.extend(newPanta.encode("shift-jis"))

###
            smfTrackCnt = self.byteArr[index]
            index += 1

            for i in range(smfTrackCnt):
                b = self.byteArr[index]
                index += 1
                index += b

            oldCnt = self.byteArr[index]
            index += 1

            mdlSmfCnt = self.byteArr[index]
            index += 1
            for i in range(mdlSmfCnt):
                b = self.byteArr[index]
                index += 1
                index += b

            colCnt = self.byteArr[index]
            index += 1
            for i in range(colCnt):
                b = self.byteArr[index]
                index += 1
                index += b

            pantaCnt = self.byteArr[index]
            index += 1
            for i in range(pantaCnt):
                b = self.byteArr[index]
                index += 1
                index += b
###
            startIdx = index
            for i in range(4):
                b = self.byteArr[index]
                index += 1
                index += b
            newByteArr.extend(self.byteArr[startIdx:index])
###
            for i in range(newCnt):
                idx = trainWidget.comboList[3*i].current()
                if idx == len(trainWidget.comboList[3*i]["values"])-1:
                    idx = 255
                newByteArr.append(idx)

            for i in range(newCnt):
                idx = trainWidget.comboList[3*i+1].current()
                if idx == len(trainWidget.comboList[3*i+1]["values"])-1:
                    idx = 255
                newByteArr.append(idx)

            for i in range(newCnt):
                idx = trainWidget.comboList[3*i+2].current()
                if idx == len(trainWidget.comboList[3*i+2]["values"])-1:
                    idx = 255
                newByteArr.append(idx)
                
###
            #mdlList
            for i in range(oldCnt):
                index += 1
            #pantaList
            for i in range(oldCnt):
                index += 1
            #colList
            for i in range(oldCnt):
                index += 1

###
            newIndex = len(newByteArr)
            newByteArr.extend(self.byteArr[index:])
            diff = newIndex - index
            index = newIndex
###
            colorCnt = trainWidget.varColor.get()
            colorIdx = diff + self.colorIdx + trainIdx
            newByteArr[colorIdx] = colorCnt

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
