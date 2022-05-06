# -*- coding: utf-8 -*-

import struct

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
    "add",
    "未詳",
    "未詳",
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
    "D_Speed",
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
                perf = round(perf, 4)
                train_perf.append(perf)
                index += 4
            self.trainInfoList.append(train_perf)

            daishaCnt = line[index]
            index += 1

            daishaModelNameCnt = line[index]
            index += 1
            daishaModelName = line[index:index+daishaModelNameCnt].decode("shift-jis")
            index += daishaModelNameCnt

            henseiCnt = line[index]
            index += 1

            for j in range(3):
                modelNameCnt = line[index]
                index += 1
                modelName = line[index:index+modelNameCnt].decode("shift-jis")
                index += modelNameCnt

            for j in range(3):
                colNameCnt = line[index]
                index += 1
                colName = line[index:index+colNameCnt].decode("shift-jis")
                index += colNameCnt

            pantaModelCnt = line[index]
            index += 1

            if pantaModelCnt > 0:
                for j in range(pantaModelCnt):
                    pantaModelNameCnt = line[index]
                    index += 1
                    pantaModelName = line[index:index+pantaModelNameCnt].decode("shift-jis")
                    index += pantaModelNameCnt
                
                for j in range(henseiCnt):
                    idx = line[index]
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
    def saveTrain(self):
        try:
            w = open(self.filePath, "wb")
            w.write(self.byteArr)
            w.close()
            return True
        except Exception as e:
            self.error = str(e)
            return False
