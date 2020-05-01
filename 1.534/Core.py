#coding: utf-8
import os, sys, json, time, random, ftplib, MySQLdb, threading, urllib2, binascii, traceback, ConfigParser

# Compilar
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

# Modules
from modules import *
from utils import *

# Outros
from datetime import datetime
from datetime import timedelta
from twisted.internet import reactor, protocol

Database, Cursor = None, None
Database = MySQLdb.connect("74.208.214.173","eal","omaresgei","niu")
Database.isolation_level = None 
Cursor = Database.cursor()
Database.autocommit(True)

class Client(ClientHandler):
    def __init__(this):
        # String
        this.Username = ""
        this.Langue = "BR"
        this.realLangue = "BR"
        this.MouseColor = "78583a"
        this.ShamanColor = "95d9d6"
        this.roomName = ""
        this.shopItems = ""
        this.shamanItems = ""
        this.playerLook = "1;0,0,0,0,0,0,0,0,0"
        this.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        this.lastMessage = ""
        this.modoPwetLangue = "ALL"
        this.silenceMessage = ""
        this.marriage = ""
        this.tribeName = ""
        this.tribeMessage = ""
        this.tribeRanks = ""
        this.nameColor = ""
        this.tradeName = ""
        this.tempMouseColor = ""
        this.mouseName = ""
        this.botVillage = ""
        this.captcha = ""
        this.currentCaptcha = ""

        # Integer
        this.lastPacketID = random.randint(0, 99)
        this.authKey = random.randint(0, 2147483647)
        this.langueByte = 0
        this.playerScore = 0
        this.playerCode = 0
        this.privLevel = 0
        this.playerID = 0
        this.TitleNumber = 0
        this.TitleStars = 0
        this.posX = 0
        this.posY = 0
        this.velX = 0
        this.velY = 0
        this.firstCount = 0
        this.cheeseCount = 0
        this.shamanCheeses = 0
        this.shopCheeses = 100
        this.shopFraises = 0
        this.shamanSaves = 0
        this.hardModeSaves = 0
        this.divineModeSaves = 0
        this.bootcampCount = 0
        this.shamanType = 0
        this.regDate = 0
        this.banHours = 0
        this.shamanLevel = 1
        this.shamanExp = 0
        this.shamanExpNext = 32
        this.ambulanceCount = 0
        this.bubblesCount = 0
        this.lastOn = 0
        this.silenceType = 0
        this.gender = 0
        this.lastDivorceTimer = 0
        this.tribeCode = 0
        this.tribeRank = 0
        this.tribeJoined = 0
        this.tribeChat = 0
        this.tribeHouse = 0
        this.tribulleID = 0
        this.tribePoints = 0
        this.defilantePoints = 0
        this.iceCount = 2
        this.lastGameMode = 0
        this.currentPlace = 0
        this.equipedShamanBadge = 0
        this.pet = 0
        this.petEnd = 0
        this.numGiveCheese = 0
        this.racingRounds = 0
        this.bootcampRounds = 0
        this.survivorDeath = 0
        this.playerStartTimeMillis = 0

        # Bool
        this.isClosed = False
        this.validatingVersion = False
        this.isGuest = False
        this.isReceivedDummy = False
        this.isDead = False
        this.hasCheese = False
        this.hasEnter = False
        this.isMovingRight = False
        this.isMovingLeft = False
        this.isJumping = False
        this.isShaman = False
        this.isSuspect = False
        this.isAfk = False
        this.isVoted = False
        this.qualifiedVoted = False
        this.isMute = False
        this.RTotem = False
        this.UTotem = False
        this.LoadCountTotem = False
        this.modoPwet = False
        this.canResSkill = False
        this.canShamanRespawn = False
        this.isOpportunist = False
        this.desintegration = False
        this.sendMusic = True
        this.isCafe = False
        this.canSkipMusic = False
        this.isHidden = False
        this.isTeleport = False
        this.isFly = False
        this.canSpawnCN = True
        this.isSpeed = False
        this.isNewPlayer = False
        this.isVampire = False
        this.isLuaAdmin = False
        this.isTrade = False
        this.tradeConfirm = False
        this.canUseConsumable = True
        this.canRespawn = False
        this.isSkill = False
        this.showButtons = True

        # Others
        this.Cursor = Cursor
        this.TFMUtils = TFMUtils
        this.apiToken = TFMUtils.getRandomChars(50)

        # Nonetype
        this.room = None
        this.resSkillsTimer = None
        this.consumablesTimer = None
        this.skipMusicTimer = None

        # List
        this.STotem = [0, ""]
        this.Totem = [0, ""]
        this.survivorStats = [0] * 4
        this.racingStats = [0] * 4
        this.marriageInvite = []
        this.tribeData = ["", "", 0, None]
        this.tribeInvite = []
        this.mulodromePos = []
        this.canLogin = [False, False]        
        this.cheeseTitleList = []
        this.firstTitleList = []
        this.shamanTitleList = []
        this.shopTitleList = []
        this.bootcampTitleList = []
        this.hardModeTitleList = []
        this.divineModeTitleList = []
        this.specialTitleList = []
        this.titleList = []
        this.clothes = []
        this.shopBadges = []
        this.friendsList = []
        this.ignoredsList = []
        this.ignoredMarriageInvites = []
        this.ignoredTribeInvites = []
        this.chats = []
        this.voteBan = []
        this.shamanBadges = []
        this.equipedConsumables = []
        this.custom = []

        # Dict
        this.playerSkills = {}
        this.playerConsumables = {}
        this.tradeConsumables = {}
        this.itensBots = {"Papaille": [(4, 800, 50, 4, 2253, 50), (4, 800, 50, 4, 2254, 50), (4, 800, 50, 4, 2257, 50), (4, 800, 50, 4, 2260, 50), (4, 800, 50, 4, 2261, 50)], "Buffy": [(1, 147, 1, 4, 2254, 200), (2, 17, 1, 4, 2254, 150), (2, 18, 1, 4, 2254, 150), (2, 19, 1, 4, 2254, 150), (3, 398, 1, 4, 2254, 150), (3, 392, 1, 4, 2254, 50)], "Indiana Mouse": [(3, 255, 1, 4, 2257, 50), (3, 394, 1, 4, 2257, 50), (3, 395, 1, 4, 2257, 50), (3, 320, 1, 4, 2257, 50), (3, 393, 1, 4, 2257, 50), (3, 402, 1, 4, 2257, 50), (3, 397, 1, 4, 2257, 50), (3, 341, 1, 4, 2257, 50), (3, 335, 1, 4, 2257, 25), (3, 403, 1, 4, 2257, 50), (1, 6, 1, 4, 2257, 50), (1, 17, 1, 4, 2257, 50)], "Elise": [(4, 31, 2, 4, 2261, 5), (4, 2256, 2, 4, 2261, 5), (4, 2232, 2, 4, 2253, 1), (4, 21, 5, 4, 2253, 1), (4, 33, 2, 4, 2260, 1), (4, 33, 2, 4, 2254, 1)], "Oracle": [(1, 145, 1, 4, 2253, 200), (2, 16, 1, 4, 2253, 150), (2, 21, 1, 4, 2253, 150), (2, 24, 1, 4, 2253, 150), (2, 20, 1, 4, 2253, 150), (3, 390, 1, 4, 2253, 50), (3, 391, 1, 4, 2253, 200), (3, 399, 1, 4, 2253, 150)], "Prof": [(4, 800, 20, 4, 2257, 10), (4, 19, 2, 4, 2257, 5), (4, 2258, 2, 4, 2257, 4), (4, 2262, 5, 4, 2257, 2), (4, 2259, 10, 4, 2257, 1), (4, 20, 1, 4, 2257, 2)], "Cassidy": [(1, 154, 1, 4, 2261, 200), (2, 23, 1, 4, 2261, 150), (3, 400, 1, 4, 2261, 100)], "Von Drekkemouse": [(2, 22, 1, 4, 2260, 150), (1, 153, 1, 4, 2260, 200), (3, 401, 1, 4, 2260, 100)], "Tod": [(4, 2259, 10, 4, 2257, 1), (4, 2258, 10, 4, 2254, 230), (3, 401, 1, 4, 2260, 100)]}
    
    def connectionMade(this):
        this.ipAddress = this.transport.getPeer().host
        this.server = this.factory

        this.parsePackets = ParsePackets(this, this.server)
        this.parseCommands = ParseCommands(this, this.server)
        this.shopModule = ShopModule(this, this.server)
        this.ModoPwet = ModoPwet(this, this.server)
        this.skillModule = SkillModule(this, this.server)
        this.tribulle = Tribulle(this, this.server)
        
        if this.server.getIPPermaBan(this.ipAddress) or this.ipAddress in this.server.tempIPBanList:
            this.transport.loseConnection()
            return

        if this.server.connectedCounts.has_key(this.ipAddress):
            this.server.connectedCounts[this.ipAddress] += 1
        else:
            this.server.connectedCounts[this.ipAddress] = 1

        if this.server.connectedCounts[this.ipAddress] >= 5:
            this.server.tempIPBanList.append(this.ipAddress)
            this.server.sendOutput("Attack DDOS blocked in IP: "+str(this.ipAddress))
            this.server.sendStaffMessage(7, "<R>Attack DDOS</R>: <J>["+str(this.ipAddress)+"]</J>")
            this.server.disconnectIPAddress(this.ipAddress)
            del this.server.connectedCounts[this.ipAddress]
            this.transport.loseConnection()

    def connectionLost(this, remove=True):
        this.isClosed = True
        for timer in [this.resSkillsTimer, this.consumablesTimer, this.skipMusicTimer]:
            if timer != None:
                timer.cancel()

        if this.server.connectedCounts.has_key(this.ipAddress):
            count = this.server.connectedCounts[this.ipAddress] - 1
            if count <= 0:
                del this.server.connectedCounts[this.ipAddress]
            else:
                this.server.connectedCounts[this.ipAddress] = count

        if not this.Username == "":
            if not this.isGuest:
                this.updateDatabase()
                
            if this.isTrade:
                this.cancelTrade(this.tradeName)

            if this.server.players.has_key(this.Username) and remove:
                del this.server.players[this.Username]

            if this.ModoPwet.checkReport(this.server.reports["names"], this.Username):
                if not this.server.reports[this.Username]["status"] == "banned":
                    this.server.reports[this.Username]["status"] = "disconnected"
                    this.ModoPwet.updateModoPwet()

            if this.server.chatMessages.has_key(this.Username):
                this.server.chatMessages[this.Username] = {}
                del this.server.chatMessages[this.Username]

            for client in this.server.players.values():
                if this.Username and client.Username in this.friendsList and client.friendsList:
                    client.tribulle.sendFriendDisconnected(this.Username)

            if not this.tribeName == "":
                this.tribulle.sendTribeMemberDisconnected()

            if this.privLevel >= 4:
                this.sendStaffLogin(True)
                
        if this.room != None:
            this.room.removeClient(this)

    def sendPacket(this, identifiers, packet=""):
        if this.isClosed:
            return

        p = ByteArray().writeBytes("".join(map(chr, identifiers)) + packet) if type(packet) != list else ByteArray().writeBytes(chr(1) + chr(1)).writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + packet)))
        if not this.isClosed:
            this.transport.write((ByteArray().writeByte(1).writeUnsignedByte(p.getLength()) if p.getLength() <= 0xFF else ByteArray().writeByte(2).writeUnsignedShort(p.getLength()) if p.getLength() <= 0xFFFF else ByteArray().writeByte(3).writeUnsignedByte((p.getLength() >> 16) & 0xFF).writeUnsignedByte((p.getLength() >> 8) & 0xFF).writeUnsignedByte(p.getLength() & 0xFF) if p.getLength() <= 0xFFFFFF else 0).writeBytes(p.toByteArray()).toByteArray())

    def parseString(this, packet):
        if this.isClosed:
            return

        if packet in ["", " ", "\x00", "\x01"]:
            this.server.tempIPBanList.append(this.ipAddress)
            this.server.sendOutput("Attack DDOS blocked in IP: "+str(this.ipAddress))
            this.server.sendStaffMessage(7, "<R>Attack DDOS</R>: <J>["+str(this.ipAddress)+"]</J>")
            this.server.disconnectIPAddress(this.ipAddress)
            this.transport.loseConnection()
            this.block()
        
        p = ByteArray(packet)
        if not this.validatingVersion:
            C, CC = p.readShort(), p.readByte()
            if C == 0x1c and CC == 0x1:
                version = p.readShort()
                ckey = p.readUTF()

                if not ckey == this.server.CKEY and version != this.server.Version:
                    this.server.sendOutput("WARNING: Invalid CKEY ("+ckey+") and version ("+str(version)+")")
                    this.transport.loseConnection()

                else:
                    this.validatingVersion = True
                    this.sendCorrectVersion()
        else:
            try:
                checkPacketID = (this.lastPacketID % 99)
                checkPacketID += 0 if checkPacketID == 0 else 1
                packetID = p.readByte()
                this.lastPacketID = packetID

                C, CC = p.readByte(), p.readByte()
                this.parsePackets.parsePacket(packetID, C, CC, packet)
                        
            except Exception as ERROR:
                c = open("./include/errors.log", "a")
                c.write("\n" + "=" * 60 + "\n- Time: %s\n- Player: %s\n- Error: \n" %(time.strftime("%d/%m/%Y - %H:%M:%S"), this.Username))
                traceback.print_exc(file=c)
                c.close()

    def loginPlayer(this, playerName, password, startRoom):
        playerName = "Souris" if playerName == "" else playerName
        if password == "":
            playerName = this.server.checkAlreadyExistingGuest("*" + (playerName[0].isdigit() or len(playerName) > 12 or len(playerName) < 3 or "Souris" if "+" in playerName else playerName))

        if not "#" in playerName:
            playerName += "#0000"

        if not this.canLogin[0] and not this.canLogin[1]:
            this.transport.loseConnection()
            return

        if not this.isGuest and playerName in this.server.userPermaBanCache:
            this.sendPacket(Identifiers.old.send.Player_Ban_Login, [])
            this.transport.loseConnection()
            return

        if not this.isGuest and playerName in this.server.userTempBanCache:
            banInfo = this.server.getTempBanInfo(playerName)
            timeCalc = TFMUtils.getHoursDiff(int(banInfo[0]))
            if timeCalc <= 0:
                this.server.removeTempBan(playerName)
            else:
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc * 3600000, str(banInfo[1])])
                this.transport.loseConnection()
                return

        if this.server.checkConnectedAccount(playerName):
            this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(1).writeUTF(playerName).writeUTF("").toByteArray())
        else:
            vipTime, letters, gifts, messages = 0, "", "", ""
            if not this.isGuest:
                this.Cursor.execute("select * from Users where Username = %s and Password = %s", [playerName, password])
                rs = this.Cursor.fetchone()
                if rs:
                    this.playerID = rs[2]
                    this.privLevel = rs[3]
                    this.titleNumber = rs[4]
                    this.firstCount = rs[5]
                    this.cheeseCount = rs[6]
                    this.shamanCheeses = rs[7]
                    this.shopCheeses = rs[8]
                    this.shopFraises = rs[9]
                    this.shamanSaves = rs[10]
                    this.hardModeSaves = rs[11]
                    this.divineModeSaves = rs[12]
                    this.bootcampCount = rs[13]
                    this.shamanType = rs[14]
                    this.shopItems = rs[15]
                    this.shamanItems = rs[16]
                    this.clothes = rs[17].split("|")
                    this.playerLook = rs[18]
                    this.shamanLook = rs[19]
                    this.mouseColor = rs[20]
                    this.shamanColor = rs[21]
                    this.regDate = rs[22]
                    this.shopBadges = rs[23].split(",")
                    this.cheeseTitleList = rs[24].split(",")
                    this.firstTitleList = rs[25].split(",")
                    this.shamanTitleList = rs[26].split(",")
                    this.shopTitleList = rs[27].split(",")
                    this.bootcampTitleList = rs[28].split(",")
                    this.hardModeTitleList = rs[29].split(",")
                    this.divineModeTitleList = rs[30].split(",")
                    this.specialTitleList = rs[31].split(",")
                    this.banHours = rs[32]
                    level = rs[33].split("/")
                    this.shamanLevel = int(level[0])
                    this.shamanExp = int(level[1])
                    this.shamanExpNext = int(level[2])
                    for skill in rs[34].split(";"):
                        values = skill.split(":")
                        if len(values) >= 2:
                            this.playerSkills[int(values[0])] = int(values[1])
                    this.lastOn = rs[35]
                    this.friendsList = rs[36].split(",")
                    this.ignoredsList = rs[37].split(",")
                    this.gender = rs[38]
                    this.lastDivorceTimer = rs[39]
                    this.marriage = rs[40]
                    totem = this.server.getTotemData(playerName)
                    if len(totem) == 2: this.STotem = [int(totem[0]), totem[1]]
                    gifts = rs[42]
                    message = rs[43]
                    this.survivorStats = map(int, rs[44].split(","))
                    this.racingStats = map(int, rs[45].split(","))
                    vipTime = rs[46]
                    for consumable in rs[47].split(";"):
                        values = consumable.split(":")
                        if len(values) >= 2:
                            this.playerConsumables[int(values[0])] = int(values[1])                            
                    this.equipedConsumables = map(int, filter(None, rs[48].split(",")))
                    this.pet = rs[49]
                    this.petEnd = 0 if this.pet == 0 else Utils.getTime() + rs[50]
                    this.shamanBadges = rs[51].split(",")
                    this.equipedShamanBadge = rs[52]
                    letters = rs[53]
                    this.custom = rs[55].split(",")
                    this.tribeCode = rs[56]
                    this.tribeRank = rs[57]
                    this.tribeJoined = rs[58]
                else:
                    reactor.callLater(5, lambda: this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray()))
                    return

            if this.privLevel == -1:
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Account Locked."])
                this.transport.loseConnection()
                return

            this.server.lastPlayerCode += 1
            this.Username = playerName
            this.playerCode = this.server.lastPlayerCode
            this.Cursor.execute("insert into LoginLog select %s, %s where not exists (select 1 from LoginLog where Username = %s and IP = %s)", [playerName, this.ipAddress, playerName, this.ipAddress])

            this.clothes = filter(None, this.clothes)
            this.shopBadges = filter(None, this.shopBadges)
            this.custom = filter(None, this.custom)
            this.shamanBadges = filter(None, this.shamanBadges)
            this.shopTitleList = filter(None, this.shopTitleList)
            this.firstTitleList = filter(None, this.firstTitleList)
            this.cheeseTitleList = filter(None, this.cheeseTitleList)
            this.shamanTitleList = filter(None, this.shamanTitleList)
            this.specialTitleList = filter(None, this.specialTitleList)
            this.bootcampTitleList = filter(None, this.bootcampTitleList)
            this.hardModeTitleList = filter(None, this.hardModeTitleList)
            this.divineModeTitleList = filter(None, this.divineModeTitleList)

            for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                this.checkAndRebuildTitleList(name)

            this.sendCompleteTitleList()
            this.shopModule.checkAndRebuildBadges()
            
            for title in this.titleList:
                if str(title).split(".")[0] == str(this.TitleNumber):
                    this.TitleStars = int(str(title).split(".")[1])
                    break

            this.isMute = playerName in this.server.userMuteCache
            this.server.players[this.Username] = this
            this.tribulle.platformAuthentication(True)
            this.skillModule.sendShamanSkills()
            this.skillModule.sendExp(this.shamanLevel, this.shamanExp, this.shamanExpNext)
            this.sendLogin()
            this.sendPlayerIdentification()
            this.shopModule.sendShamanItems()
            if this.shamanSaves >= 500:
                this.sendShamanType(this.shamanType, (this.shamanSaves >= 2500 and this.hardModeSaves >= 1000))

            if this.tribeCode != 0:
                tribeInfo = this.tribulle.getTribeInfo(this.tribeCode)
                this.tribeName = tribeInfo[0]
                this.tribeMessage = tribeInfo[1]
                this.tribeHouse = tribeInfo[2]
                this.tribeRanks = tribeInfo[3]
                this.tribeChat = tribeInfo[4]

            this.server.checkPromotionsEnd()
            this.sendTimeStamp()
            this.sendPromotions()
            this.sendPacket(Identifiers.send.Email_Confirmed, chr(1))
            
            if this.privLevel == 2:
                this.checkVip(vipTime)

            # this.tribulle.sendPlayerInfo()
            this.tribulle.sendFriendsList(None)
            # this.tribulle.sendIgnoredsList()
            # this.tribulle.sendTribe(False)

            for client in this.server.players.values():
                if this.Username in client.friendsList and client.Username in this.friendsList:
                    client.tribulle.sendFriendConnected(this.Username)

            if not this.tribeName == "":
                this.tribulle.sendTribeMemberConnected()

            if this.privLevel >= 4:
                this.sendStaffLogin(False)
                
            this.sendInventoryConsumables()
            this.checkLetters(letters)
            this.shopModule.checkGiftsAndMessages(gifts, messages)

            if not startRoom == "" and not startRoom == "1":
                this.enterRoom(this.server.checkRoom(startRoom, this.Langue))
            else:
                this.enterRoom(this.server.recommendRoom(this.Langue))
                
            this.resSkillsTimer = reactor.callLater(600, setattr, this, "canResSkill", True)

    def createAccount(this, playerName, password):
        this.server.lastPlayerID += 1
        this.Cursor.execute("insert into Users values (%s, %s, %s, 1, 0, 0, 0, 0, %s, %s, 0, 0, 0, 0, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', %s, '', '', '', '', '', '', '', '', '', 0, '200/0/100000', '', 0, '', '', 0, 0, '', '', '', '', '0,0,0,0', '0,0,0,0', 0, '0:10', '0', 0, 0, '', 0, '', 0, '', 0, 0, 0)", [playerName, password, this.server.lastPlayerID, this.server.initialCheeses, this.server.initialFraises, TFMUtils.getTime()])
        this.sendNewConsumable(23, 10)
        this.sendAccountTime()

        this.server.updateConfig()

    def checkAndRebuildTitleList(this, type):
        titlesLists = [this.cheeseTitleList, this.firstTitleList, this.shamanTitleList, this.shopTitleList, this.bootcampTitleList, this.hardModeTitleList, this.divineModeTitleList]
        titles = [this.server.cheeseTitleList, this.server.firstTitleList, this.server.shamanTitleList, this.server.shopTitleList, this.server.bootcampTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0
        count = this.cheeseCount if type == "cheese" else this.firstCount if type == "first" else this.shamanSaves if type == "shaman" else this.shopModule.getShopLength() if type == "shop" else this.bootcampCount if type == "bootcamp" else this.hardModeSaves if type == "hardmode" else this.divineModeSaves if type == "divinemode" else 0
        tempCount = count
        rebuild = False
        while tempCount > 0:
            if titles[typeID].has_key(tempCount):
                if not titles[typeID][tempCount] in titlesLists[typeID]:
                    rebuild = True
                    break

            tempCount -= 1

        if rebuild:
            titlesLists[typeID] = []
            x = 0
            while x <= count:
                if titles[typeID].has_key(x):
                    title = titles[typeID][x]                    
                    i = 0
                    while i < len(titlesLists[typeID]):
                        if str(titlesLists[typeID][i]).startswith(str(title).split(".")[0]):
                            del titlesLists[typeID][i]
                        i += 1                        
                    titlesLists[typeID].append(title)
                x += 1
                
            this.cheeseTitleList = titlesLists[0]
            this.firstTitleList = titlesLists[1]
            this.shamanTitleList = titlesLists[2]
            this.shopTitleList = titlesLists[3]
            this.bootcampTitleList = titlesLists[4]
            this.hardModeTitleList = titlesLists[5]
            this.divineModeTitleList = titlesLists[6]

    def sendMBox(this, text, x, y, width, height, alpha, bgcolor, bordercolor, boxid, fixed=True):
        text = str(text)
        x, y, width, height = int(x), int(y), int(width), int(height)
        alpha = str(alpha).split("%")[0]
        alpha = int(alpha)
        if "#" in str(bgcolor):
            bgcolor = str(bgcolor[1:])
        else:
            pass
        if "#" in str(bordercolor):
            bordercolor = str(bordercolor[1:])
        else:
            pass
        bgcolor, bordercolor = int(bgcolor, 16), int(bordercolor, 16)
        data = struct.pack("!ih", int(boxid), len(text)) + str(text) + struct.pack("!hhhhiibb", int(x), int(y), int(width), int(height), int(bgcolor), int(bordercolor), int(alpha), fixed)
        this.sendPacket([29, 20], data)
        if boxid == 50:
            reactor.callLater(12, this.sendPacket, [29, 22], struct.pack("!i", int(50)))

    def editMBox(this, boxid, newtext):
        info = struct.pack("!ih", int(boxid), len(newtext)) + str(newtext)
        this.room.sendAllBin([29, 21], info)

    def removeMBox(this, boxid):
        data = struct.pack("!i", int(boxid))
        this.room.sendAllBin([29, 22], data)

    def updateDatabase(this):
        this.updateTribePoints()
        this.Cursor.execute("update Users set PrivLevel = %s, TitleNumber = %s, FirstCount = %s, CheeseCount = %s, ShamanCheeses = %s, ShopCheeses = %s, ShopFraises = %s, ShamanSaves = %s, HardModeSaves = %s, DivineModeSaves = %s, BootcampCount = %s, ShamanType = %s, ShopItems = %s, ShamanItems = %s, Clothes = %s, Look = %s, ShamanLook = %s, MouseColor = %s, ShamanColor = %s, RegDate = %s, Badges = %s, CheeseTitleList = %s, FirstTitleList = %s, BootcampTitleList = %s, ShamanTitleList = %s, HardModeTitleList = %s, DivineModeTitleList = %s, ShopTitleList = %s, SpecialTitleList = %s, BanHours = %s, ShamanLevel = %s, Skills = %s, FriendsList = %s, IgnoredsList = %s, Gender = %s, LastDivorceTimer = %s, Marriage = %s, TribeInfo = %s, SurvivorStats = %s, RacingStats = %s, Consumables = %s, EquipedConsumables = %s, LastOn = %s, Pet = %s, PetEnd = %s, ShamanBadges = %s, EquipedShamanBadge = %s, customItems = %s, TribeCode = %s, TribeRank = %s, TribeJoined = %s where Username = %s", [this.privLevel, this.TitleNumber, this.firstCount, this.cheeseCount, this.shamanCheeses, this.shopCheeses, this.shopFraises, this.shamanSaves, this.hardModeSaves, this.divineModeSaves, this.bootcampCount, this.shamanType, this.shopItems, this.shamanItems, "|".join(map(str, this.clothes)), this.playerLook, this.shamanLook, this.MouseColor, this.ShamanColor, this.regDate, ",".join(map(str, this.shopBadges)), ",".join(map(str, this.cheeseTitleList)), ",".join(map(str, this.firstTitleList)), ",".join(map(str, this.bootcampTitleList)), ",".join(map(str, this.shamanTitleList)), ",".join(map(str, this.hardModeTitleList)), ",".join(map(str, this.divineModeTitleList)), ",".join(map(str, this.shopTitleList)), ",".join(map(str, this.specialTitleList)), this.banHours, "/".join(map(str, [this.shamanLevel, this.shamanExp, this.shamanExpNext])), ";".join(map(lambda skill: str(skill[0]) + ":" + str(skill[1]), this.playerSkills.items())), ",".join(map(str, this.friendsList)), ",".join(map(str, this.ignoredsList)), this.gender, this.lastDivorceTimer, this.marriage, "" if this.tribeName == "" else "#".join(map(str, [this.tribeCode, this.tribeRank, this.tribeJoined])), ",".join(map(str, this.survivorStats)), ",".join(map(str, this.racingStats)), ";".join(map(lambda consumable: str(consumable[0]) + ":" + str(consumable[1]), this.playerConsumables.items())), ",".join(map(str, this.equipedConsumables)), this.tribulle.getTime(), this.pet, abs(TFMUtils.getSecondsDiff(this.petEnd)), ",".join(map(str, this.shamanBadges)), this.equipedShamanBadge, ",".join(map(str, this.custom)), this.tribeCode, this.tribeRank, this.tribeJoined, this.Username])

    def reloadRanking(this):
        Userlist = []
        lists = "<V><p align='center'><b>Ranking Transformice</b></p>\n"
        this.Cursor.execute("select Username, CheeseCount, FirstCount, BootcampCount, ShamanSaves from Users where PrivLevel < 6 ORDER By FirstCount DESC LIMIT 20")
        rs = this.Cursor.fetchall()
        pos = 1
        this.updateDatabase()
        for rrf in rs:
            playerName = str(rrf[0])
            CheeseCount = rrf[1]
            FirstCount = rrf[2]
            BootcampCount = rrf[3]
            ShamanSaves = rrf[4]
            player = this.server.players.get(playerName)
            if pos == 1:
                lists += "<V>"+str(pos)+"<N> - <N><V>"+str(playerName)+"<N> - <N>" + ("[<VP>Online<N> - <VP>"+str(player.Langue) + "<N>]\n" if player != None else "<N>[<R>Offline<N>]\n")
            elif pos == 2:
                lists += "<V>"+str(pos)+"<N> - <N><V>"+str(playerName)+"<N> - <N>" + ("[<VP>Online<N> - <VP>"+str(player.Langue) + "<N>]\n" if player != None else "<N>[<R>Offline<N>]\n")
            elif pos == 3:
                lists += "<V>"+str(pos)+"<N> - <N><V>"+str(playerName)+"<N> - <N>" + ("[<VP>Online<N> - <VP>"+str(player.Langue) + "<N>]\n" if player != None else "<N>[<R>Offline<N>]\n")
            else:
                lists += "<V>"+str(pos)+"<N> - <N><V>"+str(playerName)+"<N> - <N>" + ("[<VP>Online<N> - <VP>"+str(player.Langue) + "<N>]\n" if player != None else "<N>[<R>Offline<N>]")
                lists += "<br />"
            lists += "<BL>• Frists :</font> <V>"+str(FirstCount)+""
            lists += "<br />"
            lists += "<BL>• Cheeses :</font> <V>"+str(CheeseCount)+""
            lists += "<br />"
            lists += "<BL>• Saves :</font> <V>"+str(ShamanSaves)+""
            lists += "<br />"
            lists += "<BL>• Bootcamps :</font> <V>"+str(BootcampCount)+"\n"
            lists += "<br />"
            pos += 1

        this.sendLogMessage(lists + "</p>")

    def enterRoom(this, roomName):
        if this.isTrade:
            this.cancelTrade(this.tradeName)

        if this.server.DEBUG:
            this.sendPacket([29, 1], "")

        roomName = roomName.replace("<", "&lt;")

        if roomName.startswith(chr(3) + "[Editeur] ") or roomName.startswith(chr(3)+ "[Totem] ") or roomName.startswith(chr(3) + "[Tutorial] "):
            if not this.Username == roomName.split(" ")[1]:
                roomName = this.Langue + "-" + this.Username

        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == '-' and this.privLevel >= 7):
            roomName = this.Langue + "-" + roomName        
            
        if this.room != None:
            this.room.removeClient(this)

        this.roomName = roomName
        this.sendGameType(11 if "music" in roomName else 1 if "madchees" in roomName else 4, 4 if "madchees" in roomName else 0)
        this.sendEnterRoom(roomName)
        this.server.addClientToRoom(this, roomName)
        this.sendPacket(Identifiers.old.send.Anchors, this.room.anchors)
        this.LoadCountTotem = False

        for client in this.server.players.values():
            if this.Username and client.Username in this.friendsList and client.friendsList:
                client.tribulle.sendFriendChangedRoom(this.Username, this.langueByte)

        if not this.tribeName == "":
            this.tribulle.sendTribeMemberChangeRoom()

        if this.room.isMusic and this.room.isPlayingMusic:
            this.sendMusicVideo(False)
            
        if roomName.startswith("music") or roomName.startswith("*music"):
            this.canSkipMusic = False
            if this.skipMusicTimer != None:
                this.skipMusicTimer.cancel()

            this.skipMusicTimer = reactor.callLater(900, setattr, this, "canSkipMusic", True)
        
        if this.room.isFuncorp:
            this.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
           
    def resetPlay(this, hasCheese=True):
        this.isDead = False
        this.isAfk = True
        this.isShaman = False
        this.isSuspect = False
        this.hasEnter = False
        this.UTotem = False
        this.canShamanRespawn = False
        this.ambulanceCount = 0
        this.bubblesCount = 0
        this.isOpportunist = False
        this.desintegration = False
        this.canRespawn = False
        this.defilantePoints = 0
        this.iceCount = 2
        this.isNewPlayer = False
        this.currentPlace = 0
        this.isVampire = False
        this.numGiveCheese = 0
        this.bootcampRounds = 0
        if hasCheese:
            this.hasCheese = False

    def sendAccountTime(this):

        eventTime = 1

        date = datetime.now() + timedelta(hours=int(eventTime))

        timetuple = date.timetuple()

        eventTime_ = int(str(thetime.mktime(timetuple)).split(".")[0])

        this.Cursor.execute('select IP from Account where IP = %s', [this.ipAddress])

        rrf = this.Cursor.fetchone()

        if rrf is None:

           this.Cursor.execute('insert into Account values (%s, %s)', [this.ipAddress, eventTime_])

        else:

           this.Cursor.execute('update Account set Time = %s where IP = %s', [eventTime_, this.ipAddress])

        


    def checkTimeAccount(this):

        this.Cursor.execute('SELECT Time FROM Account WHERE IP = %s', [this.ipAddress])

        rrf = this.Cursor.fetchone()

        if rrf is None:

            return True

        else:

            if (int(str(thetime.time()).split(".")[0]) >= int(rrf[0])):

                return True

            else:

                return False 

    def startPlay(this):
        this.playerStartTimeMillis = this.room.gameStartTimeMillis
        this.isNewPlayer = this.room.isCurrentlyPlay
        this.sendMap(False, True) if this.room.mapCode != -1 else this.sendMap() if this.room.isEditeur and this.room.EMapCode != 0 else this.sendMap(True)

        shamanCode2 = 0
        if this.room.isDoubleMap:
            shamans = this.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = this.room.getShamanCode()

        if this.playerCode == shamanCode or this.playerCode == shamanCode2:
            this.isShaman = True

        if this.isShaman and not this.room.noShamanSkills:
            this.skillModule.getkills()

        if this.room.currentShamanName != "" and not this.room.noShamanSkills:
            this.skillModule.getPlayerSkills(this.room.currentShamanSkills)

        if this.room.currentSecondShamanName != "" and not this.room.noShamanSkills:
            this.skillModule.getPlayerSkills(this.room.currentSecondShamanSkills)

        this.sendPlayerList()
        if this.room.catchTheCheeseMap and not this.room.noShamanSkills:
            this.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            this.sendPacket(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(shamanCode).writeBool(True).toByteArray())
            if not this.room.currentMap in [108, 109]:
                this.sendShamanCode(shamanCode, shamanCode2)
        else:
            this.sendShamanCode(shamanCode, shamanCode2)

        this.sendSync(this.room.getSyncCode())
        this.sendRoundTime(this.room.roundTime + (this.room.gameStartTime - TFMUtils.getTime()) + this.room.addTime)
        this.sendMapStartTimerEnd() if this.room.isCurrentlyPlay or this.room.isTutorial or this.room.isTotemEditeur or this.room.isBootcamp or this.room.isDefilante or this.room.getPlayerCountUnique() <= 2 else this.sendMapStartTimer()
        if this.room.isTotemEditeur:
            this.initTotemEditeur()

        if this.room.currentMap in range(200, 211) and not this.isShaman:
            this.sendPacket(Identifiers.send.Can_Transformation, chr(1))

        if this.room.isSurvivor and this.isShaman:
            this.sendPacket(Identifiers.send.Can_Meep, chr(1))

        if this.room.isVillage:
            reactor.callLater(0.2, this.sendBotsVillage)

    def sendBotsVillage(this):
        this.sendPacket([8, 30], "\xff\xff\xff\xff\x00\x06Oracle\x01+\x01\x00*61;0,0,0,0,0,19_3d100f+1fa896+ffe15b,0,0,0\x08\x8b\x01}\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfe\x00\x08Papaille\x01*\x01\x00\x134;2,0,2,2,0,0,0,0,1\tZ\x00\xd1\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfd\x00\x05Elise\x01]\x01\x00\x143;10,0,1,0,1,0,0,1,0\t\x19\x00\xd1\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfc\x00\x05Buffy\x01[\x01\x00\x06$Buffy\x07t\x01\xf3\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfb\x00\rIndiana Mouse\x01(\x00\x00\x1445;0,0,0,0,0,0,0,0,0\x00\xae\x02\xca\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfa\x00\x04Prof\x01G\x00\x00\n$Proviseur\x01!\x02\xcb\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xf9\x00\x07Cassidy\x01\x18\x00\x00\x07$Barman\n\xd2\x02%\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xf8\x00\x0fVon Drekkemouse\x01\x1f\x00\x00\n$Halloween\x06\x88\x01z\x00\x01\x0b\x00\x00")

    def getPlayerData(this):
        return ByteArray().writeUTF(this.Username if this.mouseName == "" else this.mouseName).writeInt(this.playerCode).writeBool(this.isShaman).writeBool(this.isDead).writeShort(this.playerScore).writeBool(this.hasCheese).writeShort(this.TitleNumber).writeByte(this.TitleStars).writeByte(this.gender).writeShort(0).writeUTF("1;0,0,0,0,0,0,0,0,0,0" if this.room.isBootcamp else this.playerLook).writeBool(False).writeInt(int(this.tempMouseColor if not this.tempMouseColor == "" else this.MouseColor, 16)).writeInt(int(this.ShamanColor, 16)).writeBytes('\x00\x00\x00\x00\xff\xff\xff\xff').toByteArray()

    def sendShamanCode(this, shamanCode, shamanCode2):
        this.sendShaman(shamanCode, shamanCode2, this.server.getShamanType(shamanCode), this.server.getShamanType(shamanCode2), this.server.getShamanLevel(shamanCode), this.server.getShamanLevel(shamanCode2), this.server.getShamanBadge(shamanCode), this.server.getShamanBadge(shamanCode2))

    def sendDoubleShamanCode(this, shamanCode, shamanCodeTwo):
        this.sendShaman(shamanCode, shamanCodeTwo, this.room.currentShamanType, this.room.currentSecondShamanType, this.server.getPlayerLevel(this.room.currentShamanName), this.server.getPlayerLevel(this.room.currentSecondShamanName), this.skillModule.getShamanBadge(this.room.currentShamanSkills, this.room.currentShamanCode), this.skillModule.getShamanBadge(this.room.currentSecondShamanSkills, this.room.currentSecondShamanCode))

    def sendCorrectVersion(this):
        this.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(this.server.getConnectedPlayerCount()).writeByte(this.lastPacketID).writeUTF("br").writeUTF("br").writeInt(this.authKey).toByteArray())
        this.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeByte(1).writeByte(7).writeByte(1).writeByte(0).toByteArray())
        this.sendPacket(Identifiers.send.Interface_Login, ByteArray().writeUTF("").toByteArray())
        
    def sendLogin(this):
        this.sendPacket(Identifiers.old.send.Login, [this.Username, this.playerCode, this.privLevel, 30, 1 if this.isGuest else 0, 0, 0, 0])
        if this.isGuest:
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeUnsignedByte(200).toByteArray())

    def sendPlayerIdentification(this):
        if this.isGuest:
            this.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(this.playerID).writeUTF(this.Username).writeInt(600000).writeByte(this.langueByte).writeInt(this.playerCode).writeByte(this.privLevel).writeBool(False).writeBool(False).toByteArray())
            this.sendPacket([100, 6], "\x00\x00")
        else:
            this.sendPacket(Identifiers.send.Player_Identification, ByteArray().writeInt(this.playerID).writeUTF(this.Username).writeInt(600000).writeByte(this.langueByte).writeInt(this.playerCode).writeByte(this.privLevel).writeBool(False).writeBool(False).toByteArray())
            this.sendPacket([100, 6], "\x00\x00")
            
    def sendTimeStamp(this):
        this.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(TFMUtils.getTime()).toByteArray())

    def enableSpawnCN(this):
        this.canSpawnCN = True

    def sendPromotions(this):
        for promotion in this.server.shopPromotions:
            this.sendPacket(Identifiers.send.Promotion, ByteArray().writeBool(True).writeBool(True).writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeBool(True).writeInt(promotion[3]).writeByte(promotion[2]).toByteArray())

        if len(this.server.shopPromotions) > 0:
            promotion = this.server.shopPromotions[0]
            item = promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)
            this.sendPacket(Identifiers.send.Promotion_Popup, ByteArray().writeByte(promotion[0]).writeByte(promotion[1]).writeByte(promotion[2]).writeShort(this.server.shopBadges.get(item, 0)).toByteArray())

    def sendGameType(this, gameType, serverType):
        this.sendPacket(Identifiers.send.Room_Type, ByteArray().writeByte(gameType).toByteArray())
        this.sendPacket(Identifiers.send.Room_Server, ByteArray().writeByte(serverType).toByteArray())

    def sendEnterRoom(this, roomName):
        this.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBool(roomName.startswith("*") or roomName.startswith(str(chr(3)))).writeUTF(roomName).toByteArray())

    def sendMap(this, newMap=False, newMapCustom=False):
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(this.room.currentMap if newMap else this.room.mapCode if newMapCustom else -1).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastRoundCode).writeShort(0).writeUTF("" if newMap else this.room.mapXML.encode("zlib") if newMapCustom else this.room.EMapXML.encode("zlib")).writeUTF("" if newMap else this.room.mapName if newMapCustom else "-").writeByte(0 if newMap else this.room.mapPerma if newMapCustom else 100).writeBool(this.room.mapInverted if newMapCustom else False).toByteArray())    

    def sendPlayerList(this):
        players, data = this.room.getPlayerList(), ""
        for player in players: data += player
        this.sendPacket(Identifiers.send.Players_List, ByteArray().writeShort(len(players)).writeBytes(data).toByteArray())
        
    def sendSync(this, playerCode):
        if this.room.mapCode != 1 or this.room.EMapCode != 0:
            this.sendPacket(Identifiers.old.send.Sync, [playerCode, ""])
        else:
            this.sendPacket(Identifiers.old.send.Sync, [playerCode])

    def sendRoundTime(this, time):
        this.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(time).toByteArray())
    
    def sendMapStartTimer(this):
        this.sendPacket(Identifiers.send.Map_Start_Timer, chr(1))

    def sendMapStartTimerEnd(this):
        if this.hasCheese:
            this.hasCheese = False
            this.room.sendAll(Identifiers.send.Remove_Cheese, ByteArray().writeInt(this.playerCode).toByteArray())

        this.sendPacket(Identifiers.send.Map_Start_Timer, chr(0))

    def sendPlayerDisconnect(this):
        this.room.sendAll(Identifiers.old.send.Player_Disconnect, [this.playerCode])

    def sendPlayerDied(this):
        this.room.sendAll(Identifiers.old.send.Player_Died, [this.playerCode, 0, this.playerScore])

        if this.room.isBootcamp:
            this.hasCheese = False

        if this.room.isRacing:
            this.racingRounds = 0

        if this.room.getAliveCount() < 1 or this.room.catchTheCheeseMap or this.isAfk:
            this.canShamanRespawn = False

        if ((this.room.checkIfTooFewRemaining() and not this.canShamanRespawn) or (this.room.checkIfShamanIsDead() and not this.canShamanRespawn) or (this.room.checkIfDoubleShamansAreDead())):
            this.room.send20SecRemainingTimer()

        if this.canShamanRespawn:
            this.isDead = False
            this.isAfk = False
            this.hasCheese = False
            this.hasEnter = False
            this.canShamanRespawn = False
            this.playerStartTimeMillis = time.time()
            this.room.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(this.getPlayerData()).writeBool(False).writeBool(True).toByteArray())
            if this.hasCheese:
                this.hasCheese = False
                this.sendGiveCheese()
            for client in this.room.clients.values():
                client.sendShamanCode(this.playerCode, 0)

    def sendShaman(this, shamanCode, shamanCode2, shamanType, shamanType2, shamanLevel, shamanLevel2, shamanBadge, shamanBadge2):
        this.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(shamanType).writeByte(shamanType2).writeShort(shamanLevel).writeShort(shamanLevel2).writeShort(shamanBadge).writeShort(shamanBadge2).toByteArray())

    def sendConjurationDestroy(this, x, y):
        this.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendGiveCheese(this, distance=-1):
        if distance != -1 and distance != 1000 and not this.room.catchTheCheeseMap and this.room.countStats:
            if distance >= 30:
                this.isSuspect = True

        this.room.canChangeMap = False
        if not this.hasCheese:
            this.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(this.playerCode).writeBool(True).toByteArray())
            this.numGiveCheese += 1
            this.hasCheese = True
            if this.room.isTutorial:
                this.sendPacket(Identifiers.send.Tutorial, chr(1))
            if this.room.currentMap in range(108, 114):
                if this.numGiveCheese >= 10:
                    this.room.killShaman()

        this.room.canChangeMap = True

    def playerWin(this, holeType, distance=-1):
        if distance != -1 and distance != 1000 and this.isSuspect and this.room.countStats:
            if distance >= 30:
                this.server.sendStaffMessage(7, "[<V>ANTI-HACK</V>][<J>%s</J>][<V>%s</V>] Instant win detected by distance." %(this.ipAddress, this.Username))
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Instant win detected by distance."])
                this.transport.loseConnection()
                return

        this.room.canChangeMap = False
        canGo = this.room.checkIfShamanCanGoIn() if this.isShaman else True
        if not canGo:
            this.sendSaveRemainingMiceMessage()

        if this.isDead or not this.hasCheese and not this.isOpportunist:
            canGo = False

        if this.room.isTutorial:
            this.sendPacket(Identifiers.send.Tutorial, chr(2))
            this.hasCheese = False
            reactor.callLater(10, lambda: this.enterRoom(this.server.recommendRoom(this.Langue)))
            this.sendRoundTime(10)
            return

        if this.room.isEditeur:
            if not this.room.EMapValidated and this.room.EMapCode != 0:
                this.room.EMapValidated = True
                this.sendPacket(Identifiers.old.send.Map_Validated, [""])

        if canGo:
            this.isDead = True
            this.hasCheese = False
            this.hasEnter = True
            this.isOpportunist = False
            this.room.numCompleted += 1
            place = this.room.numCompleted
            if this.room.isDoubleMap:
                if holeType == 1:
                    this.room.FSnumCompleted += 1
                elif holeType == 2:
                    this.room.SSnumCompleted += 1
                else:
                    this.room.FSnumCompleted += 1
                    this.room.SSnumCompleted += 1

            timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
            this.currentPlace = place
            if place == 1:
                this.playerScore += (4 if this.room.isRacing else 16) if not this.room.noAutoScore else 0
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn and not this.isGuest:
                    this.firstCount += 3
                    this.cheeseCount += 3

                    if not this.tribeName == "":
                        this.tribePoints += 1

            elif place == 2:
                this.playerScore += (3 if this.room.isRacing else 14) if not this.room.noAutoScore else 0
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn and not this.isGuest:
                    this.firstCount += 2
                    this.cheeseCount += 2
            elif place == 3:
                this.playerScore += (2 if this.room.isRacing else 12) if not this.room.noAutoScore else 0
                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn and not this.isGuest:
                    this.firstCount += 1
                    this.cheeseCount += 1
            else:
                this.playerScore += (1 if this.room.isRacing else 10) if not this.room.noAutoScore else 0

            if this.room.isMulodrome:
                if this.Username in this.room.redTeam:
                    this.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1

                elif this.Username in this.room.blueTeam:
                    this.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1

                this.room.sendMulodromeRound()

            if this.room.isDefilante:
                if not this.room.noAutoScore: this.playerScore += this.defilantePoints
                id = 2257
                if not id in this.playerConsumables:
                    this.playerConsumables[id] = 1
                else:
                    count = this.playerConsumables[id] + 1
                    this.playerConsumables[id] = count
                this.sendAnimZeldaInventory(4, id, 1)
                   
            if this.room.isRacing:
                id = 2254
                this.racingRounds += 1
                if this.racingRounds >= 5:
                    if not id in this.playerConsumables:
                        this.playerConsumables[id] = 1
                    else:
                        count = this.playerConsumables[id] + 1
                        this.playerConsumables[id] = count
                    this.sendAnimZeldaInventory(4, id, 1)
                    this.racingRounds = 0

            if this.room.isBootcamp:
                id = 2261
                this.bootcampRounds += 1
                if this.bootcampRounds == 5:
                    if not id in this.playerConsumables:
                        this.playerConsumables[id] = 1
                    else:
                        count = this.playerConsumables[id] + 1
                        this.playerConsumables[id] = count
                    this.sendAnimZeldaInventory(4, id, 1)

            if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.room.isBootcamp and not this.isGuest:
                if this.playerCode == this.room.currentShamanCode or this.playerCode == this.room.currentSecondShamanCode:
                    this.shamanCheeses += 1
                    this.sendAnimZelda(4, 2253)
                    this.sendNewConsumable(2253, 1)
                    if this.playerConsumables.has_key(2253):
                        this.playerConsumables[2253] += 1
                    else:
                        this.playerConsumables[2253] = 1

                    count = 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    this.shopCheeses += count
                    this.shopFraises += count

                    this.sendGiveCurrency(0, 1)
                    this.skillModule.earnExp(False, 20)
                    if not this.isGuest:
                        if place == 1 and this.server.firstTitleList.has_key(this.firstCount):
                            title = this.server.firstTitleList[this.firstCount]
                            this.checkAndRebuildTitleList("first")
                            this.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                            this.sendCompleteTitleList()
                            this.sendTitleList()
                        
                        if this.server.cheeseTitleList.has_key(this.cheeseCount):
                            title = this.server.cheeseTitleList[this.cheeseCount]
                            this.checkAndRebuildTitleList("cheese")
                            this.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                            this.sendCompleteTitleList()
                            this.sendTitleList()
                           
            elif this.room.getPlayerCountUnique() >= this.server.needToBootcamp and this.room.isBootcamp and not this.isGuest:
                if not this.server.isNowEvent:
                    this.bootcampCount += 1
                else:
                    this.bootcampCount += 3

                if this.server.bootcampTitleList.has_key(this.bootcampCount):
                    title = this.server.bootcampTitleList[this.bootcampCount]
                    this.checkAndRebuildTitleList("bootcamp")
                    this.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    this.sendCompleteTitleList()
                    this.sendTitleList()
                    
            this.room.giveShamanSave(this.room.currentSecondShamanName if holeType == 2 and this.room.isDoubleMap else this.room.currentShamanName, 0)
            if this.room.currentShamanType != 0:
                this.room.giveShamanSave(this.room.currentShamanName, this.room.currentShamanType)

            if this.room.currentSecondShamanType != 0:
                this.room.giveShamanSave(this.room.currentSecondShamanName, this.room.currentSecondShamanType)

            this.sendPlayerWin(place, timeTaken)

            if this.room.getPlayerCount() >= 2 and this.room.checkIfTooFewRemaining() and not this.room.isDoubleMap and this.room.currentShamanName != "" and this.isOpportunist:
                this.playerWin(0)
            else:
                this.room.checkShouldChangeMap()

        this.room.canChangeMap = True

    def sendSaveRemainingMiceMessage(this):
        this.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(this, type, count):
        this.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWin(this, place, timeTaken):
        this.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if this.room.isDefilante else 0).writeInt(this.playerCode).writeShort(this.playerScore).writeUnsignedByte(place).writeUnsignedShort(timeTaken).toByteArray())
        this.hasCheese = False

    def sendCompleteTitleList(this):
        this.titleList = []
        this.titleList.append(0.1)
        this.titleList.extend(this.cheeseTitleList)
        this.titleList.extend(this.firstTitleList)
        this.titleList.extend(this.shamanTitleList)
        this.titleList.extend(this.shopTitleList)
        this.titleList.extend(this.bootcampTitleList)
        this.titleList.extend(this.hardModeTitleList)
        this.titleList.extend(this.divineModeTitleList)
        this.titleList.extend(this.specialTitleList)

        if this.privLevel >= 2:
            this.titleList.append(1100.9)

        if this.privLevel >= 4:
            this.titleList.append(1101.9 if this.gender in [2, 0] else 1102.9)

        if this.privLevel >= 5:
            this.titleList.append(1103.9 if this.gender in [2, 0] else 1104.9)

        if this.privLevel >= 6:
            this.titleList.append(1105.9 if this.gender in [2, 0] else 1106.9)

        if this.privLevel >= 7:
            this.titleList.append(1107.9 if this.gender in [2, 0] else 1108.9)

        if this.privLevel >= 8:
            this.titleList.append(1109.9 if this.gender in [2, 0] else 1110.9)

        if this.privLevel >= 9:
            this.titleList.append(1111.9 if this.gender in [2, 0] else 1112.9)

        if this.privLevel == 10:
            this.titleList.extend([440.9, 442.9, 444.9, 445.9, 446.9, 447.9, 448.9, 449.9, 450.9, 451.9, 452.9, 453.9, 1113.9 if this.gender in [2, 0] else 1114.9])

    def sendTitleList(this):
        this.sendPacket(Identifiers.old.send.Titles_List, [this.titleList])

    def sendUnlockedTitle(this, title, stars):
        this.room.sendAll(Identifiers.old.send.Unlocked_Title, [this.playerCode, title, stars])

    def sendMessage(this, message, tab=False):
        this.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeBool(tab).writeUTF(message).writeByte(0).writeUTF("").toByteArray())

    def sendProfile(this, playerName):
        player = this.server.players.get(playerName)

        if player != None and not player.isGuest:
            p = ByteArray().writeUTF(player.Username if player.mouseName == "" else this.mouseName).writeInt(player.playerID)
            p.writeInt(str(player.regDate)[:10])
            p.writeByte(1 if player.privLevel <= 2 else 21 if player.privLevel <= 5 else 20 if player.privLevel <= 6 else 6 if player.privLevel <= 9 else 10)
            p.writeByte(player.gender)
            p.writeUTF(player.tribeName)
            p.writeUTF(player.marriage)
            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                p.writeInt(stat)

            p.writeShort(player.TitleNumber)
            titles = ByteArray()
            for title in player.titleList:
                titleInfo = str(title).split(".")
                titles.writeShort(int(titleInfo[0])).writeByte(int(titleInfo[1]))

            titlesResult = titles.toByteArray()

            p.writeShort(len(player.titleList))
            p.write(titlesResult)
            p.writeUTF(player.playerLook + ";" + player.MouseColor)
            p.writeShort(player.shamanLevel)
            p.writeShort(len(player.shopBadges) * 2)

            badges = map(int, player.shopBadges)
            for badge in [120, 121, 122, 123, 124, 125, 126, 127, 145, 42, 54, 55, 0, 1, 6, 7, 9, 16, 17, 18, 28, 29, 30, 33, 34, 35, 46, 47, 50, 51, 57, 58, 59, 64, 65, 69, 71, 73, 129, 130, 131, 132, 133, 134, 139, 142, 144, 147, 153, 154, 158]:
                if badge in badges:
                    p.writeShort(badge).writeShort(0)
                    badges.remove(int(badge))

            for badge in badges:
                p.writeShort(badge).writeShort(0)

            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123]]
            p.writeByte(len(stats))
            for stat in stats:
                p.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeByte(stat[3])

            p.writeByte(player.equipedShamanBadge).writeByte(len(player.shamanBadges))
            for shamanBadge in player.shamanBadges:
                p.writeByte(shamanBadge)

            this.sendPacket(Identifiers.send.Profile, p.writeBytes('\x00\x00\x00\x00\x00').toByteArray())

    def sendPlayerBan(this, hours, reason, silent):
        this.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])
        if not silent and this.room != None:
            for player in this.room.clients.values():
                player.sendLangueMessage("", "<ROSE>$Message_Ban", this.Username, str(hours), reason)

        this.server.disconnectIPAddress(this.ipAddress)

    def sendPlayerEmote(this, emoteID, flag, others, lua):
        p = ByteArray().writeInt(this.playerCode).writeByte(emoteID)
        if not flag == "": p.writeUTF(flag)
        result = p.writeBool(lua).toByteArray()

        this.room.sendAllOthers(this, Identifiers.send.Player_Emote, result) if others else this.room.sendAll(Identifiers.send.Player_Emote, result)

    def sendEmotion(this, emotion):
        this.room.sendAllOthers(this, Identifiers.send.Emotion, ByteArray().writeInt(this.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(this, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        p = ByteArray().writeInt(objectID).writeShort(code).writeShort(px).writeShort(py).writeShort(angle).writeByte(vx).writeByte(vy).writeBool(dur)
        p.writeByte(0) if this.isGuest or sendAll else p.writeBytes(this.shopModule.getShamanItemCustom(code))

        if not sendAll:
            this.room.sendAllOthers(this, Identifiers.send.Spawn_Object, p.toByteArray())
            this.room.objectID = objectID
        else:
            this.room.sendAll(Identifiers.send.Spawn_Object, p.toByteArray())

    def sendAllModerationChat(this, type, message):
        playerName = this.Username if type == -1 else "" if type == 0 else "Message Serveur" if type == 1 else this.Langue.upper() + "][" + ("Admin][" if this.privLevel == 10 else "Coord][" if this.privLevel == 9 else "Smod][" if this.privLevel == 8 else "Mod][" if this.privLevel == 7 else "MapCrew][" if this.privLevel == 6 else "Helper][" if this.privLevel == 5 else "DV][" if this.privLevel == 4 else "LUA][" if this.privLevel == 3 else "")
        if "][" in playerName: playerName += this.Username
        this.server.sendStaffChat(type, this.Langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(playerName).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def sendStaffLogin(this, isDisconnect):
        playerName = "Server][" + ("Admin" if this.privLevel == 10 else "Coord" if this.privLevel == 9 else "SMod" if this.privLevel == 8 else "Mod" if this.privLevel == 7 else "MapCrew" if this.privLevel == 6 else "Helper" if this.privLevel == 5 else "DV" if this.privLevel == 4 else "")
        this.server.sendStaffChat(2, this.Langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(2).writeUTF(playerName).writeUTF(this.Username + " desconectou-se." if isDisconnect else this.Username + " conectou-se.").writeShort(0).writeShort(0).toByteArray())

    def sendTotem(this, totem, x, y, playerCode):
        this.sendPacket(Identifiers.old.send.Totem, [str(playerCode) + "#" + str(x) + "#" + str(y) + totem])

    def sendTotemItemCount(this, number):
        if this.room.isTotemEditeur:
            this.sendPacket(Identifiers.old.send.Totem_Item_Count, ByteArray().writeShort(number * 2).writeShort(0).toByteArray())

    def initTotemEditeur(this):
        if this.RTotem:
            this.sendTotemItemCount(0)
            this.RTotem = False
        else:
            if not this.STotem[1] == "":
                this.Totem[0] = this.STotem[0]
                this.Totem[1] = this.STotem[1]
                this.sendTotemItemCount(int(this.STotem[0]))
                this.sendTotem(this.STotem[1], 400, 202, this.playerCode)
            else:
                this.sendTotemItemCount(0)

    def sendShamanType(this, mode, canDivine):
        this.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBool(canDivine).writeInt(int(this.ShamanColor, 16)).toByteArray())

    def sendBanConsideration(this):
        this.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])
        
    def sendShamanPosition(this, direction):
        this.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(this.playerCode).writeBool(direction).toByteArray())

    def loadCafeMode(this):
        can = this.privLevel >= 5 or (this.Langue.upper() == this.realLangue and this.privLevel != 0 and this.cheeseCount >= 100)
        if not can:
            this.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")

        this.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBool(can).toByteArray())
        p = ByteArray()
        this.Cursor.execute("select * from CafeTopics where Langue = %s order by Date desc limit 0, 20", [this.Langue])
        r = this.Cursor.fetchall()
        for rs in r:
            p.writeInt(rs[0]).writeUTF(rs[1]).writeInt(this.server.getPlayerID(rs[2])).writeInt(rs[4]).writeUTF(rs[3]).writeInt(TFMUtils.getSecondsDiff(rs[5]))
        this.sendPacket(Identifiers.send.Cafe_Topics_List, p.toByteArray())

    def openCafeTopic(this, topicID):
        p = ByteArray().writeBool(True).writeInt(topicID)
        this.Cursor.execute("select * from CafePosts where TopicID = %s order by PostID asc", [topicID])
        r = this.Cursor.fetchall()
        for rs in r:
            p.writeInt(rs[0]).writeInt(this.server.getPlayerID(rs[2])).writeInt(TFMUtils.getSecondsDiff(rs[4])).writeUTF(rs[2]).writeUTF(rs[3]).writeBool(str(this.playerCode) not in rs[6].split(",")).writeShort(rs[5])
        this.sendPacket(Identifiers.send.Open_Cafe_Topic, p.toByteArray())

    def createNewCafeTopic(this, title, message):
        this.server.lastTopicID += 1
        this.Cursor.execute("insert into CafeTopics values (%s, %s, %s, '', 0, %s, %s)", [this.server.lastTopicID, title, this.Username, TFMUtils.getTime(), this.Langue])
        this.server.updateConfig()
        this.createNewCafePost(this.server.lastTopicID, message)
        this.loadCafeMode()

    def createNewCafePost(this, topicID, message):
        commentsCount = 0
        this.server.lastPostID += 1
        this.Cursor.execute("insert into CafePosts values (%s, %s, %s, %s, %s, 0, %s)", [this.server.lastPostID, topicID, this.Username, message, TFMUtils.getTime(), str(this.playerCode)])
        this.Cursor.execute("update CafeTopics set Posts = Posts + 1, LastPostName = %s, Date = %s where TopicID = %s", [this.Username, TFMUtils.getTime(), topicID])
        this.Cursor.execute("select count(*) as count from CafePosts where TopicID = %s", [topicID])
        rs = this.Cursor.fetchone()
        commentsCount = rs[0]
        this.openCafeTopic(topicID)
        for client in this.server.players.values():
            if client.isCafe:
                client.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(this.Username).writeInt(commentsCount).toByteArray())

    def voteCafePost(this, topicID, postID, mode):
        this.Cursor.execute("update cafeposts set Points = Points %s 1, Votes = (case when Votes = '' then %s else (Votes || %s) end) where TopicID = %s and PostID = %s" %("+" if mode else "-"), [this.playerCode, this.playerCode, topicID, postID])

    def sendLangueMessage(this, message1, message2, *args):
        p = ByteArray().writeUTF(message1).writeUTF(message2).writeByte(len(args))
        for arg in args:
            p.writeUTF(arg)
        this.sendPacket(Identifiers.send.Message_Langue, p.toByteArray())

    def sendVampireMode(this, others):
        this.isVampire = True
        p = ByteArray().writeInt(this.playerCode).writeBytes('\xff\xff\xff\xff')
        if others:
            this.room.sendAllOthers(this, Identifiers.send.Vampire_Mode, p.toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Vampire_Mode, p.toByteArray())

    def sendRemoveCheese(this):
        this.room.sendAll(Identifiers.send.Remove_Cheese, ByteArray().writeInt(this.playerCode).toByteArray())

    def sendLuaMessage(this, message):
        this.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def sendGameMode(this, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 11, 2, 10, 16]
        p = ByteArray().writeByte(len(types))
        for roomType in types:
            p.writeByte(roomType)

        p.writeByte(mode)
        modeInfo = this.server.getPlayersCountMode(mode, this.Langue)
        if not modeInfo[0] == "":
            roomsCount = 0
            p.writeUnsignedByte(1).writeUnsignedByte(this.langueByte).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            for checkRoom in this.server.rooms.values():
                if (checkRoom.isNormRoom if mode == 1 else checkRoom.isVanilla if mode == 3 else checkRoom.isSurvivor if mode == 8 else checkRoom.isRacing if mode == 9 else checkRoom.isMusic if mode == 11 else checkRoom.isBootcamp if mode == 2 else checkRoom.isDefilante if mode == 10 else checkRoom.isVillage) and checkRoom.community == this.Langue.lower():
                    roomsCount +=1
                    p.writeUnsignedByte(0).writeUnsignedByte(this.langueByte).writeUTF(checkRoom.roomName).writeUnsignedShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBool(checkRoom.isFuncorp)

            if roomsCount == 0:
                p.writeUnsignedByte(0).writeUnsignedByte(this.langueByte).writeUTF(("" if mode == 1 else str(modeInfo[0].split(" ")[1])) + "1").writeUnsignedShort(0).writeUnsignedByte(200).writeBool(False)
                
        this.sendPacket(Identifiers.send.Game_Mode, p.toByteArray())

    def sendMusicVideo(this, sendAll):
        music = this.room.musicVideos[0]
        p = ByteArray().writeUTF(str(music["VideoID"].encode("UTF-8"))).writeUTF(str(music["Title"].encode("UTF-8"))).writeShort(this.room.musicTime).writeUTF(str(music["By"].encode("UTF-8")))
        if sendAll:
            this.room.musicSkipVotes = 0
            this.room.sendAll(Identifiers.send.Music_Video, p.toByteArray())
        else:
            this.sendPacket(Identifiers.send.Music_Video, p.toByteArray())

    def checkMusicSkip(this):
        if this.room.isMusic and this.room.isPlayingMusic:
            count = this.room.getPlayersCount()
            count = count if count % 2 == 0 else count + 1
            if this.room.musicSkipVotes == count / 2:
                this.room.musicVideos.remove(0)
                this.sendMusicVideo(True)

    def sendStaffMessage(this, message, othersLangues):
        for player in this.server.players.values():
            if othersLangues or player.Langue == this.Langue:
                player.sendMessage(message, True)

    def checkVip(this, vipTime):
        days = TFMUtils.getDiffDays(vipTime)
        if days >= 0:
            this.privLevel = 1
            if this.TitleNumber == 1100:
                this.TitleNumber = 0

            this.sendMessage("O seu VIP se estogou.")
            this.Cursor.execute("update users set VipTime = 0 where Username = %s", [this.Username])
        else:
            this.sendMessage("Você ainda tem <V>"+str(days)+"</V> dias de VIP!")

    def updateTribePoints(this):
        this.Cursor.execute("update Tribe set Points = Points + %s where Code = %s", [this.tribePoints, this.tribeCode])
        this.tribePoints = 0

    def sendLogMessage(this, message):
        this.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(message) >> 16) & 0xFF).writeUnsignedByte((len(message) >> 8) & 0xFF).writeUnsignedByte(len(message) & 0xFF).writeBytes(message).toByteArray())

    def runLuaAdminScript(this, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            startTime = int(time.time())
            endTime = int(time.time())
            totalTime = endTime - startTime
            message = "<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)"
            this.sendLuaMessage(message)
        except Exception as error:
            this.server.sendStaffMessage(7, "<V>["+this.room.roomName+"]<BL> [Bot: "+this.Username+"][Exception]: "+str(error))

    def runLuaScript(this, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            startTime = int(time.time())
            totalTime = int(time.time()) - startTime

            if totalTime > 4000:
                this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script not loaded. ("+str(totalTime)+" ms - 4000 max)")
            else:
                this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)")
        except Exception as error:
            this.sendLuaMessage("<V>["+this.room.roomName+"]<BL> ["+this.Username+"][Exception]: "+str(error))

    def sendAnimZelda(this, type, item):
        if type == 7:
            this.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(this.playerCode).writeByte(type).writeUTF("$De6").writeByte(item).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(this.playerCode).writeByte(type).writeInt(item).toByteArray())

    def sendAnimZeldaInventory(this, id1, id2, count):
        if id1 == 4:
            this.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
            #this.sendData("\x64C", this.put("bhh", 0, id2, count))
        this.room.sendAll([8, 44], ByteArray().writeInt(this.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def premioVillage(this, coisa):
        if coisa[0] == 1:
            medal = coisa[1]
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                if not int(medal) in this.shopBadges:
                    this.shopModule.sendUnlockedBadge(medal)
                    this.shopBadges.append(str(medal))
                    this.playerConsumables[coisa[4]] -= coisa[5]
        elif coisa[0] == 2:
            symbol = str(coisa[1])
            if not symbol in this.shamanBadges:
                if this.shamanBadges[0] == '':
                    this.shamanBadges = [symbol]
                else:
                    test = [symbol]
                    this.shamanBadges = this.shamanBadges + test
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(6, coisa[1], 1)
        elif coisa[0] == 3:
            titles = [str(coisa[1])+".1"]
            #titles = ["387.1"]
            title = random.choice(titles)
            while title in this.titleList:
                try:
                    titles.remove(title)
                    title = random.choice(titles)
                except:
                    break
            if not title in this.titleList:
                stitle = title.split(".")
                this.specialTitleList = this.specialTitleList + [title]
                this.sendUnlockedTitle(stitle[0], stitle[1])

                this.sendCompleteTitleList()
                this.sendTitleList()
        elif coisa[0] == 4:
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                id = coisa[1]
                if not id in this.playerConsumables:
                    this.playerConsumables[id] = coisa[2]
                else:
                    count = this.playerConsumables[id] + coisa[2]
                    this.playerConsumables[id] = count
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(4, id, coisa[2])
        this.BotsVillage(this.botVillage)

    def BotsVillage(this, bot):
        itens = list()
        for item in this.itensBots[bot]:
            if item[0] == 1 and str(item[1]) in this.shopBadges:
                itens.append(item)
            elif item[0] == 2 and str(item[1]) in this.shamanBadges:
                itens.append(item)
            elif item[0] == 3 and str(item[1])+".1" in this.titleList:
                itens.append(item)
        for item in itens:
            this.itensBots[bot].remove(item)
        p = ByteArray()
        for items in this.itensBots[bot]:
            count = items[5]
            if items[4] in this.playerConsumables:
                one = 0 if this.playerConsumables[items[4]] >= count else 1
            else:
                one = 1
            #data += this.put("bbhhbhh", one, *items)
            p.writeByte(one).writeByte(items[0]).writeShort(items[1]).writeShort(items[2]).writeByte(items[3]).writeShort(items[4]).writeShort(items[5]).writeBytes('\x00\x00\x00\x00')
        this.sendPacket([26, 38], ByteArray().writeUTF(bot).writeByte(len(this.itensBots[bot])).toByteArray() + p.toByteArray())

    def sendInventoryConsumables(this):
        p = ByteArray().writeShort(len(this.playerConsumables))
        for id, count in this.playerConsumables.items():
            p.writeShort(str(id)).writeUnsignedByte(250 if count > 250 else count).writeUnsignedByte(0).writeBool(True).writeBool(False if id in this.server.inventory else True).writeBool(True).writeBool(True).writeBool(True).writeBool(False).writeBool(False).writeUnsignedByte(this.equipedConsumables.index(str(id)) + 1 if str(id) in this.equipedConsumables else 0)
        this.sendPacket(Identifiers.send.Inventory, p.toByteArray())
        
    def updateInventoryConsumable(this, id, count):
        this.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray())

    def useInventoryConsumable(this, id):
        if id == 29 or id == 30 or id == 2241:
            this.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())

    def sendTradeResult(this, playerName, result):
        this.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray())

    def sendTradeInvite(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeStart(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray())

    def tradeInvite(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None and (not this.ipAddress == player.ipAddress or this.privLevel == 10 or player.privLevel == 10) and this.privLevel != 0 and player.privLevel != 0:
            if not player.isTrade:
                if not player.room.name == this.room.name:
                    this.sendTradeResult(playerName, 5)
                elif player.isTrade:
                    this.sendTradeResult(playerName, 0)
                else:
                    this.sendLangueMessage("", "$Demande_Envoyée")
                    player.sendTradeInvite(this.playerCode)

                this.tradeName = playerName
                this.isTrade = True
            else:
                this.tradeName = playerName
                this.isTrade = True
                this.sendTradeStart(player.playerCode)
                player.sendTradeStart(this.playerCode)

    def cancelTrade(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None:
            this.tradeName = ""
            this.isTrade = False
            this.tradeConsumables = {}
            this.tradeConfirm = False
            player.tradeName = ""
            player.isTrade = False
            player.tradeConsumables = {}
            player.tradeConfirm = False
            player.sendTradeResult(this.Username, 2)

    def tradeAddConsumable(this, id, isAdd):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.Username:
            if isAdd:
                if this.tradeConsumables.has_key(id):
                    this.tradeConsumables[id] += 1
                else:
                    this.tradeConsumables[id] = 1
            else:
                count = this.tradeConsumables[id] - 1
                if count > 0:
                    this.tradeConsumables[id] = count
                else:
                    del this.tradeConsumables[id]

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBool(False).writeShort(id).writeBool(isAdd).writeByte(1).writeBool(False).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBool(True).writeShort(id).writeBool(isAdd).writeByte(1).writeBool(False).toByteArray())

    def tradeResult(this, isAccept):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.Username:
            this.tradeConfirm = isAccept
            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBool(False).writeBool(isAccept).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBool(True).writeBool(isAccept).toByteArray())
            if this.tradeConfirm and player.tradeConfirm:
                for consumable in player.tradeConsumables.items():
                    if this.playerConsumables.has_key(consumable[0]):
                        this.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        this.playerConsumables[consumable[0]] = consumable[1]

                    count = player.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del player.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            player.equipedConsumables.remove(consumable[0])
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                for consumable in this.tradeConsumables.items():
                    if this.playerConsumables.has_key(consumable[0]):
                        this.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        this.playerConsumables[consumable[0]] = consumable[1]

                    count = this.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del this.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            this.equipedConsumables.remove(consumable[0])
                    else:
                        this.playerConsumables[consumable[0]] = consumable[1]

                player.tradeName = ""
                player.isTrade = False
                player.tradeConsumables = {}
                player.tradeConfirm = False
                player.sendPacket(Identifiers.send.Trade_Close)
                player.sendInventoryConsumables()
                this.tradeName = ""
                this.isTrade = False
                this.tradeConsumables = {}
                this.tradeConfirm = False
                this.sendPacket(Identifiers.send.Trade_Close)
                this.sendInventoryConsumables()

    def giveConsumable(this, id, amount=80, limit=80):
        this.sendAnimZelda(4, id)
        sum = (this.playerConsumables[id] if this.playerConsumables.has_key(id) else 0) + amount
        if limit != -1 and sum > limit: sum = limit
        if this.playerConsumables.has_key(id):
            this.playerConsumables[id] = sum
        else:
            this.playerConsumables[id] = sum

        this.updateInventoryConsumable(id, sum)

    def sendNewConsumable(this, consumable, count):
        this.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray())

    def checkLetters(this, playerLetters):
        needUpdate = False
        letters = playerLetters.split("/")
        for letter in letters:
            if not letter == "":
                values = letter.split("|")
                this.sendPacket(Identifiers.send.Letter, ByteArray().writeUTF(values[0]).writeUTF(values[1]).writeByte(int(values[2])).writeBytes(binascii.unhexlify(values[3])).toByteArray())
                needUpdate = True

        if needUpdate:
            this.Cursor.execute("update users set Letters = '' where Username = %s", [this.Username])

    def getFullItemID(this, category, itemID):
        return itemID + 10000 + 1000 * category if (itemID >= 100) else itemID + 100 * category

    def getSimpleItemID(this, category, itemID):
        return itemID - 10000 - 1000 * category if (itemID >= 10000) else itemID - 100 * category

    def getItemInfo(this, category, itemID):
        shop = map(lambda x: map(int, x.split(",")), this.server.shopList)
        
        return filter(lambda x: x[0] == category and x[1] == itemID, shop)[0] + ([20] if (category != 22) else [0])

