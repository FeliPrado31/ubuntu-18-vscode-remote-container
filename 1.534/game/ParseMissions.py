#coding: utf-8
import random, os, sys
from struct import *

class ByteArray:
    def __init__(this, bytes=b""):
        reload(sys)
        sys.setdefaultencoding("ISO-8859-1")
        if type(bytes) == str:
            try:
                bytes = bytes.encode()
            except Exception as e:
                print(e)
                print("error on encode packet str to bytes")
        this.bytes = bytes

    def writeByte(this, value):
        this.write(pack("!B", int(value) & 0xFF))
        return this

    def writeShort(this, value):
        this.write(pack("!H", int(value) & 0xFFFF))
        return this
    
    def writeInt(this, value):
        this.write(pack("!I", long(value) & 0xFFFFFFFF))
        return this

    def writeBool(this, value):
        return this.writeByte(1 if bool(value) else 0)

    def writeUTF(this, value):
        value = bytes(value.encode())
        this.writeShort(len(value))
        this.write(value)
        return this

    def writeBytes(this, value):
        this.bytes += value
        return this

    def read(this, c = 1):
        found = ""
        if this.getLength() >= c:
            found = this.bytes[:c]
            this.bytes = this.bytes[c:]

        return found

    def write(this, value):
        this.bytes += value
        return this

    def readByte(this):
        value = 0
        if this.getLength() >= 1:
            value = unpack("!B", this.read())[0]
        return value

    def readShort(this):
        value = 0
        if this.getLength() >= 2:
            value = unpack("!H", this.read(2))[0]
        return value

    def readInt(this):
        value = 0
        if this.getLength() >= 4:
            value = unpack("!I", this.read(4))[0]
        return value

    def readUTF(this):
        value = ""
        if this.getLength() >= 2:
            value = this.read(this.readShort()).decode()
        return value

    def readBool(this):
        return this.readByte() > 0

    def readUTFBytes(this, size):
        value = this.bytes[:int(size)]
        this.bytes = this.bytes[int(size):]
        return value

    def getBytes(this):
        return this.bytes

    def toByteArray(this):
        return this.getBytes()

    def getLength(this):
        return len(this.bytes)

    def bytesAvailable(this):
        return this.getLength() > 0


