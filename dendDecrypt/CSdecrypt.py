# -*- coding: utf-8 -*-

import struct

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

class CSdecrypt():
    def __init__(self, filePath):
        self.filePath = filePath
        self.trainNameList = CSTrainName
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
        index = 0
        trainCnt = line[index]
        index += 1

        #[S300], [Yokohama], [S500]のデータは使わない
        trainCnt -= 3

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

            for j in range(mdlSmfCnt):
                b = line[index]
                index += 1
                index += b

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
    def saveTrain(self):
        try:
            w = open(self.filePath, "wb")
            w.write(self.byteArr)
            w.close()
            return True
        except Exception as e:
            self.error = str(e)
            return False