class Server(protocol.ServerFactory):
    protocol = Client
    def __init__(this):

        # Settings
        this.DEBUG = bool(int(this.config("DEBUG")))
        this.CKEY = str(this.config("CKEY"))
        this.Version = str(this.config("Version"))
        this.lastPlayerID = int(this.config("Last Player ID"))
        this.lastMapEditeurCode = int(this.config("Last Map Editeur Code"))
        this.needToFirst = int(this.config("Need To First"))
        this.needToBootcamp = int(this.config("Need To Bootcamp"))
        this.lastTribeID = int(this.config("Last Tribe ID"))
        this.lastChatID = int(this.config("Last Chat ID"))
        this.initialCheeses = int(this.config("Initial Cheeses"))
        this.initialFraises = int(this.config("Initial Fraises"))
        this.lastTopicID = int(this.config("Last Topic ID"))
        this.lastPostID = int(this.config("Last Post ID"))
        this.isNowEvent = bool(int(this.config("Now Event")))
        this.adminAllow = this.config("admin Allow").split(", ")
        this.shopList = Config.get("ConfigShop", "Shop List", 0).split(";")
        this.shamanShopList = Config.get("ConfigShop", "Shaman Shop List", 0).split(";")

        # Integer
        this.lastPlayerCode = 0
        this.lastGiftID = 0

        # Nonetype
        this.rebootTimer = None

        # List
        this.loginKeys = []
        this.packetKeys = []
        this.userMuteCache = []
        this.tempIPBanList = []
        this.userMuteCache = []
        this.tempIPBanList = []
        this.shopPromotions = []
        this.ipPermaBanCache = []
        this.userTempBanCache = []
        this.userPermaBanCache = []

        # Dict
        this.reports = {"names": []}
        this.rooms = {}
        this.players = {}
        this.shopListCheck = {}
        this.shamanShopListCheck = {}
        this.shopGifts = {}
        this.chatMessages = {}
        this.connectedCounts = {}
        this.cheeseTitleList = {5:5.1, 20:6.1, 100:7.1, 200:8.1, 300:35.1, 400:36.1, 500:37.1, 600:26.1, 700:27.1, 800:28.1, 900:29.1, 1000:30.1, 1100:31.1, 1200:32.1, 1300:33.1, 1400:34.1, 1500:38.1, 1600:39.1, 1700:40.1, 1800:41.1, 2000:72.1, 2300:73.1, 2700:74.1, 3200:75.1, 3800:76.1, 4600:77.1, 6000:78.1, 7000:79.1, 8000:80.1, 9001:81.1, 10000:82.1, 14000:83.1, 18000:84.1, 22000:85.1, 26000:86.1, 30000:87.1, 34000:88.1, 38000:89.1, 42000:90.1, 46000:91.1, 50000:92.1, 55000:234.1, 60000:235.1, 65000:236.1, 70000:237.1, 75000:238.1, 80000:93.1}
        this.firstTitleList = {1:9.1, 10:10.1, 100:11.1, 200:12.1, 300:42.1, 400:43.1, 500:44.1, 600:45.1, 700:46.1, 800:47.1, 900:48.1, 1000:49.1, 1100:50.1, 1200:51.1, 1400:52.1, 1600:53.1, 1800:54.1, 2000:55.1, 2200:56.1, 2400:57.1, 2600:58.1, 2800:59.1, 3000:60.1, 3200:61.1, 3400:62.1, 3600:63.1, 3800:64.1, 4000:65.1, 4500:66.1, 5000:67.1, 5500:68.1, 6000:69.1, 7000:231.1, 8000:232.1, 9000:233.1, 10000:70.1, 12000:224.1, 14000:225.1, 16000:226.1, 18000:227.1, 20000:202.1, 25000:228.1, 30000:229.1, 35000:230.1, 40000:71.1}
        this.shamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
        this.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
        this.bootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}
        this.hardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
        this.divineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
        this.shopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2205:38, 2220:25, 2221:32, 2215:37, 2222:39, 2236:36, 2204:40, 2238:41, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:69, 2254:70, 10132:71, 2255:72, 2256:128, 10133:129, 422:130, 124:73, 2257:135, 2258:136, 2259:137, 2260:138, 2262:140, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175, 2281:176, 2282:177, 2283:178}
        this.inventory = [2202, 2203, 2204, 2227, 2235, 2257, 2261, 2253, 2254, 2260, 2261, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2276, 2277, 2278, 2279, 2280, 2281, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2327, 2328]
        # Others
        this.Cursor = Cursor
        this.parseShop()
        this.parseBanList()
        this.parseShamanShop()
        this.captchaList = this.parseJson("./include/captcha.json")
        this.blackList = this.parseJson("./include/blackList.json")
        this.promotions = this.parseJson("./include/promotions.json")
        this.parsePromotions()

    def buildCaptchaCode(this):
        chars = this.captchaList.keys()
        CC = "".join([random.choice(chars) for x in range(4)])
        words = list(CC)
        px, py = 0, 1
        lines = []
        for count in range(1, 17):
            wc = 1
            values = []
            for word in words:
                ws = this.captchaList[word]
                if count > len(ws):
                    count = len(ws)
                ws = ws[str(count)]
                values += ws.split(",")[(1 if wc > 1 else 0):]
                wc += 1
            lines += [",".join(map(str, values))]
            if px < len(values):
                px = len(values)
            py += 1
        return [CC, (px + 2), 17, lines]

    def updateConfig(this):
        this.configs("Last Player ID", str(this.lastPlayerID))
        this.configs("Last Map Editeur Code", str(this.lastMapEditeurCode))
        this.configs("Last Tribe ID", str(this.lastTribeID))
        this.configs("Last Chat ID", str(this.lastChatID))
        this.configs("Last Topic ID", str(this.lastTopicID))
        this.configs("Last Post ID", str(this.lastPostID))
                
    def parseShop(this):
        for item in this.shopList:
            values = item.split(",")
            this.shopListCheck[values[0] + "|" + values[1]] = [int(values[5]), int(values[6])]

    def parseShamanShop(this):
        for item in this.shamanShopList:
            values = item.split(",")
            this.shamanShopListCheck[values[0]] = [int(values[3]), int(values[4])]

    def sendOutput(this, message):
        print "["+(str(time.strftime("%H:%M:%S")))+"] " + message

    def config(this, setting):
        return Config.get("Settings", setting, 0)

    def configs(this, setting, value):
        Config.set("Settings", setting, value)
        with open("./include/Config.ini", "w") as f:
            Config.write(f)

    def parseJson(this, directory):
        with open(directory, "r") as f:
            return eval(f.read())

    def updateBlackList(this):
        with open("./include/blackList.json", "w") as f:
            json.dump(str(this.blackList), f)
                    
    def sendServerReboot(this):
        this.sendServerRestart(0, 0)
        reactor.callLater(120, this.closeServer)

    def sendServerRestart(this, no, sec):
        if sec > 0 or no != 5:
            this.sendServerRestartSEC(120 if no == 0 else 60 if no == 1 else 30 if no == 2 else 20 if no == 3 else 10 if no == 4 else sec)
            if this.rebootTimer != None: this.rebootTimer.cancel()
            this.rebootTimer = reactor.callLater(60 if no == 0 else 30 if no == 1 else 10 if no == 2 or no == 3 else 1, lambda: this.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else sec - 1 if no == 5 else 0))

    def sendServerRestartSEC(this, seconds):
        this.sendPanelRestartMessage(seconds)
        this.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(this, seconds):
        if seconds == 120:
            this.sendOutput("[SERVER] The server will restart in 2 minutes.")
        elif seconds < 120 and seconds > 1:
            this.sendOutput("[SERVER] The server will restart in "+str(seconds)+" seconds.")
        else:
            this.sendOutput("[SERVER] The server will restart in 1 second.")

    def closeServer(this):
        this.updateConfig()
        for client in this.players.values():
            client.transport.loseConnection()
            del this.players[client.Username]

        os._exit(0)

    def getConnectedPlayerCount(this):
        return len(this.players)

    def getRoomsCount(this):
        return len(this.rooms)

    def checkAlreadyExistingGuest(this, playerName):
        found = False
        result = ""

        if not this.checkConnectedAccount(playerName):
            found = True
            result = playerName

        while not found:
            tempName = playerName + "_" + TFMUtils.getRandomChars(4)
            if not this.checkConnectedAccount(tempName):
                found = True
                result = tempName
        return result

    def checkConnectedAccount(this, playerName):
        return this.players.has_key(playerName)

    def disconnectIPAddress(this, ip):
        for client in this.players.values():
            if client.ipAddress == ip:
                client.transport.loseConnection()

    def checkExistingUser(this, playerName):
        this.Cursor.execute("select * from Users where Username = %s", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def recommendRoom(this, langue):
        found = False
        x = 0
        result = ""
        while not found:
            x += 1
            if this.rooms.has_key(langue + "-" + str(x)):
                if this.rooms[langue + "-" + str(x)].getPlayerCount() < 25:
                    found = True
                    result = str(x)
            else:
                found = True
                result = str(x)
        return result

    def checkRoom(this, roomName, langue):
        found = False
        x = 0
        result = roomName
        if this.rooms.has_key(langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName):
            room = this.rooms.get(langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if this.rooms.has_key((langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x)):
                room = this.rooms.get((langue + "-" + roomName if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result

    def addClientToRoom(this, client, roomName):
        if this.rooms.has_key(roomName):
            this.rooms[roomName].addClient(client)
        else:
            room = Room(this, roomName)
            this.rooms[roomName] = room
            room.addClient(client)

    def getIPPermaBan(this, ip):
        return ip in this.ipPermaBanCache

    def checkReport(this, array, playerName):
        return playerName in array

    def banPlayer(this, playerName, bantime, reason, modname, silent):        
        found = False

        client = this.players.get(playerName)
        if client != None:
            found = True
            if not modname == "Server":
                client.banHours += bantime
                ban = str(time.time())
                bandate = ban[:len(ban) - 4]
                this.Cursor.execute("insert into BanLog values (%s, %s, %s, %s, %s, 'Online', %s, %s)", [playerName, modname, str(bantime), reason, bandate, client.roomName, client.ipAddress])
            else:
                this.sendStaffMessage(5, "<V>Server <BL>banned player <V>"+playerName+"<BL> for <V>1 <BL> hour. Reason: <V>Vote Populaire<BL>.")

            this.Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])

            if bantime >= 361 or client.banHours >= 361:
                this.userPermaBanCache.append(playerName)
                this.Cursor.execute("insert into UserPermaBan values (%s, %s, %s)", [playerName, modname, reason])

            if client.banHours >= 361:
                this.ipPermaBanCache.append(client.ipAddress)
                this.Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [client.ipAddress, modname, reason])

            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)
                this.tempBanIP(client.ipAddress, bantime)

            if this.checkReport(this.reports["names"], playerName):
                this.reports[playerName]["status"] = "banned"
                this.reports[playerName]["status"] = "modname"
                this.reports[playerName]["status"] = str(bantime)
                this.reports[playerName]["banreason"] = "hack"

            client.sendPlayerBan(bantime, reason, silent)

        if not found and this.checkExistingUser(playerName) and not modname == "Server" and bantime >= 1:
            found = True
            totalBanTime = this.getTotalBanHours(playerName) + bantime
            if (totalBanTime >= 361 and bantime <= 360) or bantime >= 361:
                this.userPermaBanCache.append(playerName)
                this.Cursor.execute("insert into UserPermaBan values (%s, %s, %s)", [playerName, modname, reason])

            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)

            this.Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])

            ban = str(time.time())
            bandate = ban[:len(ban) - 4]
            this.Cursor.execute("insert into BanLog values (%s, %s, %s, %s, %s, 'Offline', '', 'Offline')", [playerName, modname, str(bantime), reason, bandate])

        return found

    def checkTempBan(this, playerName):
        this.Cursor.execute("select * from UserTempBan where Name = %s", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def removeTempBan(this, playerName):
        try:
            this.userTempBanCache.remove(playerName)
            this.Cursor.execute("delete from UserTempBan where Name = %s", [playerName])
        except: pass

    def tempBanUser(this, playerName, bantime, reason):
        if this.checkTempBan(playerName):
            this.removeTempBan(playerName)

        this.userTempBanCache.append(playerName)
        this.Cursor.execute("insert into UserTempBan values (%s, %s, %s)", [playerName, str(TFMUtils.getTime() + (bantime * 60 * 60)), reason])

    def getTempBanInfo(this, playerName):
        this.Cursor.execute("select Reason, Time from UserTempBan where Name = %s", [playerName])
        r = this.Cursor.fetchall()
        for rs in r:
            return [rs[0], rs[1]]
        return ["", 0]

    def checkPermaBan(this, playerName):
        this.Cursor.execute("select * from UserPermaBan where Name = %s", [playerName])
        if this.Cursor.fetchone():
            return True
        return False

    def removePermaBan(this, playerName):
        try:
            this.userPermaBanCache.remove(playerName)
            this.Cursor.execute("delete from UserPermaBan where Name = %s", [playerName])
        except: pass

    def tempBanIP(this, ip, time):
        if not ip in this.tempIPBanList:
            this.tempIPBanList.append(ip)
            reactor.callLater(time, lambda: this.tempIPBanList.remove(ip))

    def getTotalBanHours(this, playerName):
        this.Cursor.execute("select BanHours from Users where Username = %s", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs[0]
        return 0

    def parseBanList(this):
        this.Cursor.execute("select ip from IPPermaBan")
        rs = this.Cursor.fetchone()
        if rs:
            this.ipPermaBanCache.append(rs[0])

        this.Cursor.execute("select Name from UserPermaBan")
        rs = this.Cursor.fetchone()
        if rs:
            this.userPermaBanCache.append(rs[0])

        this.Cursor.execute("select Name from UserTempBan")
        rs = this.Cursor.fetchone()
        if rs:
            this.userTempBanCache.append(rs[0])

        this.Cursor.execute("select Name from UserTempMute")
        rs = this.Cursor.fetchone()
        if rs:
            this.userMuteCache.append(rs[0])

    def voteBanPopulaire(this, playerName, ip):
        client = this.players.get(playerName)
        if client != None and client.privLevel == 1 and not ip in client.voteBan:
            client.voteBan.append(ip)
            if len(client.voteBan) == 10:
                this.banPlayer(playerName, 1, "Vote Populaire", "Server", False)

    def muteUser(this, playerName, mutetime, reason):
        this.userMuteCache.append(playerName)
        this.Cursor.execute("insert into UserTempMute values (%s, %s, %s)", [playerName, str(TFMUtils.getTime() + (mutetime * 60 * 60)), reason])

    def removeModMute(this, playerName):
        try:
            this.userMuteCache.remove(playerName)
            this.Cursor.execute("delete from UserTempMute where Name = %s", [playerName])
        except:pass

    def getModMuteInfo(this, playerName):
        this.Cursor.execute("select Time, Reason from UserTempMute where Name = %s", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return [rs[0], rs[1]]
        return [0, ""]

    def mutePlayer(this, playerName, time, reason, modname):
        client = this.players.get(playerName)
        if client != None:
            this.sendStaffMessage(5, "<V>"+str(modname)+"<BL> left the player <V>"+playerName+"<BL> without talking for <V>"+str(time)+"<BL> "+str("hora" if time == 1 else "hours")+". Reason: <V>"+str(reason))
            if playerName in this.userMuteCache:
                this.removeModMute(playerName)

            for player in client.room.clients.values():
                if player.Username != playerName:
                    player.sendLangueMessage("", "<ROSE>$MuteInfo2", playerName, str(time), reason)

            client.isMute = True
            client.sendLangueMessage("", "<ROSE>$MuteInfo1", str(time), reason)
            this.muteUser(playerName, time, reason)

    def desmutePlayer(this, playerName, modname):
        client = this.players.get(playerName)
        if client != None:
            this.sendStaffMessage(5, "<V>"+str(modname)+"<N> was unmuted <V>"+playerName+"<BL>.")
            this.removeModMute(playerName)
            client.isMute = False

    def sendStaffChat(this, type, langue, identifiers, packet):
        minLevel = 0 if type == -1 or type == 0 else 1 if type == 1 else 7 if type == 3 or type == 4 else 5 if type == 2 or type == 5 else 6 if type == 7 or type == 6 else 3 if type == 8 else 4 if type == 9 else 0
        for client in this.players.values():
            if client.privLevel >= minLevel and client.Langue == langue or type == 1 or type == 4 or type == 5:
                client.sendPacket(identifiers, packet)

    def getTotemData(this, playerName):
        if playerName.startswith("*"):
            return []
        else:
            this.Cursor.execute("select ItemCount, Totem from Totem where Name = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                itemCount = rs[0]
                totem = rs[1]
                totem = totem.replace("%", chr(1))
                return [str(itemCount), totem]
        return []

    def setTotemData(this, playerName, ItemCount, totem):
        if playerName.startswith("*"):
            pass
        else:
            totem = totem.replace(chr(1), "%")

            if len(this.getTotemData(playerName)) != 0:
                this.Cursor.execute("update Totem set ItemCount = %s, Totem = %s where Name = %s", [ItemCount, totem, playerName])
            else:
                this.Cursor.execute("insert into Totem values (%s, %s, %s)", [playerName, ItemCount, totem])

    def getShamanType(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.shamanType

        return 0

    def getShamanLevel(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.shamanLevel
        return 0

    def getShamanBadge(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.skillModule.getShamanBadge()
        
        return 0

    def getPlayerAvatar(this, playerName):
        this.Cursor.execute("select Avatar from Users where Username = %s", [playerName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs[0]
        return 0

    def getPlayerID(this, playerName):
        if playerName.startswith("*"):
            return 0

        elif this.players.has_key(playerName):
            return this.players[playerName].playerID
        else:
            this.Cursor.execute("select PlayerID from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs[0]
        return 0

    def getPlayerPrivlevel(this, playerName):
        if playerName.startswith("*"):
            return 0

        elif this.players.has_key(playerName):
            return this.players[playerName].privLevel
        else:
            this.Cursor.execute("select PrivLevel from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs[0]
        return 0

    def getPlayerName(this, playerID):
        this.Cursor.execute("select Username from Users where PlayerID = %s", [playerID])
        rs = this.Cursor.fetchone()
        if rs:
            return rs[0]
        return ""

    def getPlayerRoomName(this, playerName):
        if this.players.has_key(playerName):
            return this.players[playerName].roomName
        return ""

    def getTribeInfo(this, tribeCode):
        tribeRankings = {}
        this.Cursor.execute("select * from Tribe where Code = %s", [tribeCode])
        rs = this.Cursor.fetchone()
        if rs:
            for rank in rs[4].split(";"):
                values = rank.split("|", 1)
                tribeRankings[int(values[0])] = values[1]
            return [rs[1], rs[2], rs[3], tribeRankings, rs[7]]
        return ["", "", 0, tribeRankings, 0]

    def getTribeHouse(this, tribeName):
        this.Cursor.execute("select House from Tribe where Name = %s", [tribeName])
        rs = this.Cursor.fetchone()
        if rs:
            return rs[0]
        return -1

    def getPlayersCountMode(this, mode, langue):
        modeName = "Transformice" if mode == 1 else "Transformice vanilla" if mode == 3 else "Transformice survivor" if mode == 8 else "Transformice racing" if mode == 9 else "Transformice music" if mode == 11 else "Transformice bootcamp" if mode == 2 else "Transformice defilante" if mode == 10 else "Transformice village" if mode == 16 else ""
        playerCount = 0
        for room in this.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor if mode == 8 else room.isRacing if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante if mode == 10 else room.isVillage if mode == 16 else True) and room.community == langue.lower()):
                playerCount += room.getPlayerCount()
        return [modeName, playerCount]

    def parsePromotions(this):
        needUpdate = False
        i = 0
        while i < len(this.promotions):
            item = this.promotions[i]                
            if item[3] < 1000:
                item[3] = TFMUtils.getTime() + item[3] * 86400 + 30
                needUpdate = True
            
            this.shopPromotions.append([item[0], item[1], item[2], item[3]])
            i += 1
        
        this.checkPromotionsEnd()

    def checkPromotionsEnd(this):
        needUpdate = False
        for promotion in this.shopPromotions:
            if TFMUtils.getHoursDiff(promotion[3]) <= 0:
                this.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(this.promotions):
                    if this.promotions[i][0] == promotion[0] and this.promotions[i][1] == promotion[1]:
                        this.promotions.remove(i)
                    i += 1

    def sendWholeServer(this, identifiers, result):
        for client in this.players.values():
            client.sendPacket(identifiers, result)

    def checkMessage(this, client, message):
        list = this.blackList["list"]
        i = 0
        while i < len(list):
            if re.search("[^a-zA-Z]*".join(list[i]), message.lower()):
                this.sendStaffMessage(7, "[<V>" + client.roomName + "</V>][<T>" + client.Username + "</T>] sent a link in the message: [<J>" + str(message) + "</J>].")
                return True
            i += 1
        return False

    def setVip(this, playerName, days):
        player = this.players.get(playerName)
        if ((player != None and player.privLevel == 1) or this.getPlayerPrivlevel(playerName) == 1):
            this.Cursor.execute("update users set VipTime = %s where Username = %s" if player != None else "update users SET VipTime = %s, PrivLevel = 2 where Username = %s", [TFMUtils.getTime() + (days * 24 * 3600), playerName])
            if player != None:
                player.privLevel = 2

            this.sendStaffMessage(7, "<V>"+playerName+"</V> became VIP for <V>"+str(days)+"</V> days.")
            return True
        
        return False

    def getPlayerCode(this, playerName):
        client = this.players.get(TFMUtils.parsePlayerName(playerName))
        return client.playerCode if player != None else 0

    def sendStaffMessage(this, minLevel, message):
        for client in this.players.values():
            if client.privLevel >= minLevel:
                client.sendMessage(message)        

class Room:
    def __init__(this, server, name):

        # String
        this.currentSyncName = ""
        this.currentShamanName = ""
        this.currentSecondShamanName = ""
        this.forceNextMap = "-1"
        this.mapName = ""
        this.mapXML = ""
        this.EMapXML = ""
        this.roomPassword = ""        

        # Integer        
        this.maxPlayers = 200
        this.currentMap = 0
        this.lastRoundCode = 0
        this.mapCode = -1
        this.mapYesVotes = 0
        this.mapNoVotes = 0
        this.mapPerma = -1
        this.mapStatus = 0
        this.currentSyncCode = -1
        this.roundTime = 120
        this.gameStartTime = 0
        this.currentShamanCode = -1
        this.currentSecondShamanCode = -1
        this.currentShamanType = -1
        this.currentSecondShamanType = -1
        this.forceNextShaman = -1
        this.numCompleted = 0
        this.FSnumCompleted = 0
        this.SSnumCompleted = 0
        this.receivedNo = 0
        this.receivedYes = 0
        this.EMapLoaded = 0
        this.EMapCode = 0
        this.objectID = 0
        this.tempTotemCount = -1
        this.addTime = 0
        this.cloudID = -1
        this.companionBox = -1
        this.mulodromeRoundCount = 0
        this.redCount = 0
        this.blueCount = 0
        this.musicMapStatus = 0
        this.roundsCount = -1
        this.survivorMapStatus = 0
        this.lastImageID = 0
        this.changeMapAttemps = 0
        this.musicSkipVotes = 0
        this.musicTime = 0

        this.gameStartTimeMillis = 0

        # Bool
        this.discoRoom = False
        this.isClosed = False
        this.isCurrentlyPlay = False
        this.isDoubleMap = False
        this.isNoShamanMap = False
        this.isVotingMode = False
        this.initVotingMode = True
        this.isVotingBox = False
        this.EMapValidated = False
        this.countStats = True
        this.never20secTimer = False
        this.isVanilla = False
        this.isEditeur = False
        this.changed20secTimer = False
        this.specificMap = False
        this.noShaman = False
        this.isTutorial = False
        this.isTotemEditeur = False
        this.autoRespawn = False
        this.noAutoScore = False
        this.catchTheCheeseMap = False
        this.isTribeHouse = False
        this.isTribeHouseMap = False
        this.isMulodrome = False
        this.isRacing = False
        this.isMusic = False
        this.isPlayingMusic = False
        this.isRacingP17 = False
        this.isBootcamp = False
        this.isBootcampP13 = False
        this.isSurvivor = False
        this.isSurvivorVamp = False
        this.isDefilante = False
        this.isNormRoom = False
        this.isSnowing = False
        this.canChangeMap = True
        this.disableAfkKill = False
        this.isFixedMap = False
        this.noShamanSkills = False
        this.is801Room = False
        this.mapInverted = False
        this.canChangeMusic = True
        this.isFuncorp = False
        this.isVillage = False

        # Bool
        this.changeMapTimer = None
        this.closeRoomRoundJoinTimer = None
        this.voteCloseTimer = None
        this.killAfkTimer = None
        this.autoRespawnTimer = None
        this.endSnowTimer = None
        this.startTimerLeft = None

        # List Arguments
        this.MapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.anchors = []
        this.lastHandymouse = [-1, -1]
        this.musicVideos = []

        # List
        this.redTeam = []
        this.blueTeam = []
        this.roomTimers = []
        this.adminsRoom = []
        this.playersBan = []

        # Dict
        this.clients = {}
        this.currentShamanSkills = {}
        this.currentSecondShamanSkills = {}
        this.currentTimers = {}

        # Others
        this.name = name
        this.server = server
        this.Cursor = Cursor

        if this.name.startswith("*"):
            this.community = "xx"
            this.roomName = this.name
        else:
            this.community = this.name.split("-")[0].lower()
            this.roomName = this.name.split("-")[1]

        if this.roomName.startswith(chr(3) + "[Editeur] "):
            this.countStats = False
            this.isEditeur = True
            this.never20secTimer = True

        elif this.roomName.startswith(chr(3) + "[Tutorial] "):
            this.countStats = False
            this.currentMap = 900
            this.specificMap = True
            this.noShaman = True
            this.never20secTimer = True
            this.isTutorial = True

        elif this.roomName.startswith(chr(3) + "[Totem] "):
            this.countStats = False
            this.specificMap = True
            this.currentMap = 444
            this.isTotemEditeur = True
            this.never20secTimer = True

        elif this.roomName.startswith("*" + chr(3)):
            this.countStats = False
            this.isTribeHouse = True
            this.autoRespawn = True
            this.never20secTimer = True
            this.noShaman = True

        elif this.roomName.startswith("music") or this.roomName.startswith("*music"):
            this.isMusic = True

        elif this.roomName.startswith("racing") or this.roomName.startswith("*racing"):
            this.isRacing = True
            this.noShaman = True
            this.roundTime = 63

        elif this.roomName.startswith("bootcamp") or this.roomName.startswith("*bootcamp"):
            this.isBootcamp = True
            this.countStats = False
            this.roundTime = 360
            this.never20secTimer = True
            this.autoRespawn = True
            this.noShaman = True

        elif this.roomName.startswith("vanilla") or this.roomName.startswith("*vanilla"):
            this.isVanilla = True

        elif this.roomName.startswith("survivor") or this.roomName.startswith("*survivor"):
            this.isSurvivor = True
            this.roundTime = 90

        elif this.roomName.startswith("defilante") or this.roomName.startswith("*defilante"):
            this.isDefilante = True
            this.noShaman = True
            this.countStats = False
            this.noAutoScore = True

        elif this.roomName.startswith("village") or this.roomName.startswith("*village"):
            this.isVillage = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True

        elif this.roomName.startswith("801") or this.roomName.startswith("*801"):
            this.is801Room = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True
        else:
            this.isNormRoom = True

        this.mapChange()

    def startTimer(this):
        for client in this.clients.values():
            client.sendMapStartTimerEnd()

    def mapChange(this):
        if this.changeMapTimer != None: this.changeMapTimer.cancel()
        
        if not this.canChangeMap:
            this.changeMapAttemps += 1
            if this.changeMapAttemps < 5:
                this.changeMapTimer = reactor.callLater(1, this.mapChange)
                return

        for timer in this.roomTimers:
            timer.cancel()

        this.roomTimers = []

        for timer in [this.voteCloseTimer, this.killAfkTimer, this.autoRespawnTimer, this.startTimerLeft]:
            if timer != None:
                timer.cancel()

        if this.initVotingMode:
            if not this.isVotingBox and (this.mapPerma == 0 and this.mapCode != -1) and this.getPlayerCount() >= 2:
                this.isVotingMode = True
                this.isVotingBox = True
                this.voteCloseTimer = reactor.callLater(8, this.closeVoting)
                for client in this.clients.values():
                    client.sendPacket(Identifiers.old.send.Vote_Box, [this.mapName, this.mapYesVotes, this.mapNoVotes])
            else:
                this.votingMode = False
                this.closeVoting()

        elif this.isTribeHouse and this.isTribeHouseMap:
            pass
        else:
            if this.isVotingMode:
                TotalYes = this.mapYesVotes + this.receivedYes
                TotalNo = this.mapNoVotes + this.receivedNo
                isDel = False

                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = (1.0 * TotalYes / TotalNo) * 100
                    rate = str(Rating).split(".")
                    if int(rate[0]) < 50:
                        isDel = True
                this.Cursor.execute("update MapEditor set YesVotes = %s, NoVotes = %s, Perma = 44 where Code = %s", [TotalYes, TotalNo, this.mapCode]) if isDel else this.Cursor.execute("update MapEditor set YesVotes = %s, NoVotes = %s where Code = %s", [TotalYes, TotalNo, this.mapCode])
                this.isVotingMode = False
                this.receivedNo = 0
                this.receivedYes = 0
                for client in this.clients.values():
                    client.qualifiedVoted = False
                    client.isVoted = False

            this.initVotingMode = True

            this.lastRoundCode += 1
            this.lastRoundCode %= 127

            if this.isSurvivor:
                for client in this.clients.values():
                    if not client.isDead and (not client.isVampire if this.isSurvivorVamp else not client.isShaman):
                        if not this.noAutoScore: client.playerScore += 10

            if this.catchTheCheeseMap:
                this.catchTheCheeseMap = False
            else:
                numCom = this.FSnumCompleted - 1 if this.isDoubleMap else this.numCompleted - 1
                numCom2 = this.SSnumCompleted - 1 if this.isDoubleMap else 0
                if numCom < 0: numCom = 0
                if numCom2 < 0: numCom2 = 0

                player = this.clients.get(this.currentShamanName)
                if player != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentShamanName, numCom])
                    if not this.noAutoScore: player.playerScore = numCom
                    if numCom > 0:
                        player.skillModule.earnExp(True, numCom)

                player2 = this.clients.get(this.currentSecondShamanName)
                if player2 != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentSecondShamanName, numCom2])
                    if not this.noAutoScore: player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.skillModule.earnExp(True, numCom2)

            if this.isSurvivor and this.getPlayerCount() >= this.server.needToFirst:
                this.giveSurvivorStats()
            elif this.isRacing and this.getPlayerCount() >= this.server.needToFirst:
                this.giveRacingStats()

            this.currentSyncCode = -1
            this.currentSyncName = ""
            this.currentShamanCode = -1
            this.currentSecondShamanCode = -1
            this.currentShamanName = ""
            this.currentSecondShamanName = ""
            this.currentShamanType = -1
            this.currentSecondShamanType = -1
            this.currentShamanSkills = {}
            this.currentSecondShamanSkills = {}
            this.changed20secTimer = False
            this.isDoubleMap = False
            this.isNoShamanMap = False
            this.FSnumCompleted = 0
            this.SSnumCompleted = 0
            this.objectID = 0
            this.tempTotemCount = -1
            this.addTime = 0
            this.cloudID = -1
            this.companionBox = -1
            this.lastHandymouse = [-1, -1]
            this.isTribeHouseMap = False
            this.canChangeMap = True
            this.changeMapAttemps = 0

            this.getSyncCode()

            this.anchors = []

            this.mapStatus += 1
            this.mapStatus %= 13
            this.musicMapStatus += 1
            this.musicMapStatus %= 6
            this.survivorMapStatus += 1
            this.survivorMapStatus %= 11

            this.isRacingP17 = not this.isRacingP17
            this.isBootcampP13 = not this.isBootcampP13

            this.numCompleted = 0
            this.canChangeMusic = True

            this.currentMap = this.selectMap()
            this.checkVanillaXML()

            if not this.noShamanSkills:
                player = this.clients.get(this.currentShamanName)
                if player != None:
                    if this.currentShamanName != None:
                        player.skillModule.getTimeSkill()

                    if this.currentSecondShamanName != None:
                        player.skillModule.getTimeSkill()

            if this.currentMap in [range(44, 54), range(138, 144)] or this.mapPerma == 8 and this.getPlayerCount() >= 2:
                this.isDoubleMap = True

            if this.mapPerma == 7 or this.mapPerma == 42 or this.isSurvivorVamp:
                this.isNoShamanMap = True

            if this.currentMap in range(108, 114):
                this.catchTheCheeseMap = True

            this.gameStartTime = TFMUtils.getTime()
            this.gameStartTimeMillis = time.time()
            this.isCurrentlyPlay = False

            for player in this.clients.values():
                player.resetPlay()

            for player in this.clients.values():
                player.startPlay()
                if player.isHidden:
                    player.sendPlayerDisconnect()

            for player in this.clients.values():
                if player.pet != 0:
                    if TFMUtils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        this.sendAll(Identifiers.send.Pet, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.pet).toByteArray())

            if this.isSurvivorVamp:
                reactor.callLater(5, this.sendVampireMode)

            if this.isMulodrome:
                this.mulodromeRoundCount += 1
                this.sendMulodromeRound()

                if this.mulodromeRoundCount <= 10:
                    for client in this.clients.values():
                        if client.Username in this.blueTeam:
                            this.setNameColor(client.Username, int("979EFF", 16))
                        else:
                            this.setNameColor(client.Username, int("FF9396", 16))
            else:
                this.sendAll(Identifiers.send.Mulodrome_End)

            if this.isRacing or this.isDefilante:
                this.roundsCount += 1
                this.roundsCount %= 10
                player = this.clients.get(this.getHighestScore())
                this.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(this.roundsCount).writeInt(player.playerCode if player != None else 0).toByteArray())

            this.startTimerLeft = reactor.callLater(3, this.startTimer)
            this.closeRoomRoundJoinTimer = reactor.callLater(3, setattr, this, "isCurrentlyPlay", True)
            if not this.isFixedMap and not this.isTribeHouse and not this.isTribeHouseMap:
                this.changeMapTimer = reactor.callLater(this.roundTime + this.addTime, this.mapChange)
            
            this.killAfkTimer = reactor.callLater(30, this.killAfk)
            if this.autoRespawn or this.isTribeHouseMap:
                this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)

    def getPlayerCount(this):
        return len(filter(lambda player: not player.isHidden, this.clients.values()))

    def getPlayerCountUnique(this):
        ipList = []
        for client in this.clients.values():
            if not client.ipAddress in ipList:
                ipList.append(client.ipAddress)
        return len(ipList)

    def getPlayerList(this):
        result = []
        for client in this.clients.values():
            if not client.isHidden:
                result.append(client.getPlayerData())
        return result

    def addClient(this, client):
        this.clients[client.Username] = client

        client.room = this
        client.isDead = this.isCurrentlyPlay
        this.sendAllOthers(client, Identifiers.send.Player_Respawn, ByteArray().writeBytes(client.getPlayerData()).writeBool(False).writeBool(True).toByteArray())
        client.startPlay()

    def removeClient(this, client):
        if client.Username in this.clients:
            del this.clients[client.Username]
            client.resetPlay()
            client.playerScore = 0
            client.sendPlayerDisconnect()

            if this.isMulodrome:
                if client.Username in this.redTeam: this.redTeam.remove(client.Username)
                if client.Username in this.blueTeam: this.blueTeam.remove(client.Username)

                if len(this.redTeam) == 0 and len(this.blueTeam) == 0:
                    this.mulodromeRoundCount = 10
                    this.sendMulodromeRound()

            if len(this.clients) == 0:
                for timer in [this.autoRespawnTimer, this.changeMapTimer, this.closeRoomRoundJoinTimer, this.endSnowTimer, this.killAfkTimer, this.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()
                        
                this.isClosed = True
                del this.server.rooms[this.name]
            else:
                if client.playerCode == this.currentSyncCode:
                    this.currentSyncCode = -1
                    this.currentSyncName = ""
                    this.getSyncCode()
                    for clientOnline in this.clients.values():
                        clientOnline.sendSync(this.currentSyncCode)
                this.checkShouldChangeMap()

    def checkShouldChangeMap(this):
        if this.isBootcamp or this.autoRespawn or (this.isTribeHouse and this.isTribeHouseMap) or this.isFixedMap:
            pass
        else:
            allDead = True
            for client in this.clients.values():
                if not client.isDead:
                    allDead = False

            if allDead:
                this.mapChange()

    def sendAll(this, identifiers, packet=""):
        for client in this.clients.values():
            client.sendPacket(identifiers, packet)

    def sendAllOthers(this, senderClient, identifiers, packet=""):
        for client in this.clients.values():
            if not client == senderClient:
                client.sendPacket(identifiers, packet)

    def sendAllChat(this, playerCode, playerName, message, LangueByte, isOnly):
        p = ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(LangueByte).writeUTF(message)
        if not isOnly:
            for client in this.clients.values():
                client.sendPacket(Identifiers.send.Chat_Message, p.toByteArray())
        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.Chat_Message, p.toByteArray())

    def getSyncCode(this):
        if this.getPlayerCount() > 0:
            if this.currentSyncCode == -1:
                players = this.clients
                values = players.values()
                client = random.choice(values)
                this.currentSyncCode = client.playerCode
                this.currentSyncName = client.Username
        else:
            if this.currentSyncCode == -1:
                this.currentSyncCode = 0
                this.currentSyncName = ""

        return this.currentSyncCode

    def selectMap(this):
        if not this.forceNextMap == "-1":
            force = this.forceNextMap
            this.forceNextMap = "-1"
            this.mapCode = -1

            if force.isdigit():
                return this.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return this.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return this.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return this.selectMapSpecificic(force, "Xml")
            else:
                return 0

        elif this.specificMap:
            this.mapCode = -1
            return this.currentMap
        else:
            if this.isEditeur:
                return this.EMapCode

            elif this.isTribeHouse:
                tribeName = this.roomName[2:]
                runMap = this.server.getTribeHouse(tribeName)

                if runMap == 0:
                    this.mapCode = 0
                    this.mapName = "Tigrounette"
                    this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    this.mapYesVotes = 0
                    this.mapNoVotes = 0
                    this.mapPerma = 22
                    this.mapInverted = False
                else:
                    run = this.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        this.mapCode = 0
                        this.mapName = "Tigrounette"
                        this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        this.mapYesVotes = 0
                        this.mapNoVotes = 0
                        this.mapPerma = 22
                        this.mapInverted = False

            elif this.is801Room or this.isVillage:
                this.getMap801(801, "_Atelier 801")

            elif this.isVanilla:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map
                
            else:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                return this.selectMapStatus(this.mapStatus)
        return -1

    def selectMapStatus(this, mapStatus):
        customMaps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]                
        mapList = []

        if this.isVanilla:
            map = random.choice(this.MapList)
            while map == this.currentMap:
                map = random.choice(this.MapList)
            return map

        elif this.isMusic:
            if this.musicMapStatus == 5:
                this.Cursor.execute("select Code from MapEditor where Perma = 19 ORDER BY RAND() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])

        elif this.isRacing:
            this.Cursor.execute("select Code from MapEditor where Perma = 17 ORDER BY RAND() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.isBootcamp:
            P3List = []
            P13List = []

            this.Cursor.execute("select Code, Perma from MapEditor where Perma = 3 or Perma = 13 ORDER BY RAND() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                perma = rs[1]
                if perma == 3:
                    P3List.append(rs[0])
                else:
                    P13List.append(rs[0])

            if this.isBootcampP13:
                mapList = P3List if len(P13List) == 0 else P13List
            else:
                mapList = P13List if len(P3List) == 0 else P3List

        elif this.isSurvivor:
            this.isSurvivorVamp = this.survivorMapStatus == 10

            this.Cursor.execute("select Code from MapEditor where Perma = %s", [11 if this.isSurvivorVamp else 10])
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif this.isDefilante:
            this.Cursor.execute("select Code from MapEditor where Perma = 18 ORDER BY RAND() LIMIT 1")
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

        elif mapStatus in customMaps:
            multiple = False
            selectCode = 0

            if mapStatus == 1 or mapStatus == 9:
                multiple = True
            elif mapStatus == 2:
                selectCode = 5
            elif mapStatus == 3:
                selectCode = 9
            elif mapStatus == 5 or mapStatus == 11:
                selectCode = 6
            elif mapStatus == 6:
                selectCode = 7
            elif mapStatus == 7:
                selectCode = 8
            elif mapStatus == 10:
                selectCode = 4

            if multiple:
                this.Cursor.execute("select Code from MapEditor where Perma = 0 ORDER BY RAND() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])

                this.Cursor.execute("select Code from MapEditor where Perma = 1 ORDER BY RAND() LIMIT 1")
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
            else:
                this.Cursor.execute("select Code from MapEditor where Perma = %s ORDER BY RAND() LIMIT 1", [selectCode])
                r = this.Cursor.fetchall()
                for rs in r:
                    mapList.append(rs[0])
        else:
            map = random.choice(this.MapList)
            while map == this.currentMap:
                map = random.choice(this.MapList)
            return map

        if len(mapList) >= 1:
            runMap = random.choice(mapList)
        else:
            runMap = 0

        if len(mapList) >= 2:
            while runMap == this.currentMap:
                runMap = random.choice(mapList)

        if runMap == 0:
            map = random.choice(this.MapList)
            while map == this.currentMap:
                map = random.choice(this.MapList)
            return map
        else:
            mapInfo = this.getMapInfo(runMap)
            this.mapCode = runMap
            this.mapName = str(mapInfo[0])
            this.mapXML = str(mapInfo[1])
            this.mapYesVotes = int(mapInfo[2])
            this.mapNoVotes = int(mapInfo[3])
            this.mapPerma = int(mapInfo[4])
            this.mapInverted = random.randint(0, 100) > 85
            return -1
        
    def selectMapSpecificic(this, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            mapInfo = this.getMapInfo(int(code))
            if mapInfo[0] == None:
                return 0
            else:
                this.mapCode = int(code)
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapInverted = False
                return -1

        elif type == "Perm":
            mapList = []
            this.Cursor.execute("select Code from MapEditor where Perma = %s ORDER BY RAND() LIMIT 1", [int(str(code))])
            r = this.Cursor.fetchall()
            for rs in r:
                mapList.append(rs[0])

            if len(mapList) >= 1:
                runMap = random.choice(mapList)
            else:
                runMap = 0

            if len(mapList) >= 2:
                while runMap == this.currentMap:
                    runMap = random.choice(mapList)

            if runMap == 0:
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map
            else:
                mapInfo = this.getMapInfo(runMap)
                this.mapCode = runMap
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapInverted = False
                return -1

        elif type == "Xml":
            this.mapCode = 0
            this.mapName = "#Module"
            this.mapXML = str(code)
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 22
            this.mapInverted = False
            return -1

    def getMapInfo(this, mapCode):
        mapInfo = ["", "", 0, 0, 0]
        this.Cursor.execute("select Name, XML, YesVotes, NoVotes, Perma from MapEditor where Code = %s ORDER BY RAND() LIMIT 1", [mapCode])
        rs = this.Cursor.fetchone()
        if rs:
            mapInfo = rs[0], rs[1], rs[2], rs[3], rs[4]

        return mapInfo

    def checkIfTooFewRemaining(this):
        return len(filter(lambda player: not player.isDead, this.clients.values())) <= 2

    def getAliveCount(this):
        return len(filter(lambda player: not player.isDead, this.clients.values()))

    def getDeathCountNoShaman(this):
        return len(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, this.clients.values()))

    def getHighestScore(this):
        scores = []

        for client in this.clients.values():
            scores.append(client.playerScore)

        try:
            for client in this.clients.values():
                if client.playerScore == max(scores):
                    return client.playerCode
        except: pass
        return 0

    def getSecondHighestScore(this):
        scores = []

        for client in this.clients.values():
            scores.append(client.playerScore)

        scores.remove(max(scores))

        try:
            for client in this.clients.values():
                if client.playerScore == max(scores):
                    return client.playerCode
        except: pass
        return 0

    def getShamanCode(this):
        if this.currentShamanCode == -1:
            if this.currentMap in this.noShamanMaps or this.isNoShamanMap:
                pass
            elif this.noShaman or (this.survivorMapStatus == 7 and this.isSurvivor):
                pass
            else:
                if this.forceNextShaman > 0:
                    this.currentShamanCode = this.forceNextShaman
                    this.forceNextShaman = 0
                else:
                    this.currentShamanCode = this.getHighestScore()

            if this.currentShamanCode == -1:
                this.currentShamanName = ""
            else:
                for client in this.clients.values():
                    if client.playerCode == this.currentShamanCode:
                        this.currentShamanName = client.Username
                        this.currentShamanType = client.shamanType
                        this.currentShamanSkills = client.playerSkills
                        break
        return this.currentShamanCode

    def getDoubleShamanCode(this):
        if this.currentShamanCode == -1 and this.currentSecondShamanCode == -1:
            if this.forceNextShaman > 0:
                this.currentShamanCode = this.forceNextShaman
                this.forceNextShaman = 0
            else:
                this.currentShamanCode = this.getHighestScore()

            if this.currentSecondShamanCode == -1:
                this.currentSecondShamanCode = this.getSecondHighestScore()

            if this.currentSecondShamanCode == this.currentShamanCode:
                values = this.clients.values()
                tempClient = random.choice(values)
                this.currentSecondShamanCode = tempClient.playerCode

            for client in this.clients.values():
                if client.playerCode == this.currentShamanCode:
                    this.currentShamanName = client.Username
                    this.currentShamanType = client.shamanType
                    this.currentShamanSkills = client.playerSkills
                    break

                if client.playerCode == this.currentSecondShamanCode:
                    this.currentSecondShamanName = client.Username
                    this.currentSecondShamanType = client.shamanType
                    this.currentSecondShamanSkills = client.playerSkills
                    break

        return [this.currentShamanCode, this.currentSecondShamanCode]

    def closeVoting(this):
        this.initVotingMode = False
        this.isVotingBox = False
        if this.voteCloseTimer != None: this.voteCloseTimer.cancel()
        this.mapChange()

    def killAllNoDie(this):
        for client in this.clients.values():
            if not client.isDead:
                client.isDead = True
        this.checkShouldChangeMap()

    def killAll(this):
        for client in this.clients.values():
            if not client.isDead:
                client.sendPlayerDied()
                client.isDead = True
        this.checkShouldChangeMap()

    def killShaman(this):
        for client in this.clients.values():
            if client.playerCode == this.currentShamanCode:
                client.isDead = True
                client.sendPlayerDied()
        this.checkShouldChangeMap()

    def killAfk(this):
        if not this.isEditeur or not this.isTotemEditeur or not this.isBootcamp or not this.isTribeHouseMap or not this.disableAfkKill:
            if ((TFMUtils.getTime() - this.gameStartTime) < 32 and (TFMUtils.getTime() - this.gameStartTime) > 28):
                for client in this.clients.values():
                    if not client.isDead and client.isAfk:
                        client.isDead = True
                        if not this.noAutoScore: client.playerScore += 1
                        client.sendPlayerDied()
                this.checkShouldChangeMap()

    def checkIfDoubleShamansAreDead(this):
        client1 = this.clients.get(this.currentShamanName)
        client2 = this.clients.get(this.currentSecondShamanName)
        return (False if client1 == None else client1.isDead) and (False if client2 == None else client2.isDead)

    def checkIfShamanIsDead(this):
        client = this.clients.get(this.currentShamanName)
        return False if client == None else client.isDead

    def checkIfShamanCanGoIn(this):
        for client in this.clients.values():
            if client.playerCode != this.currentShamanCode and client.playerCode != this.currentSecondShamanCode and not client.isDead:
                return False
        return True

    def giveShamanSave(this, shamanName, type):
        if not this.countStats:
            return

        client = this.clients.get(shamanName)
        if client != None:
            if type == 0:
                client.shamanSaves += 1
            elif type == 1:
                client.hardModeSaves += 1
            elif type == 2:
                client.divineModeSaves += 1
            if client.privLevel != 0:
                counts = [client.shamanSaves, client.hardModeSaves, client.divineModeSaves]
                titles = [this.server.shamanTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if titles[type].has_key(counts[type]):
                    title = titles[type][counts[type]]
                    client.checkAndRebuildTitleList(rebuilds[type])
                    client.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    client.sendCompleteTitleList()
                    client.sendTitleList()
                    
    def respawnMice(this):
        for client in this.clients.values():
            if client.isDead:
                client.isDead = False
                client.playerStartTimeMillis = time.time()
                this.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(client.getPlayerData()).writeBool(False).writeBool(True).toByteArray())

        if this.autoRespawn or this.isTribeHouseMap:
            this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)

    def respawnSpecific(this, playerName, isResetPlay=False):
        client = this.clients.get(playerName)
        if client != None and client.isDead:
            client.resetPlay(isResetPlay)
            client.isAfk = False
            client.playerStartTimeMillis = time.time()
            this.sendAll(Identifiers.send.Player_Respawn, ByteArray().writeBytes(client.getPlayerData()).writeBool(False).writeBool(True).toByteArray())

    def sendMulodromeRound(this):
        this.sendAll(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(this.mulodromeRoundCount).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
        if this.mulodromeRoundCount > 10:
            this.sendAll(Identifiers.send.Mulodrome_End, "")
            this.sendAll(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if this.blueCount == this.redCount else (1 if this.blueCount < this.redCount else 0)).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
            this.isMulodrome = False
            this.mulodromeRoundCount = 0
            this.redCount = 0
            this.blueCount = 0
            this.redTeam = []
            this.blueTeam = []
            this.isRacing = False
            this.mapStatus = 1
            this.never20secTimer = False
            this.noShaman = False

    def checkVanillaXML(this):
        try:
            with open("./include/vanilla/"+str(this.currentMap)+".xml", "r") as f:
                XML = f.read()
                f.close()

                this.mapCode = int(this.currentMap)
                this.mapName = "Transformice"
                this.mapXML = str(XML)
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = 2
                this.currentMap = -1
                this.mapInverted = False
        except: pass

    def getMap801(this, code, name):
        try:
            with open("./include/vanilla/801.xml", "r") as f:
                XML = f.read()
                f.close()

                this.mapCode = code
                this.mapName = name
                this.mapXML = str(XML)
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = 41
                this.currentMap = -1
                this.mapInverted = False
        except: pass

    def sendVampireMode(this):
        client = this.clients.get(this.currentSyncName)
        if client != None:
            client.sendVampireMode(False)

    def bindKeyBoard(this, playerName, key, down, yes):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBool(down).writeBool(yes).toByteArray())

    def addPhysicObject(this, id, x, y, bodyDef):
        this.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBool(bool(bodyDef["dynamic"]) if bodyDef.has_key("dynamic") else False).writeByte(int(bodyDef["type"]) if bodyDef.has_key("type") else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if bodyDef.has_key("width") else 0).writeShort(int(bodyDef["height"]) if bodyDef.has_key("height") else 0).writeBool(bool(bodyDef["foreground"]) if bodyDef.has_key("foreground") else False).writeShort(int(bodyDef["friction"]) if bodyDef.has_key("friction") else 0).writeShort(int(bodyDef["restitution"]) if bodyDef.has_key("restitution") else 0).writeShort(int(bodyDef["angle"]) if bodyDef.has_key("angle") else 0).writeBool(bodyDef.has_key("color")).writeInt(int(bodyDef["color"]) if bodyDef.has_key("color") else 0).writeBool(bool(bodyDef["miceCollision"]) if bodyDef.has_key("miceCollision") else True).writeBool(bool(bodyDef["groundCollision"]) if bodyDef.has_key("groundCollision") else True).writeBool(bool(bodyDef["fixedRotation"]) if bodyDef.has_key("fixedRotation") else False).writeShort(int(bodyDef["mass"]) if bodyDef.has_key("mass") else 0).writeShort(int(bodyDef["linearDamping"]) if bodyDef.has_key("linearDamping") else 0).writeShort(int(bodyDef["angularDamping"]) if bodyDef.has_key("angularDamping") else 0).writeBool(False).writeUTF("").toByteArray())

    def chatMessage(this, message, playerName):
        p = ByteArray().writeUTF(message)
        if playerName == "":
            this.sendAll(Identifiers.send.Message, p.toByteArray())
        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.Message, p.toByteArray())

    def removeObject(this, objectId):
        this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBool(True).toByteArray())

    def movePlayer(this, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBool(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBool(sOffSet).toByteArray())

    def setNameColor(this, playerName, color):
        if this.clients.has_key(playerName):
            this.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(this.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def bindMouse(this, playerName, yes):
        client = this.clients.get(playerName)
        if client != None:
            client.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBool(yes).toByteArray())

    def addPopup(this, id, type, text, targetPlayer, x, y, width, fixedPos):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBool(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())

    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBool(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(this, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def showColorPicker(this, id, targetPlayer, defaultColor, title):
        p = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Show_Color_Picker, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Show_Color_Picker, p.toByteArray())

    def startSnowSchedule(this, power):
        if this.isSnowing:
            this.startSnow(0, power, False)

    def startSnow(this, millis, power, enabled):
        this.isSnowing = enabled
        this.sendAll(Identifiers.send.Snow, ByteArray().writeBool(enabled).writeShort(power).toByteArray())
        if enabled:
            this.endSnowTimer = reactor.callLater(millis, lambda: this.startSnowSchedule(power))

    def giveSurvivorStats(this):
        for client in this.clients.values():
            if not client.isNewPlayer:
                client.survivorStats[0] += 1
                if client.isShaman:
                    client.survivorStats[1] += 1
                    client.survivorStats[2] += this.getDeathCountNoShaman()
                elif not client.isDead:
                    client.survivorStats[3] += 1

                if client.survivorStats[0] >= 1000 and not str(120) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(120))
                    client.shopBadges.append(str(120))
                    client.shopModule.checkAndRebuildBadges()

                if client.survivorStats[1] >= 800 and not str(121) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(121))
                    client.shopBadges.append(str(121))
                    client.shopModule.checkAndRebuildBadges()

                if client.survivorStats[2] >= 20000 and not str(122) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(122))
                    client.shopBadges.append(str(122))
                    client.shopModule.checkAndRebuildBadges()

                if client.survivorStats[3] >= 10000 and not str(123) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(123))
                    client.shopBadges.append(str(123))
                    client.shopModule.checkAndRebuildBadges()

    def giveRacingStats(this):
        for client in this.clients.values():
            if not client.isNewPlayer:
                client.racingStats[0] += 1
                if client.hasCheese or client.hasEnter:
                    client.racingStats[1] += 1

                if client.hasEnter:
                    if client.currentPlace <= 3:
                        client.racingStats[2] += 1

                    if client.currentPlace == 1:
                        client.racingStats[3] += 1

                if client.racingStats[0] >= 1500 and not str(124) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(124))
                    client.shopBadges.append(str(124))
                    client.shopModule.checkAndRebuildBadges()

                if client.racingStats[1] >= 10000 and not str(125) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(125))
                    client.shopBadges.append(str(125))
                    client.shopModule.checkAndRebuildBadges()

                if client.racingStats[2] >= 10000 and not str(127) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(127))
                    client.shopBadges.append(str(127))
                    client.shopModule.checkAndRebuildBadges()

                if client.racingStats[3] >= 10000 and not str(126) in client.shopBadges:
                    client.shopModule.sendUnlockedBadge(str(126))
                    client.shopBadges.append(str(126))
                    client.shopModule.checkAndRebuildBadges()

    def send20SecRemainingTimer(this):
        if not this.changed20secTimer:
            if not this.never20secTimer and this.roundTime + (this.gameStartTime - TFMUtils.getTime()) > 21:
                this.changed20secTimer = True
                this.changeMapTimers(20)
                for client in this.clients.values():
                    client.sendRoundTime(20)

    def changeMapTimers(this, seconds):
        if this.changeMapTimer != None: this.changeMapTimer.cancel()
        this.changeMapTimer = reactor.callLater(seconds, this.mapChange)

    def newConsumableTimer(this, code):
        this.roomTimers.append(reactor.callLater(10, lambda: this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBool(False).toByteArray())))

if __name__ == "__main__":
    Config = ConfigParser.ConfigParser()
    Config.read("./include/Config.ini")

    os.system("title Transformice Emulador")
    #os.system("color F3")
    TFM = Server()
    iniports = []
    for port in [12801, 14801, 13801, 11801]:
        try:
            reactor.listenTCP(port, TFM)
            iniports.append(port)
        except:
            pass

    if not iniports == []:
        print("\n")
        print(str(iniports)).center(80)
    threading.Thread(target=reactor.run(), args=(False,)).start()