class DailyQuest:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor

        # List
        this.missionCheck = []

        # Boolean
        this.createAccount = False

    def loadDailyQuest(this, createAccount):
        this.createAccount = createAccount
        this.getMissions()
    	this.activeDailyQuest()
        this.updateDailyQuest(True)

    def activeDailyQuest(this):
    	this.client.sendPacket([144, 5], ByteArray().writeBool(True).toByteArray())

    def getMissions(this):
        if this.createAccount:
            ID = 0
            while ID < 3:
                if int(this.client.dailyQuest[ID]) == 0:
                    mission = this.randomMission()
                    if mission[0] == int(this.client.dailyQuest[0]) or int(this.client.dailyQuest[1]) or int(this.client.dailyQuest[2]):
                        mission = this.randomMission()
                    this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [int(mission[0]), this.client.playerID])
                    rs = this.Cursor.fetchone()
                    if not rs:
                        this.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [this.client.playerID, int(mission[0]), int(mission[1]), int(mission[2]), int(mission[3])])
                    this.client.dailyQuest[ID] = int(mission[0])
                    this.client.remainingMissions += 1
                    this.updateDailyQuest(True)
                ID += 1
            this.client.dailyQuest[3] = 1
            this.updateDailyQuest(True)

        this.Cursor.execute("select MissionID from DailyQuest where UserID = %s", [this.client.playerID])
        rs = this.Cursor.fetchall()
        if rs:
            for ms in rs:
                this.missionCheck.append(int(ms[0]))

        for missionID in this.missionCheck:
            if this.checkFinishMission(missionID, this.client.playerID):
                if int(missionID) in this.client.dailyQuest:
                    this.completeMission(missionID, this.client.playerID)
            this.missionCheck.remove(missionID)

    def checkFinishMission(this, missionID, playerID):
        this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
        rs = this.Cursor.fetchone()
        if int(rs[4]) >= int(rs[3]):
            return True
        return False

    def updateDailyQuest(this, alterDB = False):
        if alterDB:
            this.client.updateDatabase()
            
        this.Cursor.execute("select DailyQuest, RemainingMissions from Users where PlayerID = %s", [this.client.playerID])
        rs = this.Cursor.fetchone()
        if rs:
            this.client.remainingMissions = rs[1]
            this.client.dailyQuest = map(str, filter(None, rs[0].split(","))) if rs[0] != "" else [0, 0, 0, 1]

    def randomMission(this):
        missionID = random.randint(1, 7)
        id = 0
        while int(this.client.dailyQuest[id]) == int(missionID):
            missionID = random.randint(1, 7)
            id += 1
        missionType = 0
        reward = random.randint(15, 50)
        collect = random.randint(10, 65)

        if missionID == 2:
            missionType = random.randint(1, 3)

        if missionID == 6:
            collect = 1

        return [missionID, missionType, collect, reward]

    def getMission(this, missionID, playerID):
    	this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
    	rs = this.Cursor.fetchone()
        if rs:
            if int(rs[6]) == 0:
                return [int(missionID), int(rs[2]), int(rs[3]), int(rs[4]), int(rs[5])]
            else:
                return int(rs[4])

    def changeMission(this, missionID, playerID):
        mission = this.randomMission()
        continueChange = False

        while missionID == int(mission[0]):
            mission = this.randomMission()

        if missionID == int(this.client.dailyQuest[0]):
            this.client.dailyQuest[3] = 0
            this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = this.Cursor.fetchone()
            if rs:
                if not mission[0] == int(this.client.dailyQuest[0]) or int(this.client.dailyQuest[1]) or int(this.client.dailyQuest[2]):
                    this.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(this.client.dailyQuest[0]) or int(this.client.dailyQuest[1]) or int(this.client.dailyQuest[2]):
                    this.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    this.client.dailyQuest[0] = mission[0]

        elif missionID == int(this.client.dailyQuest[1]):
            this.client.dailyQuest[3] = 0
            this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = this.Cursor.fetchone()
            if rs:
                if not mission[0] == int(this.client.dailyQuest[0]) or int(this.client.dailyQuest[1]) or int(this.client.dailyQuest[2]):
                    this.client.dailyQuest[1] = this.client.dailyQuest[0]
                    this.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(this.client.dailyQuest[0]) or int(this.client.dailyQuest[1]) or int(this.client.dailyQuest[2]):
                    this.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    this.client.dailyQuest[1] = this.client.dailyQuest[0]
                    this.client.dailyQuest[0] = mission[0]

        elif missionID == int(this.client.dailyQuest[2]):
            this.client.dailyQuest[3] = 0
            this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [mission[0], playerID])
            rs = this.Cursor.fetchone()
            if rs:
                if not mission[0] == int(this.client.dailyQuest[0]) or int(this.client.dailyQuest[1]) or int(this.client.dailyQuest[2]):
                    this.client.dailyQuest[2] = this.client.dailyQuest[1]
                    this.client.dailyQuest[1] = this.client.dailyQuest[0]
                    this.client.dailyQuest[0] = mission[0]
            else:
                if not mission[0] == int(this.client.dailyQuest[0]) or int(this.client.dailyQuest[1]) or int(this.client.dailyQuest[2]):
                    this.Cursor.execute("insert into DailyQuest values (%s, %s, %s, %s, '0', %s, '0')", [playerID, mission[0], mission[1], mission[2], mission[3]])
                    this.client.dailyQuest[2] = this.client.dailyQuest[1]
                    this.client.dailyQuest[1] = this.client.dailyQuest[0]
                    this.client.dailyQuest[0] = mission[0]

        this.updateDailyQuest(True)

    def upMission(this, missionID, playerID):
        this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
        rs = this.Cursor.fetchone()
        if rs:
            this.Cursor.execute("update DailyQuest set QntCollected = QntCollected + 1 where MissionID = %s and UserID = %s", [missionID, playerID])
            this.updateDailyQuest(True)
            this.Cursor.execute("select * from DailyQuest where MissionID = %s and UserID = %s", [missionID, playerID])
            rs = this.Cursor.fetchone()
            if this.checkFinishMission(int(missionID), playerID):
                this.completeMission(int(missionID), playerID)
            else:
                this.client.sendPacket([144, 4], ByteArray().writeShort(missionID).writeByte(0).writeShort(rs[4]).writeShort(rs[3]).writeShort(rs[5]).writeShort(0).toByteArray())

    def completeMission(this, missionID, playerID):
        this.Cursor.execute("select * from DailyQuest where Fraise = '1' and UserID = %s", [playerID])
        rs = this.Cursor.fetchone()
        if rs:
            this.Cursor.execute("update DailyQuest set QntCollected = QntCollected + 1 where Fraise = '1' and UserID = %s", [playerID])
            this.client.cheeseCount += int(rs[5])
            this.client.shopCheeses += int(rs[5])
            #this.client.addConsumable(random.randint(0, 2350), random.randint(0, 5))
            this.client.remainingMissions -= 1
            mission = this.randomMission()
            if missionID == 6:
                mission[2] = 1

            if missionID == int(this.client.dailyQuest[0]):
                this.client.dailyQuest[0] = 0
                this.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            elif missionID == int(this.client.dailyQuest[1]):
                this.client.dailyQuest[1] = 0
                this.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            elif missionID == int(this.client.dailyQuest[2]):
                this.client.dailyQuest[2] = 0
                this.Cursor.execute("update DailyQuest set QntCollected = 0 and QntToCollect = %s and Reward = %s where MissionID = %s and UserID = %s", [mission[2], mission[3], missionID, playerID])

            this.updateDailyQuest(True)
            this.client.sendPacket([144, 4], ByteArray().writeByte(237).writeByte(129).writeByte(0).writeShort(int(rs[4])+1).writeShort(20).writeInt(20).toByteArray())

    def sendDailyQuest(this):
        p = ByteArray()
        p.writeByte(this.client.remainingMissions) # Quantidade de missões

        # Missions
        ID = 0
        while ID < 3:
            if int(this.client.dailyQuest[ID]) != 0:
                mission = this.getMission(int(this.client.dailyQuest[ID]), this.client.playerID)
                p.writeShort(int(mission[0])) # ID da missão
                p.writeByte(int(mission[1])) # Tipo de missão
                p.writeShort(int(mission[3])) # Quantidade coletada
                p.writeShort(int(mission[2])) # Quantidade a coletar
                p.writeShort(int(mission[4])) # Quantidade a receber
                p.writeShort(0)
                p.writeBool(True if bool(int(this.client.dailyQuest[3])) else False) # Substituir missão
            ID += 1

        # 4
        mission4 = this.getMission(237129, this.client.playerID)
        p.writeByte(237)
        p.writeByte(129)
        p.writeByte(0)
        p.writeShort(int(mission4)) # Quantidade coletada
        p.writeShort(20) # Quantidade a coletar
        p.writeInt(20) # Quantidade a receber
        p.writeBool(False) # Substituir missão

        this.client.sendPacket([144, 3], p.toByteArray())
