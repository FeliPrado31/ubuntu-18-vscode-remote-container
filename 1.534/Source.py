#coding: utf-8
import re, os, sys, json, time, random, MySQLdb, ftplib, urllib2, socket, sqlite3, threading, traceback, binascii, ConfigParser, time as _time

# Others
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

# Imports Components
from utils import *
from game import *
from time import gmtime, strftime

# Library
from datetime import datetime, date
from twisted.internet import reactor, protocol
from datetime import timedelta
import urllib2
from urllib import urlopen

class Client:
    def __init__(this):

        # String
        this.langue = ""
        this.packages = ""
        this.realLangue = json.load(urllib2.urlopen("http://ipinfo.io/json"))["country"].lower()
        this.nickColor = "#95d9d6"
        this.mouseName = ""
        this.roomName = ""
        this.emailAddress = ""
        this.marriage = ""
        this.shopItems = ""
        this.tribeName = ""
        this.nameColor = ""
        this.chatColor = ""
        this.tradeName = ""
        this.playerName = ""
        this.shamanItems = ""
        this.lastMessage = ""
        this.tribeMessage = ""
        this.tempMouseColor = "" 
        this.silenceMessage = ""
        this.currentCaptcha = ""
        this.mouseColor = "78583a"
        this.shamanColor = "95d9d6"
        this.modoPwetLangue = "ALL"
        this.playerLook = "1;0,0,0,0,0,0,0,0,0,0,0"
        this.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        this.fur = ""
        this.botVillage = ""
        this.lastNpc = ""
        
        # Integer
        this.lastReportID = 0
        this.playerKarma = 0
        this.mascota = 0
        this.pingTime = 0
        this.flypoints = 0
        this.pet = 0
        this.activeArtefact = 0
        this.posX = 0
        this.ClientGotHole = 1
        this.posY = 0
        this.velX = 0
        this.velY = 0
        this.gender = 0
        this.playerTime = 0
        this.loginTime = 0
        this.petEnd = 0
        this.viewMessage = 0
        this.priceDoneVisu = 0
        this.lastOn = 0
        this.regDate = 0
        this.langueID = 0
        this.useAnime = 0
        this.playerID = 0
        this.banHours = 0
        this.iceCount = 2
        this.privLevel = 0
        this.nowTokens = 0
        this.nowCoins = 0
        this.shamanExp = 0
        this.tribeCode = 0
        this.tribeRank = 0
        this.tribeChat = 0
        this.titleStars = 0
        this.firstCount = 0
        this.playerCode = 0
        this.shamanType = 0
        this.tribeHouse = 0
        this.tribeJoined = 0
        this.silenceType = 0
        this.playerScore = 0
        this.titleNumber = 0
        this.cheeseCount = 0
        this.shopFraises = 0
        this.shamanSaves = 0
        this.shamanLevel = 1
        this.lastGameMode = 0
        this.bubblesCount = 0
        this.currentPlace = 0
        this.shamanCheeses = 0
        this.hardModeSaves = 0
        this.bootcampCount = 0
        this.shopCheeses = 100
        this.shamanExpNext = 32
        this.ambulanceCount = 0
        this.defilantePoints = 0
        this.divineModeSaves = 0
        this.lastDivorceTimer = 0
        this.TimeGiro = 0
        this.equipedShamanBadge = 0
        this.playerStartTimeMillis = 0
        this.racingRounds = 0
        this.fastracingRounds = 0
        this.bootcampRounds = 0
        this.survivorDeath = 0
        this.countTime = 1
        this.countP = 0
        this.cannonX = 2
        this.cannonY = 8
        this.cXpos = 189
        this.cYpos = 133
        this.cnCustom = 0
        this.page = 1
        this.lastPacketID = random.randint(0, 99)
        this.authKey = random.randint(0, 2147483647)
        this.TFMUtils = Utils
        this.tribulleID = 0
        this.artefactID = 0
        this.drawingColor = 0

        # Bool
        this.isLuaAdmin = False
        this.isReloadCafe = False
        this.isAfk = False
        this.isDead = False
        this.isMute = False
        this.isCafe = False
        this.isGuest = False
        this.isVoted = False
        this.isTrade = False
        this.useTotem = False
        this.openStaffChat = False
        this.isHidden = False
        this.isClosed = False
        this.isShaman = False
        this.hasEnter = False
        this.isSkill = False
        this.isSuspect = False
        this.isVampire = False
        this.isLuaAdmin = False
        this.hasCheese = False
        this.hasBolo = False
        this.hasBolo2 = False
        this.selfGet = False
        this.isJumping = False
        this.resetTotem = False
        this.isModoPwet = False
        this.isModoPwetNotifications = False
        this.canRespawn = False
        this.enabledLua = False
        this.isNewPlayer = False
        this.isEnterRoom = False
        this.tradeConfirm = False
        this.canUseConsumable = True
        this.canSkipMusic = False
        this.isReloadCafe = False
        this.isMovingLeft = False
        this.isMovingRight = False
        this.isOpportunist = False
        this.qualifiedVoted = False
        this.desintegration = False
        this.canShamanRespawn = False
        this.validatingVersion = False
        this.canRedistributeSkills = False
        this.libCn = False
        this.canCN = False
        this.isFly = False
        this.isFlyMod = False
        this.isSpeed = False
        this.isFFA = False
        this.canSpawnCN = True
        this.isTeleport = False
        this.isExplosion = False
        this.chatdisabled = False
        this.canKiss = True
        this.openingFriendList = False
        this.isTribeOpen = False
        this.hasArtefact = False

        this.showButtons = True

        #Degiskenler
        this.isBlockAttack = True

        # Others
        this.Cursor = Cursor
        this.CMDTime = time.time()
        this.CAPTime = time.time()
        this.CTBTime = time.time()

        # Nonetype
        this.room = None
        this.awakeTimer = None
        this.skipMusicTimer = None
        this.resSkillsTimer = None

        # List
        this.totem = [0, ""]
        this.PInfo = [0, 0, 400]
        this.tempTotem = [0, ""]
        this.racingStats = [0] * 4
        this.survivorStats = [0] * 4

        this.chats = []
        #this.roles = [] 
        this.invitedTribeHouses = []
        this.voteBan = []
        this.clothes = []
        this.titleList = []
        this.friendsList = []
        this.tribeInvite = []
        this.shamanBadges = []
        this.ignoredsList = []
        this.mulodromePos = []
        this.shopTitleList = []
        this.marriageInvite = []
        this.firstTitleList = []
        this.cheeseTitleList = []
        this.shamanTitleList = []
        this.specialTitleList = []
        this.bootcampTitleList = []
        this.hardModeTitleList = []
        this.equipedConsumables = []
        this.ignoredTribeInvites = []
        this.divineModeTitleList = []
        this.ignoredMarriageInvites = []
        this.custom = []
        this.dailyQuest = [0, 0, 0, 0]
        this.deathStats = []
        this.visuDone = []

        # Dict
        this.ipInfo = eval(urllib2.urlopen("https://extreme-ip-lookup.com/json/").read())
        this.shopBadges = {}
       # this.role_list = {0:"locked", 1:"user", 2:"sentinel", 5:"funcorp", 6:"mapcrew", 7:"arbitre", 8:"moderator", 9:"co admin", 10:"community manager", 11:"admin"}
        this.tribeRanks = ""
        this.playerSkills = {}
        this.tradeConsumables = {}
        this.playerConsumables = {}
        this.itensBots = {"Papaille": [(4, 800, 50, 4, 2253, 50), (4, 800, 50, 4, 2254, 50), (4, 800, 50, 4, 2257, 50), (4, 800, 50, 4, 2260, 50), (4, 800, 50, 4, 2261, 50)], "Santa Claus": [(1, 34, 1, 4, 2254, 100), (1, 174, 1, 4, 2254, 100), (4, 6, 50, 4, 2253, 50), (3, 312, 1, 4, 2253, 50)], "Easter Chappie": [(1, 65, 1, 4, 2254, 100), (1, 64, 1, 4, 2254, 100), (1, 170, 1, 4, 2254, 100), (4, 6, 50, 4, 2254, 100), (3, 426, 1, 4, 2254, 100)], "Buffy": [(1, 147, 1, 4, 2254, 200), (2, 17, 1, 4, 2254, 150), (2, 18, 1, 4, 2254, 150), (2, 19, 1, 4, 2254, 150), (3, 398, 1, 4, 2254, 150), (3, 392, 1, 4, 2254, 50)], "Indiana Mouse": [(3, 255, 1, 4, 2257, 50), (3, 394, 1, 4, 2257, 50), (3, 395, 1, 4, 2257, 50), (3, 320, 1, 4, 2257, 50), (3, 393, 1, 4, 2257, 50), (3, 402, 1, 4, 2257, 50), (3, 397, 1, 4, 2257, 50), (3, 341, 1, 4, 2257, 50), (3, 335, 1, 4, 2257, 25), (3, 403, 1, 4, 2257, 50), (1, 6, 1, 4, 2257, 50), (1, 17, 1, 4, 2257, 50)], "Elise": [(4, 31, 2, 4, 2261, 5), (4, 2256, 2, 4, 2261, 5), (4, 2232, 2, 4, 2253, 1), (4, 21, 5, 4, 2253, 1), (4, 33, 2, 4, 2260, 1), (4, 33, 2, 4, 2254, 1)], "Oracle": [(1, 145, 1, 4, 2253, 200), (2, 16, 1, 4, 2253, 150), (2, 21, 1, 4, 2253, 150), (2, 24, 1, 4, 2253, 150), (2, 20, 1, 4, 2253, 150), (3, 390, 1, 4, 2253, 50), (3, 391, 1, 4, 2253, 200), (3, 399, 1, 4, 2253, 150)], "Prof": [(4, 800, 20, 4, 2257, 10), (4, 19, 2, 4, 2257, 5), (4, 2258, 2, 4, 2257, 4), (4, 2262, 5, 4, 2257, 2), (4, 2259, 10, 4, 2257, 1), (4, 20, 1, 4, 2257, 2)], "Cassidy": [(1, 154, 1, 4, 2261, 200), (2, 23, 1, 4, 2261, 150), (3, 400, 1, 4, 2261, 100)], "Von Drekkemouse": [(2, 22, 1, 4, 2260, 150), (1, 153, 1, 4, 2260, 200), (3, 401, 1, 4, 2260, 100)], "Tod": [(4, 2259, 10, 4, 2257, 1), (4, 2258, 10, 4, 2254, 230), (3, 401, 1, 4, 2260, 100)], "Fishing2017": [(1, 184, 1, 4, 2257, 200), (2, 24, 1, 4, 2257, 150), (2, 29, 1, 4, 2257, 150), (3, 422, 1, 4, 2257, 200)]}
        this.aventureCounts = {}
        this.aventurePoints = {}
        this.visusRemove = []


    def dataReceived(this, packet):
        if packet.startswith("<policy-file-request/>"):
            this.transport.write("<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\"/></cross-domain-policy>")
            this.transport.loseConnection()
        else:
            this.packages += packet
            while this.packages.strip(chr(0)):
                if len(this.packages) >= 5:
                    sizeBytes, package, length = 0, "", 0
                    p = ByteArray(this.packages)
                    sizeBytes = p.readByte()
                    if sizeBytes == 1:
                        length = p.readUnsignedByte()
                    elif sizeBytes == 2:
                        length = p.readUnsignedShort()
                    elif sizeBytes == 3:
                        length = ((p.readUnsignedByte() & 0xFF) << 16) | ((p.readUnsignedByte() & 0xFF) << 8) | (p.readUnsignedByte() & 0xFF) 
                    else:
                        this.packages = ""
                    if (length >= 1 and p.getLength() >= 3):
                        length += 1
                        if length == p.getLength():
                            package = p.toByteArray()
                            this.packages = ""
                        elif length > p.getLength():
                            break
                        else:
                            package = p.toByteArray()[:length]
                            this.packages = p.toByteArray()[length:]
                    else:
                        this.packages = ""
                    if package:
                        if len(package) >= 3:
                            this.parseString(ByteArray(package))
                    p
                else:
                    this.packages = ""

    def getText(this, object, *params):
        keys = object.split(".")
        json = this.server.menu["texts"][this.langue]
        i = 0
        while i < len(keys):
            key = keys[i]
            if i == len(keys) - 1:
                text = json[key]
                count = 0
                while count < len(params):
                    text = text.replace("%" + str(count + 1), str(params[count]))
                    count += 1
                return text
            else: json = json[key]
            i += 1
        return ""
        
    def close(this):
        i = 10002
        while i <= 10500:
            this.room.removeTextArea(i, this.playerName)
            i += 1

    def sendAddPopupText(this, id, x, y, l, a, fur1, fur2, opcit, Message):
        bg = int(fur1, 16)
        bd = int(fur2, 16)
        data = struct.pack("!i", id)
        data = data + struct.pack("!h", len(Message))
        data = data + Message + struct.pack("!hhhhiibb", int(x), int(y), int(l), int(a), int(bg), int(bd), int(opcit), 0)
        this.sendPacket([29, 20], data)
    
    def makeConnection(this, transport):
        this.transport = transport
        this.server = this.factory
        this.ipAddress = this.transport.getPeer().host
        this.modoPwet = ModoPwet(this, this.server)
        this.cafe = Cafe(this, this.server)
        this.tribulle = Tribulle(this, this.server)
        this.Shop = Shop(this, this.server)
        this.Skills = Skills(this, this.server)
        this.Packets = Packets(this, this.server)
        this.Commands = Commands(this, this.server)
        this.feli = Feli(this, this.server)
        this.fullMenu = fullMenu(this, this.server)
        this.DailyQuest = DailyQuest(this, this.server)
        this.Utility = Utility(this, this.server)
        this.AntiCheat = AntiCheat(this, this.server)
        this.parseTitles = parseTitles(this, this.server)
        if this.server.connectedCounts.has_key(this.ipAddress):
            this.server.connectedCounts[this.ipAddress] += 1
        else:
            this.server.connectedCounts[this.ipAddress] = 1
        if this.server.connectedCounts[this.ipAddress] >= 9999999999999999999999999 or this.ipAddress in this.server.IPPermaBanCache or this.ipAddress in this.server.IPTempBanCache:
            this.transport.setTcpKeepAlive(0)
            this.transport.setTcpNoDelay(True)
            this.transport.loseConnection()
            this.server.IPTempBanCache.append(this.ipAddress)

    def checkReport(this, array, playerName):
        return playerName in array

    def connectionLost(this, args):
        this.isClosed = True
        if this.server.connectedCounts.has_key(this.ipAddress):
            count = this.server.connectedCounts[this.ipAddress] - 1
            if count <= 0:
                del this.server.connectedCounts[this.ipAddress]
            else:
                this.server.connectedCounts[this.ipAddress] = count

        if this.server.players.has_key(this.playerName):
            del this.server.players[this.playerName]
                
            if this.isTrade:
                this.cancelTrade(this.tradeName)

            if this.server.reports.has_key(this.playerName):
                if not this.server.reports[this.playerName]["durum"] == "banned":
                    this.server.reports[this.playerName]["durum"] = "disconnected"
                    this.modoPwet.updateModoPwet()

            if this.server.chatMessages.has_key(this.playerName):
                this.server.chatMessages[this.playerName] = {}
                del this.server.chatMessages[this.playerName]

            for player in this.server.players.values():
                if this.playerName and player.playerName in this.friendsList and player.friendsList:
                    player.tribulle.sendFriendDisconnected(this.playerName)

            if this.tribeCode != 0:
                this.tribulle.sendTribeMemberDisconnected()

            if not this.playerName == "":
                if not this.isGuest:
                    this.updateDatabase()

            if this.privLevel in [5, 6, 7, 8]:
                    privbyte = {5:9, 6:7, 7:3, 8:3}[this.privLevel] # 2: arbitre, 3: modo, 7: mapcrew, 8: luateam, 9: funcorp, 10: fashionsquad
                    ulkebyte = this.langue.lower().swapcase()
                    userbyte = this.playerName + " se ha desconectado."
                    this.sendStaffCM(privbyte, ulkebyte, userbyte)

            if this.privLevel in [9, 10, 11]:
                    privbyte = this.langue.lower().swapcase()
                    userbyte = this.playerName + " se ha desconectado."
                    this.sendStaffCM(2, privbyte, userbyte)
                    this.sendStaffCM(3, privbyte, userbyte)
                    this.sendStaffCM(7, privbyte, userbyte)
                    this.sendStaffCM(9, privbyte, userbyte)
                    
            if this.privLevel >= 1:
                this.server.sendStaffMessage(9, "<CH>"+this.playerName+" <J>se ha desconectado</J>")

            reactor.callFromThread(this.updateDatabase)            

        if this.room != None:
            this.room.removeClient(this)

    def sendPacket(this, identifiers, packet=""):
        if this.isClosed:
            return

        p = ByteArray().writeBytes(("".join(map(chr, identifiers)) + chr(packet)) if type(packet) == int else "".join(map(chr, identifiers)) + packet) if type(packet) != list else ByteArray().writeBytes(chr(1) + chr(1)).writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + packet)))
        this.transport.write((ByteArray().writeByte(1).writeUnsignedByte(p.getLength()) if p.getLength() <= 0xFF else ByteArray().writeByte(2).writeUnsignedShort(p.getLength()) if p.getLength() <= 0xFFFF else ByteArray().writeByte(3).writeUnsignedByte((p.getLength() >> 16) & 0xFF).writeUnsignedByte((p.getLength() >> 8) & 0xFF).writeUnsignedByte(p.getLength() & 0xFF) if p.getLength() <= 0xFFFFFF else 0).writeBytes(p.toByteArray()).toByteArray())
        this.transport.setTcpKeepAlive(1)
        this.transport.setTcpNoDelay(True)

    def parseString(this, packet):
        if this.isClosed:
            return

        if packet in ["", " ", "\x00", "\x01"]:
            this.server.IPTempBanCache.append(this.ipAddress)
            this.transport.loseConnection()
            this.breakLoop()
             
        packetID, C, CC = packet.readByte(), packet.readByte(), packet.readByte()        
        if not this.validatingVersion:
            if (C == Identifiers.recv.Informations.C and CC == Identifiers.recv.Informations.Correct_Version) and not (this.isClosed):
                version = packet.readShort()
                ckey = packet.readUTF()

                if not ckey == this.server.CKEY and version != this.server.Version:
                    print "[%s] [WARN] Invalid version or CKey (%s, %s)" %(time.strftime("%H:%M:%S"), version, ckey)
                    this.transport.loseConnection()
                else:
                    this.validatingVersion = True
                    this.sendCorrectVersion()

                    
            else:
                this.transport.loseConnection()
        else:
            try:
                this.lastPacketID = (this.lastPacketID + 1) % 100
                this.lastPacketID = packetID
                this.Packets.parsePacket(packetID, C, CC, packet)
            except:
                with open("./logs/Bugs.log", "a") as f:
                    traceback.print_exc(file=f)
                    f.write("\n")

    def sendPing(this):
        this.pingTime = int(round(time.time() * 1000))
        this.sendPacket([28, 6], ByteArray().writeByte(0).toByteArray())


    def sendDeathBoard(this):
        position = 1
        shown = "<V><p align='center'><FC>DeathCount Leaderboard</font></p>\n"
        shown += "<p align='center'><font size='12'>"
        this.Cursor.execute("select Username, deathCount from users where PrivLevel < 200 ORDER By deathCount DESC LIMIT 100")
        for rrf in this.Cursor.fetchall():
            playerName = str(rrf[0])
            deathCount = rrf[1]
            shown += "<font color='#E96D84'>"+str(position)+"</font> <font color='#3C5064'>-</font> <font color='#B7E96D'>"+str(playerName)+"</font> <font color='#3C5064'>-</font> <font color='#6DB5E9'>"+str(deathCount)+"</font>"
            shown += "<br />"
            position += 1

        this.sendLogMessage(shown + "</font></p>")

    def blockAttack(this):
        reactor.callLater(1.5, this.sendBlockAttack)
        
    def sendBlockAttack(this):
        this.isBlockAttack = True

    def loginPlayer(this, playerName, password, startRoom):
        #if not "#" in playerName and not "@" in playerName:
           # playerName += "#0000"
        playerName = "Souris" if playerName == "" else playerName
        if password == "":
            playerName = this.server.checkAlreadyExistingGuest("*" + (playerName[0].isdigit() or str(playerName) > 12 or str(playerName) < 3 or "Souris" if "+" in playerName else playerName))
            startRoom = "\x03[Tutorial] %s" %(playerName)
            this.isGuest = False
            
##        playerName = "" if playerName == "" else playerName
##        if password == "":
##            playerName = this.server.checkConnectedAccount("#" + (playerName[0].isdigit() or len(playerName) > 12 or len(playerName) < 3 or "0000" if "+" in playerName else playerName))

        if not this.isGuest and playerName in this.server.userPermaBanCache:
            this.sendPacket(Identifiers.old.send.Player_Ban_Login, [this.server.getPermBanInfo(playerName)])
            this.transport.loseConnection()
            return

        if not this.isGuest:
            banInfo = this.server.getTempBanInfo(playerName)
            timeCalc = Utils.getHoursDiff(banInfo[1])
            if timeCalc <= 0:
                this.server.removeTempBan(playerName)
            else:
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc, banInfo[0]])
                this.transport.loseConnection()
                return

        if this.server.checkConnectedAccount(playerName):
            this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(1).writeUTF("").writeUTF("").toByteArray())
        else:
            letters, selfs, messages = "", "", ""
            if not this.isGuest and not playerName == "":
                Cursor.execute("select * from Users where Email = %s and Password = %s", [playerName, password])
                players = []
                for rs in Cursor.fetchall():
                    players.append(rs[0])
                if len(players) > 1:
                    i = 0
                    p = ByteArray()
                    while i != len(players):
                        p.writeBytes(players[i]).writeShort(-15708)
                        i += 1
                    this.sendPacket([26, 12], ByteArray().writeByte(11).writeShort(len(p.toByteArray())).writeBytes(p.toByteArray()).writeShort(0).toByteArray())
                else:
                    this.Cursor.execute("select * from Users where "+("Email" if "@" in playerName else "Username")+" = %s and Password = %s", [playerName, password])
                    rs = this.Cursor.fetchone()
                    if rs:
                        playerName = rs[0]
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
                        this.clothes = map(str, filter(None, rs[17].split("|")))
                        this.playerLook = rs[18]
                        this.shamanLook = rs[19]
                        this.mouseColor = rs[20]
                        this.shamanColor = rs[21]
                        this.regDate = rs[22]
                        this.estado = rs[91]
                        this.mascota = 0
                        this.chatColor = rs[92]
                        this.firstMes = rs[81]
                        this.shopBadges = eval(rs[23])
                        this.firstTitleList = map(float, filter(None, rs[25].split(",")))
                        this.shamanTitleList = map(float, filter(None, rs[26].split(",")))
                        this.shopTitleList = map(float, filter(None, rs[27].split(",")))
                        this.bootcampTitleList = map(float, filter(None, rs[28].split(",")))
                        this.hardModeTitleList = map(float, filter(None, rs[29].split(",")))
                        this.divineModeTitleList = map(float, filter(None, rs[30].split(",")))
                        this.specialTitleList = map(float, filter(None, rs[31].split(",")))
                        this.banHours = rs[32]
                        this.shamanLevel = rs[33]
                        this.shamanExp = rs[34]
                        this.shamanExpNext = rs[35]

                        for skill in map(str, filter(None, rs[36].split(";"))):
                            values = skill.split(":")
                            this.playerSkills[int(values[0])] = int(values[1])

                        this.lastOn = rs[37]
                        this.friendsList = rs[38].split(",")
                        this.ignoredsList = rs[39].split(",")
                        this.gender = rs[40]
                        this.lastDivorceTimer = rs[41]
                        this.marriage = rs[42]
                        this.tribeCode = rs[43]
                        this.tribeRank = rs[44]
                        this.tribeJoined = rs[45]
                        selfs = rs[46]
                        message = rs[47]
                        this.visuDone = rs[59].split("|")
                        this.custom = map(str, filter(None, rs[60].split(",")))
                        this.survivorStats = map(int, rs[48].split(","))
                        this.racingStats = map(int, rs[49].split(","))
                        
                        for consumable in map(str, filter(None, rs[50].split(";"))):
                            values = consumable.split(":")
                            this.playerConsumables[int(values[0])] = int(values[1])

                        this.equipedConsumables = []
                        this.pet = rs[52]
                        this.petEnd = 0 if this.pet == 0 else Utils.getTime() + rs[53]
                        this.shamanBadges = map(int, filter(None, rs[54].split(",")))
                        this.equipedShamanBadge = rs[55]
                        this.totem = [rs[57], rs[58].replace("%"[0], chr(1))]
                        this.nowCoins = rs[61]
                        this.nowTokens = rs[62]
                        this.deathStats = map(int, rs[63].split(","))
                        vipTime = rs[64]
                        this.langueStaff = rs[65]
                        this.votemayor, this.candidatar, this.isMayor, this.isPresidente, this.votepresidente, this.addpresidente=map(int, rs[66].split("#"))
                        for counts in map(str, filter(None, rs[69].split(";"))):
                            values = counts.split(":")
                            f = []
                            aux = 0
                            for i in xrange(len(values[1])):
                                try:
                                    aux = aux * 10 + int(values[1][i])
                                except:
                                    if aux > 0:
                                        f.append(aux)
                                    aux = 0
                                    pass
                            this.aventureCounts[int(values[0])] = int(f[0]), int(f[1])
                        #this.aventureCounts = eval(rs["AventureCounts"])
                        for points in map(str, filter(None, rs[70].split(";"))):
                            values = points.split(":")
                            this.aventurePoints[int(values[0])] = int(values[1])
                        this.aventureSaves = rs[71]
                        this.emailAddress = rs[82]
                        #this.recList = eval(rs[83])
                        this.dailyQuest = map(str, filter(None, rs[83].split(","))) if rs[83] != "" else [0, 0, 0, 1]
                        this.remainingMissions = rs[84]
                        letters = rs[85]
                        this.playerTime = rs[89]
                        this.playerKarma = int(rs[90]) if rs[90] != None else 0
                        this.loginTime = Utils.getTime()
                       # this.roles = map(str, filter(None, rs[91].split(",")))
                    else:
                        reactor.callLater(1, lambda: this.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF("").writeUTF("").toByteArray()))
                        return

            if "@" not in playerName:
                if this.privLevel == -1:
                    this.sendPacket(Identifiers.old.send.Player_Ban_Login, ["The account has been permanently removed."])
                    this.transport.loseConnection()
                    return

                this.server.lastPlayerCode += 1
                this.playerName = playerName
                this.playerCode = this.server.lastPlayerCode

                for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                    this.checkAndRebuildTitleList(name)

                this.sendCompleteTitleList()
                this.Shop.checkAndRebuildBadges()
                Cursor.execute("insert into loginlogs values (%s, %s, %s, %s)", [playerName, this.ipAddress, Utils.getDate(), this.langue])

                
                for title in this.titleList:
                    if str(title).split(".")[0] == str(this.titleNumber):
                        this.titleStars = int(str(title).split(".")[1])
                        break
                this.isMute = playerName in this.server.userMuteCache
                this.server.players[this.playerName] = this
                this.sendPlayerIdentification()
                this.sendLogin()
                this.Shop.sendShamanItems()
                this.sendPacket([60, 4], chr(1))
                if startRoom.startswith("\x03[Tutorial]"):
                    if not this.isGuest:
                        this.DailyQuest.loadDailyQuest(True)
                else:
                    this.DailyQuest.loadDailyQuest(False)
                this.Skills.sendShamanSkills(False)
                this.Skills.sendExp(this.shamanLevel, this.shamanExp, this.shamanExpNext)
                if this.shamanSaves >= 1000:
                    this.sendShamanType(this.shamanType, (this.shamanSaves >= 1000 and this.hardModeSaves >= 1000))

                this.server.checkPromotionsEnd()
                this.sendTimeStamp()
                this.sendPromotions()

                if this.tribeCode != 0:
                    tribeInfo = this.tribulle.getTribeInfo(this.tribeCode)
                    this.tribeName = tribeInfo[0]
                    this.tribeMessage = tribeInfo[1]
                    this.tribeHouse = tribeInfo[2]
                    this.tribeRanks = tribeInfo[3]
                    this.tribeChat = tribeInfo[4]

                #this.tribulle.sendTribe(False)
                #this.tribulle.sendPlayerInfo()
                #this.tribulle.sendIgnoredsList()
                this.tribulle.sendFriendsList(None)

                for player in this.server.players.values():
                    if this.playerName and player.playerName in this.friendsList and player.friendsList:
                        player.tribulle.sendFriendConnected(this.playerName)
   
                if this.tribeCode != 0:
                    this.tribulle.sendTribeMemberConnected()

                if this.privLevel in [5, 6, 7, 8]:
                    privbyte = {5:9, 6:7, 7:3, 8:3}[this.privLevel] # 2: arbitre, 3: modo, 7: mapcrew, 8: luateam, 9: funcorp, 10: fashionsquad
                    ulkebyte = this.langue.lower().swapcase()
                    userbyte = this.playerName + " se ha conectado."
                    this.sendStaffCM(privbyte, ulkebyte, userbyte)

                if this.privLevel in [9, 10, 11]:
                    privbyte = this.langue.lower().swapcase()
                    userbyte = this.playerName + " se ha conectado."
                    this.sendStaffCM(2, privbyte, userbyte)
                    this.sendStaffCM(3, privbyte, userbyte)
                    this.sendStaffCM(7, privbyte, userbyte)
                    this.sendStaffCM(9, privbyte, userbyte)
                    
                if this.privLevel >= 1:
                    this.server.sendStaffMessage(6, "<CH>"+this.playerName+" <J>se ha conectado</J>")

                this.sendInventoryConsumables()
                this.Shop.checkselfsAndMessages(selfs, messages)
                this.checkLetters(letters)
                this.resSkillsTimer = reactor.callLater(10, setattr, this, "canRedistributeSkills", True)
                this.startBulle(this.server.checkRoom(startRoom, this.langue) if not startRoom == "" and not startRoom == "1" else this.server.recommendRoom(this.langue))
                this.langueStaff = this.langue
                this.listanegra = this.collectBlackList()
#                this.feli.checkIP(this.ipAddress)

                reactor.callLater(300, this.sendAutoMessage)
                this.sendMessage("<vp>¿Te gustaría ver los comandos? Escribe =></vp> <j>/help</j>")

    def sendAutoMessage(this):
        this.sendMessage('<VP>[%s] Discord => https://discord.gg/CEkTTAb' %(this.langue))
        reactor.callLater(900, this.sendAutoMessage)

    def winBadgeEvent(this, badge):
        if not badge in this.shopBadges:
            this.sendAnimZelda(3, badge)
            try: this.shopBadges[badge] += 1;
            except:this.shopBadges[badge] = 1
            this.Shop.checkAndRebuildBadges()
            this.Shop.sendUnlockedBadge(badge)
            
    def EventTitleKazan(this, title):
        if not title in this.specialTitleList:
            this.specialTitleList.append(title + 0.1)
            this.sendUnlockedTitle(title, 1)
            this.sendCompleteTitleList()
            this.sendTitleList()

    def sendStaffCM(this, byte, username, message, all=True):
        if all:
            for client in this.server.players.values():
                if client.privLevel >= 4:
                    client.sendPacket([6, 10], ByteArray().writeByte(byte).writeUTF(username).writeUTF(message).writeShort(0).writeShort(0).toByteArray())
        else:
            this.sendPacket([6, 10], ByteArray().writeByte(byte).writeUTF(username).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def sendAllModerationChat(this, type, message):
        this.server.sendStaffChat(type, this.langue, Identifiers.send.Staff_Chat, ByteArray().writeByte(1 if type == -1 else type).writeUTF(this.playerName).writeUTF(message).writeShort(0).writeShort(0).toByteArray())

    def sendTotalRec(this):
        if this.room.isSpeedRace:
            if this.privLevel != 0:
                totalrecs = 0
		CursorMaps.execute("select * from Maps where Player = ?", [this.playerName])
		for rs in CursorMaps.fetchall():
		    totalrecs += 1
                try: this.sendMessage("<bl>Tus récords: </font><BV>:</BV> <font color='#9a9a9a'>%s</font>" %(totalrecs))
                except: this.sendMessage("<R>Error</R>") 

    def sendListRec(this):
	if this.room.isSpeedRace:
	    if this.privLevel != 0:
                no = 0
		recordList = "<p align='center'><VP>"+this.playerName+"'s Record (List)</VP></p>\n"
		CursorMaps.execute("select * from Maps where Player = ?", [this.playerName])
		for rs in CursorMaps.fetchall():
		    bestsecond = rs["Time"]
		    code = rs["Code"]
		    date = rs["RecDate"] 
                    second = bestsecond * 0.01
                    no += 1
		    recordList += "<p align='left'><font color='#9a9a9a'>"+str(no)+"-)</font> <font color='#f17e7e'>(@%s)</font> - <font color='#f17e7e'>(%ss)</font> - <font color='#f17e7e'>(%s)</font>\n" %(code,second,str(datetime.fromtimestamp(float(int(date)))))
		try: this.sendLogMessage(recordList)
		except: this.sendMessage("Error.")

    def sendLeaderBoard(this):
        if this.room.isSpeedRace:
                sx,sy = 800,400
                pg,pu = 410,340
                x,y = (sx-pg)/2,(sy-pu)/2
                ly = y+48
                
                addText = this.room.addTextArea
                isim = this.playerName
                this.lbsayfa,sinir = 1,10
                this.kayitlar = sorted(this.server.fastRacingRekorlar["siraliKayitlar"],key=lambda x: x[1],reverse=True)
                if len(this.kayitlar) < 10: sinir=len(this.kayitlar)
                this.sayfasayi = int(math.ceil(len(this.kayitlar)/10.0))
                if this.sayfasayi < 1: this.sayfasayi = 1
                
                addText(5000, "<p align='center'><font color='#ffc15e'><b>LEADER BOARD</b></font></p>", isim, x,y, pg,pu, 0x111111, 0x111111, 90, False)
                addText(5001, "" , isim, x+20, y+20, pg-40, 15, 0x111111, 0xFFFFFF, 10, False)
                addText(5002, "<p align='center'><font color='#ffc15e'>Player</font></p>" , isim, x-80, y+20, pg-40, 40, 0x111111, 0xFFFFFF, 0, False)
                addText(5003, "<p align='center'><font color='#ffc15e'>Record</font></p>" , isim, x+80, y+20, pg, 40, 0x111111, 0x000000, 0, False)
                addText(5035, "<p align='center'><a href='event:lbgeri'><font color='#ffc15e'>«</a> 1 / "+str(this.sayfasayi)+" <a href='event:lbileri'><b>»</b></font></a>" , isim, x, pu+10, pg, 40, 0x324650, 0x000000, 0, False)	
                addText(5036, "<a href='event:lbkapat'><font color='#ffc15e'>X</font></a>" , isim, (x+pg)-11, y, 12, 15, 0x111111, 0x111111, 100, False)	
                
                i,bos = 0," "*16
                for sira in range(sinir):
                    i+=1
                    t = this.kayitlar[sira]
                    recisim,rec = t[0],t[1]
                    addText(5003+i, bos+"<font color='#ffc15e'><b>"+str(recisim)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 30, False)
                    addText((5013+i), "<p align='center'><font color='#ffc15e'>"+str(rec)+"</font></p>" , isim,  x+((pg/2)), ly+(27*(i-1)), (pg-40)/2, 18, 0xFFFFFF, 0x000000, 30, False)
                    addText((5024+i), "<font color='#ffc15e'><b>"+str(i)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0, False)
                
    def lbSayfaDegis(this,ileri,kapat=False):
        addText = this.room.addTextArea
        updateText = this.room.updateTextArea
        removeText= this.room.removeTextArea
        isim = this.playerName
        if kapat:
            for i in range(5000,5037):
                removeText(i,isim)
            return
            
        sx,sy = 800,400
        pg,pu = 410,340
        x,y = (sx-pg)/2,(sy-pu)/2
        ly = y+48
        
        addText = this.room.addTextArea
        updateText = this.room.updateTextArea
        removeText= this.room.removeTextArea
        isim = this.playerName
        
        if ileri:
            this.lbsayfa+= 1
            if this.lbsayfa > this.sayfasayi:
                this.lbsayfa = this.sayfasayi
        else:
            this.lbsayfa-= 1
            if this.lbsayfa < 1: this.lbsayfa=1
        
        baslangic = (this.lbsayfa*10) - 9
        bitis = (this.lbsayfa*10) +1  
        if this.lbsayfa==1:
            baslangic,bitis = 0,10
        
        updateText(5035, "<p align='center'><a href='event:lbgeri'><font color='#ffc15e'>«</a> "+str(this.lbsayfa)+" / "+str(this.sayfasayi)+" <a href='event:lbileri'><b>»</b></font></a>" , isim)	    
       
        i,bos = 0," "*16
        for sira in range(baslangic,bitis):
            i+=1
            try:
                t = this.kayitlar[sira]
                recisim,rec = t[0],t[1]
                addText(5003+i, bos+"<font color='#ffc15e'><b>"+str(recisim)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 30, False)
                addText((5013+i), "<p align='center'><font color='#ffc15e'>"+str(rec)+"</font></p>" , isim,  x+((pg/2)), ly+(27*(i-1)), (pg-40)/2, 18, 0xFFFFFF, 0x000000, 30, False)
                addText((5024+i), "<font color='#ffc15e'><b>"+str(sira if this.lbsayfa !=1 else i)+"</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0, False)
            except:
                removeText(5003+i,isim)
                removeText(5013+i,isim)
                removeText(5024+i,isim)
                
    def checkAndRebuildTitleList(this, type):
        titlesLists = [this.cheeseTitleList, this.firstTitleList, this.shamanTitleList, this.shopTitleList, this.bootcampTitleList, this.hardModeTitleList, this.divineModeTitleList]
        titles = [this.server.cheeseTitleList, this.server.firstTitleList, this.server.shamanTitleList, this.server.shopTitleList, this.server.bootcampTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0
        count = this.cheeseCount if type == "cheese" else this.firstCount if type == "first" else this.shamanSaves if type == "shaman" else this.Shop.getShopLength() if type == "shop" else this.bootcampCount if type == "bootcamp" else this.hardModeSaves if type == "hardmode" else this.divineModeSaves if type == "divinemode" else 0
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

    def discoColors(this):
        colors = ["000000", "FF0000", "17B700", "F2FF00", "FFB900", "00C0D9", "F600A8", "850000", "62532B", "EFEAE1", "201E1C"]
        sColor = random.choice(colors)                
        data = struct.pack("!i", this.playerCode)
        data += struct.pack("!i", int(sColor, 16))
        this.room.sendAll([29, 4], data)
        this.discoReady()
##        for client in this.room.clients.values():
##            client.sendTitleMessage('<font color="#9327FC">Disco Time !</font>')
##            reactor.callLater(4, client.sendTitleMessage, '<font color="#FC3027">Disco Time !</font>')
##            reactor.callLater(4, client.sendTitleMessage, '<font color="#F727FC">Disco Time !</font>')
##            reactor.callLater(4, client.sendTitleMessage, '<font color="#9FFC27">Disco Time !</font>')
##            reactor.callLater(4, client.sendTitleMessage, '<font color="#27F0FC">Disco Time !</font>')
##            reactor.callLater(4, client.sendTitleMessage, '<font color="#D3FC27">Disco Time !</font>')

    def sendTitleMessage(this, message):
        for client in this.room.clients.values():
            info = struct.pack('!h', len(message)) + message + '\n'
            client.room.sendPacket([29, 25], info)  

    def collectBlackList(this):
        blacklist = []
        this.Cursor.execute("select links from blacklist")
        rrfRows = this.Cursor.fetchall()
        if rrfRows is None:
                pass
        for rrf in rrfRows:
                blacklist.append(rrf[0])
        return blacklist            

    def discoMessage(this):
        this.sendMessage("<font color='#E9A144'>Disco time begins to entertaining namecolor.</font>")

    def discoReady(this):
        reactor.callLater(4, this.discoColors)
            
    def getConnectedPlayerCount(this):
        return len(this.server.players)

    def updateDatabase(this):
        if not this.isGuest:
            Cursor.execute("update Users set PrivLevel = %s, TitleNumber = %s, FirstCount = %s, CheeseCount = %s, ShamanCheeses = %s, ShopCheeses = %s, ShopFraises = %s, ShamanSaves = %s, HardModeSaves = %s, DivineModeSaves = %s, BootcampCount = %s, ShamanType = %s, ShopItems = %s, ShamanItems = %s, Clothes = %s, Look = %s, ShamanLook = %s, mouseColor = %s, shamanColor = %s, RegDate = %s, Badges = %s, CheeseTitleList = %s, FirstTitleList = %s, ShamanTitleList = %s, ShopTitleList = %s, BootcampTitleList = %s, HardModeTitleList = %s, DivineModeTitleList = %s, SpecialTitleList = %s, BanHours = %s, ShamanLevel = %s, ShamanExp = %s, ShamanExpNext = %s, Skills = %s, LastOn = %s, FriendsList = %s, IgnoredsList = %s, Gender = %s, LastDivorceTimer = %s, Marriage = %s, TribeCode = %s, TribeRank = %s, TribeJoined = %s, SurvivorStats = %s, RacingStats = %s, Consumables = %s, EquipedConsumables = %s, Pet = %s, PetEnd = %s, ShamanBadges = %s, EquipedShamanBadge = %s, VisuDone = %s, CustomItems = %s, Coins = %s, Tokens = %s, DeathStats = %s, Langue = %s, Mayor = %s, AventureCounts = %s, AventurePoints = %s, SavesAventure = %s, DailyQuest = %s, RemainingMissions = %s, Time = %s, Karma = %s, user_line_status = 1, estado = %s, firstMes = %s where Username = %s", [this.privLevel, this.titleNumber, this.firstCount, this.cheeseCount, this.shamanCheeses, this.shopCheeses, this.shopFraises, this.shamanSaves, this.hardModeSaves, this.divineModeSaves, this.bootcampCount, this.shamanType, this.shopItems, this.shamanItems, "|".join(map(str, this.clothes)), this.playerLook, this.shamanLook, this.mouseColor, this.shamanColor, this.regDate, str(this.shopBadges), ",".join(map(str, this.cheeseTitleList)), ",".join(map(str, this.firstTitleList)), ",".join(map(str, this.shamanTitleList)), ",".join(map(str, this.shopTitleList)), ",".join(map(str, this.bootcampTitleList)), ",".join(map(str, this.hardModeTitleList)), ",".join(map(str, this.divineModeTitleList)), ",".join(map(str, this.specialTitleList)), this.banHours, this.shamanLevel, this.shamanExp, this.shamanExpNext, ";".join(map(lambda skill: "%s:%s" %(skill[0], skill[1]), this.playerSkills.items())), this.tribulle.getTime(), ",".join(map(str, filter(None, this.friendsList))), ",".join(map(str, filter(None, this.ignoredsList))), this.gender, this.lastDivorceTimer, this.marriage, this.tribeCode, this.tribeRank, this.tribeJoined, ",".join(map(str, this.survivorStats)), ",".join(map(str, this.racingStats)), ";".join(map(lambda consumable: "%s:%s" %(consumable[0], 250 if consumable[1] > 250 else consumable[1]), this.playerConsumables.items())), ",".join(map(str, this.equipedConsumables)), this.pet, abs(Utils.getSecondsDiff(this.petEnd)), ",".join(map(str, this.shamanBadges)), this.equipedShamanBadge, "|".join(map(str, this.visuDone)), ",".join(map(str, this.custom)), this.nowCoins, this.nowTokens, ",".join(map(str, this.deathStats)), this.langueStaff, "#".join([str(this.votemayor), str(this.candidatar), str(this.isMayor), str(this.isPresidente), str(this.votepresidente), str(this.addpresidente)]), ";".join(map(lambda aventure: "%s:%s" %(aventure[0], aventure[1]), this.aventureCounts.items())), ";".join(map(lambda points: "%s:%s" %(points[0], points[1]), this.aventurePoints.items())), this.aventureSaves, ",".join(map(str, this.dailyQuest)), this.remainingMissions, (this.playerTime+Utils.getSecondsDiff(this.loginTime)), this.playerKarma, this.estado, this.firstMes, this.playerName])
   # def updateAllDB(this, oldName, newName):
##        try: this.updateAllDBFriends(oldName, newName)
##        except: pass
##        try: this.updateAllDBTribes(oldName, newName)
##        except: pass
        #this.Cursor.execute("update Users set Username = %s where Username = %s", [newName, oldName])
        #this.playerName = newName
       # x = this.server.players[oldName]
       # del this.server.players[oldName]
       # this.server.players[this.playerName] = x
      #  del x
##
##    def updateAllDBFriends(this, oldName, newName):
##        this.Cursor.execute("select Username, FriendsList from Users")
##        rs = this.Cursor.fetchall()
##        inList = []
##        if not "," in rs[1] and not len(rs[1]) > 0:
##            return
##        elif len(rs[1]) != 0 and not "," in rs[1]:
##            inList.append(rs[1])
##        for rrf in rs:
##            if oldName in rs[1].split(","):
##                inList.append(rs[0])
##        if len(inList) == 0:
##            return
##        for user in inList:
##            this.Cursor.execute("select FriendsList from Users where Username = %s", [user])
##            xdd = this.Cursor.fetchone()
##            friendList = xdd[0].split(",") if "," in xdd[0] else xdd[0] if len(xdd[0]) > 0 else None
##            if friendList is None:
##                return
##            friendList[friendList.index(oldName)] = newName
##            this.Cursor.execute("update Users set FriendsList = %s where Username = %s", [",".join(friendList) if len(friendList) > 1 else friendList[0], user])
##            this.friendsList = friendList
##
##    def updateAllDBTribes(this, oldName, newName):
##        this.Cursor.execute("select Code, Members from Tribe")
##        rs = this.Cursor.fetchall()
##        inList = []
##        if not "," in rs[1] and not len(rs[1]) > 0:
##            return
##        elif len(rs[1]) != 0 and not "," in rs[1]:
##            inList.append(rs[1])
##        for rrf in rs:
##            if oldName in rs[1].split(","):
##                inList.append(rs[0])
##        if len(inList) == 0:
##            pass
##        for tribeCode in inList:
##            this.Cursor.execute("select Members from Tribe where Code = %s", [tribeCode])
##            tribeMembers = rs[0].split(",")
##            tribeMembers[tribeMembers.index(oldName)] = newName
##            this.Cursor.execute("update Tribe set Members = %s where Code = %s", [",".join(tribeMembers), tribeCode])

    def startBulle(this, roomName):
        #this.sendBulle()
        reactor.callLater(0.4, lambda: this.enterRoom(roomName))

    def enterRoom(this, roomName):
        if this.isTrade:
            this.cancelTrade(this.tradeName)

        roomName = roomName.replace("<", "&lt;")
        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == "-" and this.privLevel >= 7):
            roomName = "%s-%s" %(this.langue, roomName)
            
        for rooms in ["\x03[Editeur] ", "\x03[Totem] ", "\x03[Tutorial] "]:
            if roomName.startswith(rooms) and not this.playerName == roomName.split(" ")[1]:
                roomName = "%s-%s" %(this.langue, this.playerName)
                
        if not this.isGuest:
            nomSalon = ["#utility0%s" % (this.playerName or this.tribeName), "#utility00%s" % (this.playerName or this.tribeName)]
            if roomName == nomSalon[0] or nomSalon[1]:
                if re.search(this.playerName, roomName):
                    reactor.callLater(0.1, this.Utility.moreSettings, "giveAdmin")
                else:
                    if not this.tribeName == '':
                        if re.search(this.tribeName, roomName):
                            reactor.callLater(0.1, this.Utility.moreSettings, "giveAdmin")
        if not this.isGuest: 					   
           if re.search("#utility", roomName):
               reactor.callLater(0.1, this.Utility.moreSettings, "join")
               reactor.callLater(1.5, this.Utility.moreSettings, "removePopups")

        if this.room != None:
            this.room.removeClient(this)

        this.roomName = roomName
        this.sendGameType(11 if "music" in roomName else 4, 0)
        this.sendEnterRoom(roomName)
        this.server.addClientToRoom(this, roomName)
        this.sendPacket(Identifiers.old.send.Anchors, this.room.anchors)
        this.sendPacket([29, 1], "")
        #this.fullMenu.sendMenu()

        for player in this.server.players.values(): 
            if this.playerName and player.playerName in this.friendsList and player.friendsList:
                player.tribulle.sendFriendChangedRoom(this.playerName, this.langueID)

        if this.tribeCode != 0:
            this.tribulle.sendTribeMemberChangeRoom()

        if this.room.isMusic and this.room.isPlayingMusic:
            this.sendMusicVideo(False)

        if this.room.isTribeHouse and this.room.isPlayingMusic:
            this.sendMusicdeo(False)

##        if not this.room.isTotemEditor and not this.room.isEditor and not this.room.isRacing and not this.room.isBootcamp and not this.room.isSurvivor and not this.room.isVillage and not this.room.isDefilante:

        if roomName.startswith(this.langue + "-" + "music") or roomName.startswith(this.langue + "-" + "*music"):
            this.canSkipMusic = False
            if this.skipMusicTimer != None:
                this.skipMusicTimer.cancel()
            this.skipMusicTimer = reactor.callLater(15, setattr, this, "canSkipMusic", True)

        if this.room.isDeathmatch:
            this.room.bindKeyBoard(this.playerName, 3, False, this.room.isDeathmatch)
            this.room.bindKeyBoard(this.playerName, 32, False, this.room.isDeathmatch)
            this.room.bindKeyBoard(this.playerName, 79, False, this.room.isDeathmatch)
            this.room.bindKeyBoard(this.playerName, 80, False, this.room.isDeathmatch)
            this.sendMessage("<ROSE>¡Bienvenido a Deathmatch!", True)
            this.sendMessage("<ROSE>Para bajar: ↓ o presionando la tecla ESPACIO.", True)
            this.sendMessage("<ROSE>Usa la tecla P para ver tu perfil o la tecla O para cambiar los ítems en tu inventario", True)

        if this.room.isFFARace:
            this.room.bindKeyBoard(this.playerName, 3, False, this.room.isFFARace)
            this.room.bindKeyBoard(this.playerName, 32, False, this.room.isFFARace)
            this.canCannon = True
            this.sendMessage("<N>Welcome to <J>#ffarace")
            this.sendMessage("<N>Press <R>down <N>or <R>space <N>to launch cannons.")
            this.sendMessage("<N>Try to be the <R><b>first</b> <N>and the <R><b>survivor</b> <N>!")
            this.sendMessage("<font color='#E56CA3'>Fastracing modulune hoş geldiniz!</font>\n<font color='#e6b31e'>Lider Tablosu '!lb'</font>")#\n<font color='#e6b31e'>Kırılan kayıtlarınız '!lsrec'</font>") 
        if this.room.isSpeedRace:
            this.sendMessage("<ROSE>¡Bienvenido a Fastracing!")
        if this.room.isBigdefilante:
            this.sendMessage("<ROSE>¡Bienvenido a BigDefilante!") 
        if this.room.isMeepRace:
            this.sendMessage("<ROSE>¡Bienvenido a MeepRacing!") 
    
        if this.room.isFlyMod:
            this.room.bindKeyBoard(this.playerName, 32, False, this.room.isFly)
            this.sendLangueMessage("", "<ROSE>Presiona la tecla ESPACIO para poder volar.")
            
        if this.room.isFuncorp:
            this.sendLangueMessage("", "<FC>$FunCorpActive</FC>")

    def resetPlay(this):
        this.iceCount = 2
        this.bubblesCount = 0
        this.currentPlace = 0
        this.ambulanceCount = 0
        this.defilantePoints = 0
        this.bootcampRounds = 0
        this.artefactID = 0
        
        this.isAfk = True
        this.isDead = False
        this.useTotem = False
        this.hasEnter = False
        this.isShaman = False
        this.isVampire = False
        this.hasCheese = False
        this.isSuspect = False
        this.hasBolo = False
        this.hasBolo2 = False
        this.canRespawn = False
        this.selfGet = False
        this.isNewPlayer = False
        this.isOpportunist = False
        this.desintegration = False
        this.canShamanRespawn = False
        this.canKiss = True
        this.hasArtefact = False
        this.room.isFly = False

        this.a = []
        this.i = []
        this.s = []
        
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
        #return
#        this.Cursor.execute('SELECT Time FROM Account WHERE IP = %s', [this.ipAddress])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            return True
        else:
            if (int(str(thetime.time()).split(".")[0]) >= int(rrf[0])):
                return True
            else:
                return False

    def startFrogEvent(this):
        this.sendPacket([5, 51], "\t\x00,\x07\x00i\x07\xb2")
        this.sendPacket([5, 51], "\t\x00-\x07\x00\xc3\x07\xb2")
        this.sendPacket([5, 51], "\t\x00.\x07\x00\xcd\x07\xb2")
        this.sendPacket([5, 51], "\t\x00/\x08\x011\x07\xb2")
        this.sendPacket([5, 51], "\t\x000\x08\x01\x8b\x07\xb2")
        this.sendPacket([5, 51], "\t\x001\x08\x01\x90\x07\xc1")
        this.sendPacket([5, 51], "\t\x002\x08\x01\x95\x07\xb2")
        this.sendPacket([5, 51], "\t\x003\x08\x01\xf9\x07\xb2")
        this.sendPacket([5, 51], "\t\x004\x07\x02S\x07\xb2")
        this.sendPacket([5, 51], "\t\x005\x07\x02]\x07\xb2")
        this.sendPacket([5, 51], "\t\x006\x07\x02\xc1\x07\xb2")
        reactor.callLater(13, this.travarRatos)

    def travarRatos(this):
        this.room.sendAll([100, 66], "\x01")

    def enableKey(this, key, onKeyPress = True, onKeyLeave = True):
        if not this.isDead:
            this.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

    def disableKey(this, key, onKeyPress = False, onKeyLeave = False):
        this.sendPacket([29, 2], struct.pack('!hbb', int(key), onKeyPress, onKeyLeave))

##    def firstcounts8(this):
##        this.firstCount += 350
##        this.cheeseCount += 350
##        this.sendMessage("<font color='#729169'>[Soldier] Everyone in the room win 350 first.")

    def sendSaintConsumables(this):
        id = 2236
        if not id in this.playerConsumables:
            this.playerConsumables[id] = 5
        else:
            count = this.playerConsumables[id] + 5
            this.playerConsumables[id] = count
            this.sendAnimZeldaInventory(4, id, 5)

    def sendSaintBadge(this):
        this.sendAnimZelda(3, 132)
        this.Shop.sendUnlockedBadge(132)
        try: this.shopBadges[132] += 1
        except: this.shopBadges[132] = 1


    def sendSaintMessage(this):
        this.sendMessage("<font color='#EA489E'>[Saint Valentine] Happy Valentine's Day ^^</font>")

    def sendSaintTitle(this):
        this.specialTitleList.append(250.1)
        this.sendUnlockedTitle(250, 1)
        this.sendCompleteTitleList()
        this.sendTitleList()

    def sendSaintEvent(this):
        this.sendSaintMessage()
        reactor.callLater(20, this.sendSaintTitle)
        reactor.callLater(40, this.sendSaintBadge)
        reactor.callLater(60, this.sendSaintConsumables)

    #def sendStartSaintEvent(this):
        #this.room.mapCode == 20410

	


    
    def startPlay(this):
        this.playerStartTimeMillis = this.room.gameStartTimeMillis
        this.isNewPlayer = this.isDead
        this.sendMap(newMapCustom=True) if this.room.mapCode != -1 else this.sendMap() if this.room.isEditor and this.room.EMapCode != 0 else this.sendMap(True)

       # if this.room.mapCode == 20001 or this.room.mapCode == 20002:
            #this.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Fish Man").writeShort(335).writeBoolean(True).writeUTF("87;58,6,0,0,0,0,0,0,0").writeShort(1625).writeShort(356).writeShort(11).writeByte(0).writeShort(0).toByteArray())
            #this.sendNPC(1, 4, "Fish Man", 335, "87;58,6,0,0,0,0,0,0,0", 1625, 356, 11, 0)

        reactor.callLater(3, this.ponercolor)
        shamanCode, shamanCode2 = 0, 0
        if this.room.isDoubleMap:
            shamans = this.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = this.room.getShamanCode()

        if this.playerCode == shamanCode or this.playerCode == shamanCode2:
            this.isShaman = True

        if this.isShaman and not this.room.noShamanSkills:
            this.Skills.getkills()

        if this.room.currentShamanName != "" and not this.room.noShamanSkills:
            this.Skills.getPlayerSkills(this.room.currentShamanSkills)

        if this.room.currentSecondShamanName != "" and not this.room.noShamanSkills:
            this.Skills.getPlayerSkills(this.room.currentSecondShamanSkills)

        this.sendPlayerList()
        if this.room.catchTheCheeseMap and not this.room.noShamanSkills:
            this.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            this.sendPacket(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(shamanCode).writeBoolean(True).toByteArray())
            if not this.room.currentMap in [108, 109]:
                this.sendShamanCode(shamanCode, shamanCode2)
        else:
            this.sendShamanCode(shamanCode, shamanCode2)

        this.sendSync(this.room.getSyncCode())
        this.sendRoundTime(this.room.roundTime + (this.room.gameStartTime - Utils.getTime()) + this.room.addTime)
        this.sendMapStartTimer(False) if this.isDead or this.room.isTutorial or this.room.isTotemEditor or this.room.isBootcamp or this.room.isDefilante or this.room.getPlayerCountUnique() < 2 else this.sendMapStartTimer(True)

        if this.room.isTotemEditor:
            this.initTotemEditor()

            
        if this.room.mapCode == 20410:
            #this.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Mark").writeShort(116).writeBoolean(True).writeUTF("122;174_FFB0AF+FFBCBB+FFC3C2,0,0,66_FFC3C2,0,3_D49F9E,0,9_F6A1A0+F1BDA9+FFD0DA,10_FFC9C8+FFD2D2+FF6461+FFC6C5,0,0").writeShort(600).writeShort(359).writeShort(1).writeByte(11).writeShort(0).toByteArray())
            #this.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Gwen").writeShort(116).writeBoolean(True).writeUTF("108;172,20,0,0,40,0,0,0,0,0,0").writeShort(654).writeShort(359).writeShort(1).writeByte(11).writeShort(0).toByteArray())
            this.sendSaintEvent()
            

       
    
##        if this.room.isSpeedRace:
##            this.sendPacket([29, 25], struct.pack('!h', len('<font color="#E2E05A">Fastracing')) + '<font color="#E2E05A">Fastracing')

        if this.useAnime >= 1:
            this.useAnime = 0

        if this.room.isMeepRace:
            this.sendPacket(Identifiers.send.Can_Meep, 1)

        if this.room.isMulodrome:
            if not this.playerName in this.room.redTeam and not this.playerName in this.room.blueTeam:
                if not this.isDead:
                    this.isDead = True
                    this.sendPlayerDied()

        if this.room.isSurvivor and this.isShaman:
            this.sendPacket(Identifiers.send.Can_Meep, 1)

        if this.room.isOldSurvivor and this.isShaman:
            this.sendPacket(Identifiers.send.Can_Meep, 0)

        this.isEvent = True
        this.room.bindKeyBoard(this.playerName, 32, False, this.isEvent)

        this.isPositioncmd = True
        this.room.bindKeyBoard(this.playerName, 78, False, this.isPositioncmd)
        
        if this.room.mapCode == 20001 or this.room.mapCode == 20002:
            this.sendLangueMessage("", "<font color='#95CAD9'>[Fishing Event] Go to <ROSE>water</ROSE> <font color='#95CAD9'>parts and press space key.")

        if this.room.currentMap in range(200, 211) and not this.isShaman:
            this.sendPacket(Identifiers.send.Can_Transformation, 1)

        if this.room.isVillage:
            reactor.callLater(0.1, this.sendBotsVillage)

        elif this.room.isFFARace:
            reactor.callLater(1.3, this.enableSpawnCN)


    def sendFishingCount(this):
        this.sendPlayerEmote(14, "", False, False)
        item = ["30", "1", "5", "21", "22", "23", "24", "25", "28", "32", "33", "407", "35", "2349", "2252", "2240", "2247", "14", "15", "16", "20", "2", "3", "4", "6", "8", "800", "29", "2234", "2246", "2256", "2330", "11", "31", "34", "26"]
        id = random.choice(item)
        if not id in this.playerConsumables:
            this.playerConsumables[id] = 1
        else:
            count = this.playerConsumables[id] + 1
            this.playerConsumables[id] = count
        this.sendAnimZeldaInventoryx(4, id, 1)    
        id2 = 2343
        if not id2 in this.playerConsumables:
            this.playerConsumables[id2] = 3
        else:
            count = this.playerConsumables[id2] + 3
            this.playerConsumables[id2] = count
        this.sendAnimZeldaInventoryx(4, id2, 3)

    def sendBotsVillage(this):
        this.sendPacket([8, 30], "\xff\xff\xff\xff\x00\x06Oracle\x01+\x01\x00*61;0,0,0,0,0,19_3d100f+1fa896+ffe15b,0,0,0\x08\x8b\x01}\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfe\x00\x08Papaille\x01*\x01\x00\x134;2,0,2,2,0,0,0,0,1\tZ\x00\xd1\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfd\x00\x05Elise\x01]\x01\x00\x143;10,0,1,0,1,0,0,1,0\t\x19\x00\xd1\x01\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfc\x00\x05Buffy\x01[\x01\x00\x06$Buffy\x07t\x01\xf3\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfb\x00\rIndiana Mouse\x01(\x00\x00\x1445;0,0,0,0,0,0,0,0,0\x00\xae\x02\xca\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xfa\x00\x04Prof\x01G\x00\x00\n$Proviseur\x01!\x02\xcb\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xf9\x00\x07Cassidy\x01\x18\x00\x00\x07$Barman\n\xd2\x02%\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], "\xff\xff\xff\xf8\x00\x0fVon Drkkemouse\x01\x1f\x00\x00\n$Halloween\x06\x88\x01z\x00\x01\x0b\x00\x00")
        this.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Wise Stranger").writeShort(319).writeBoolean(True).writeUTF("106;125_902424+D9D9D9,20,0,0,1,0,0,0,0").writeShort(2145).writeShort(635).writeShort(1).writeByte(11).writeShort(0).toByteArray())
        this.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF("Savior").writeShort(354).writeBoolean(True).writeUTF("28;113_CAC5C5+EDE4DB+FFFFFF,9_000000,0,0,0,19_B8B8B8+1FA896+FFF9E1,0,3,0").writeShort(1794).writeShort(751).writeShort(1).writeByte(11).writeShort(0).toByteArray())

    def sendNPC(this, id, id2, name, title, look, px, py, mode, end):
        this.sendPacket([8, 30], ByteArray().writeShort(id).writeShort(id2).writeUTF(name).writeShort(title).writeByte(0).writeUTF(look).writeShort(px).writeShort(py).writeShort(mode).writeByte(5).writeShort(end).toByteArray()) 

    def getPlayerData(this):
        data = ByteArray()
        data.writeUTF(this.playerName if this.mouseName == "" else this.mouseName)
        data.writeInt(this.playerCode)
        data.writeBoolean(this.isShaman)
        data.writeBoolean(this.isDead)
        data.writeShort(this.playerScore)
        data.writeBoolean(this.hasCheese)
        data.writeShort(this.titleNumber)
        data.writeByte(this.titleStars)
        data.writeByte(this.gender)
        data.writeUTF("")
        data.writeUTF("1;0,0,0,0,0,0,0,0,0,0,0" if this.room.isBootcamp else (this.fur if this.fur != "" else this.playerLook))
        data.writeBoolean(False)
        data.writeInt(int(this.tempMouseColor if not this.tempMouseColor == "" else this.mouseColor, 16))
        data.writeInt(int(this.shamanColor, 16))
        data.writeInt(0)
        try:data.writeInt(int(this.nickColor.lower() if this.nickColor != "" else "#95d9d6", 16))
        except:data.writeInt(-1)
        return data.toByteArray()

    def sendShamanCode(this, shamanCode, shamanCode2):
        this.sendShaman(shamanCode, shamanCode2, this.server.getShamanType(shamanCode), this.server.getShamanType(shamanCode2), this.server.getShamanLevel(shamanCode), this.server.getShamanLevel(shamanCode2), this.server.getShamanBadge(shamanCode), this.server.getShamanBadge(shamanCode2))

    def ponercolor(this):
        if this.privLevel >= 2:
            this.room.setNameColor(this.playerName, int(this.mouseColor, 16))			
        if this.mascota > 0:
            if this.mascota == 1:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(4).toByteArray())
            if this.mascota == 2:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(3).toByteArray())
            if this.mascota == 3:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(2).toByteArray())
            if this.mascota == 4:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(1).toByteArray())
            if this.mascota == 5:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(5).toByteArray())
            if this.mascota == 6:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(6).toByteArray())
            if this.mascota == 7:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(7).toByteArray())
            if this.mascota == 8:
                this.room.sendAll([100, 70], ByteArray().writeInt(this.playerCode).writeByte(8).toByteArray())	

    def sendCorrectVersion(this):
        this.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(this.getConnectedPlayerCount()).writeByte(this.lastPacketID).writeUTF('es').writeUTF('es').writeInt(this.authKey).toByteArray())
        this.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeByte(1).writeByte(this.server.adventureID).writeByte(1).writeBoolean(False).toByteArray())
        this.sendPacket(Identifiers.send.Image_Login, ByteArray().writeUTF(this.server.adventureIMG).toByteArray())
        this.sendLuaMessageAdmin("[<V>Player</V>][<V>"+str(this.ipAddress)+"</V>] One player is connecting.")
        this.awakeTimer = reactor.callLater(999999, this.transport.loseConnection)

    def sendLogin(this):
        this.sendPacket(Identifiers.old.send.Login, [this.playerName, this.playerCode, this.privLevel, 30, 1 if this.isGuest else 0, 0, 0, 0])
        if this.isGuest:
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
            this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeByte(200).toByteArray())

    def sendPlayerIdentification(this):
        sly = ByteArray()
        playerID = this.playerID
        Username = this.playerName
        playerTime = this.playerTime
        langueID = this.langueID
        playerCode = this.playerCode
        guest = this.isGuest

        sly.writeInt(playerID)
        sly.writeUTF(Username)
        sly.writeInt(playerTime)
        sly.writeByte(langueID)
        sly.writeInt(playerCode)
        sly.writeBoolean(not guest)

        Authors = {3:7,5:5,7:6,10:10}
        staff = []
        for vanas,level in Authors.items():
            if this.privLevel >= level:
                staff.append(vanas)
                
        # 2: arbitre,
        # 3: modo,
        # 7: mapcrew,
        # 8: luateam,
        # 9: funcorp,
        # 10: fashionsquad

        sly.writeByte(len(staff))
        for staffs in staff:
            sly.writeByte(staffs)

        sly.writeBoolean(False)
        this.sendPacket(Identifiers.send.Player_Identification, sly.toByteArray()) 

   
    def sendTimeStamp(this):
        this.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(Utils.getTime()).toByteArray())

    def enableSpawnCN(this):
        this.canSpawnCN = True

        
    def getCrazzyPacket(this,type,info): 
        data = ByteArray()
        data.writeByte(type)

        if type == 1:
            data.writeShort(int(info[0]))
            data.writeInt(int(str(info[1]), 16))
            
        if type == 2:
            data.writeInt(int(info[0]))
            data.writeInt(int(info[1]))
            data.writeShort(int(info[2]))
            data.writeShort(int(info[3]))
            data.writeShort(int(info[4]))
            data.writeShort(int(info[5]))
        

        if type == 4:
            data.writeInt(int(info[0]))
            data.writeInt(int(info[1]))
        

        if type == 5:
            data.writeInt(int(info[0]))
            data.writeShort(int(info[1]))
            data.writeByte(int(info[2]))
        

        return data.toByteArray()    

    def fireworksUtility(this):
        if this.room.isUtility and this.Utility.isFireworks == True:
            this.Utility.newCoordsConj()
            reactor.callLater(0.2, this.Utility.buildConj)
            reactor.callLater(1, this.Utility.removeConj)
            reactor.callLater(1.5, this.fireworksUtility)
    
    def discoUtility(this):
        if this.room.isUtility == True:
            colors = ["000000", "FF0000", "17B700", "F2FF00", "FFB900", "00C0D9", "F600A8", "850000", "62532B", "EFEAE1", "201E1C"]
            sColor = random.choice(colors)                
            data = struct.pack("!i", this.playerCode)
            data += struct.pack("!i", int(sColor, 16))
            this.room.sendAll([29, 4], data)
            if this.room.discoRoom == True:
                this.reactorDisco()

    def reactorDisco(this):
        if this.room.isUtility == True:
            if this.room.discoRoom == True:
                reactor.callLater(0.7, this.discoUtility)

    def sendPromotions(this):
        for promotion in []:
            this.sendPacket(Identifiers.send.Promotion, ByteArray().writeBoolean(False).writeBoolean(True).writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeBoolean(True).writeInt(promotion[2]).writeByte(0).toByteArray())

    def sendGameType(this, gameType, serverType):
        this.sendPacket(Identifiers.send.Room_Type, gameType)
        this.sendPacket(Identifiers.send.Room_Server, serverType)

    def sendEnterRoom(this, roomName):
        found = False
        rooms = roomName[3:]
        count = "".join(i for i in rooms if i.isdigit())
        for room in ["vanilla", "survivor", "racing", "music", "bootcamp", "defilante", "village", "#deathmatch"]:
            if rooms.startswith(room) and not count == "" or rooms.isdigit():
                found = not (int(count) < 1 or int(count) > 1000000000 or rooms == room)
        this.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBoolean(found).writeUTF(roomName).toByteArray())

    def sendMap(this, newMap=False, newMapCustom=False):
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(this.room.currentMap if newMap else this.room.mapCode if newMapCustom else -1).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastRoundCode).writeShort(0).writeUTF("" if newMap else this.room.mapXML.encode("zlib") if newMapCustom else this.room.EMapXML.encode("zlib")).writeUTF("" if newMap else this.room.mapName if newMapCustom else "-").writeByte(0 if newMap else this.room.mapPerma if newMapCustom else 100).writeBoolean(this.room.mapInverted if newMapCustom else False).toByteArray())

    def sendPlayerList(this):
        players = this.room.getPlayerList()
        data = ByteArray().writeShort(len(players))
        for player in players:
            data.writeBytes(player)
        
        this.sendPacket([144, 1], data.toByteArray())

    def sendSync(this, playerCode):
        this.sendPacket(Identifiers.old.send.Sync, [playerCode, ""] if (this.room.mapCode != 1 or this.room.EMapCode != 0) else [playerCode])

    def sendRoundTime(this, time):
        this.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(0 if time < 0 or time > 32767 else time).toByteArray())

    def sendMapStartTimer(this, startMap):
        this.sendPacket(Identifiers.send.Map_Start_Timer, ByteArray().writeBoolean(startMap).toByteArray())

    def sendPlayerDisconnect(this):
        this.room.sendAll(Identifiers.old.send.Player_Disconnect, [this.playerCode])

    def sendChangeMap(this, time):
       this.room.sendAll([5, 22], ByteArray().writeShort(time).toByteArray())
       if this.room.changeMapTimer:
               try:
                       this.room.changeMapTimer.cancel()
               except:
                       this.room.changeMapTimer=None
       this.room.changeMapTimer = reactor.callLater(time, this.room.mapChange)

    def getPing(this, ip, user):
        if str(ip) != str(this.ipAddress):
            userPing = True
        else:            
            userPing = False
            
        ping = os.popen("ping -n 1 %s"%(ip)).readlines()[-1]
        ping = str(ping.split("= ")[-1]).strip().replace('ms', '')
        
        try:
            if userPing:
                this.sendMessage(str(user) + ", Latency: " + str(ping))
            else:
                this.sendMessage(str(ping))
        except:
            this.sendMessage("<ROSE>Could not ping player.")

    def sendPlayerDied(this):
        this.room.sendAll(Identifiers.old.send.Player_Died, [this.playerCode, this.playerScore])
        this.hasCheese = False

        if this.room.getAliveCount() < 1 or this.room.catchTheCheeseMap or this.isAfk:
            this.canShamanRespawn = False

        if ((this.room.checkIfTooFewRemaining() and not this.canShamanRespawn) or (this.room.checkIfShamanIsDead() and not this.canShamanRespawn) or (this.room.checkIfDoubleShamansAreDead())):
            this.room.send20SecRemainingTimer()
         
        if this.room.isDeathmatch:
            if this.room.checkIfDeathMouse():
                if this.room.getPlayerCount() >= 3:
                   this.sendChangeMap(5)
                for client in this.room.clients.values():
                     if not client.isDead:
                         client.firstCount += 3
                         this.Cursor.execute("update users set deathCount = deathCount + 1 where Username = %s", [client.playerName])
                         client.cheeseCount += 3

        if this.room.isRacing:
            this.racingRounds = 0
        if this.room.isSpeedRace:
            this.fastracingRounds = 0
        if this.room.isRacing:
            if this.room.checkIfDeathMouse():
                this.sendChangeMap(20)

        if this.canShamanRespawn:
            this.isDead = False
            this.isAfk = False
            this.hasCheese = False
            this.hasEnter = False
            this.canShamanRespawn = False
            this.playerStartTimeMillis = time.time()
            for player in this.room.clients.values():
                this.room.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
                player.sendShamanCode(this.playerCode, 0)

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
            this.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(this.playerCode).writeBoolean(True).toByteArray())
            this.hasCheese = True
            
            this.room.numGetCheese += 1 
            if this.room.currentMap in range(108, 114):
                if this.room.numGetCheese >= 10:
                    this.room.killShaman()

            if this.room.isTutorial:
                this.sendPacket(Identifiers.send.Tutorial, 1)
        this.room.canChangeMap = True

    def playerWin(this, holeType, distance=-1):
        if distance != -1 and distance != 1000 and this.isSuspect and this.room.countStats:
            if distance >= 30:
                this.server.sendStaffMessage(7, "[<V>ANTI-HACK</V>][<J>%s</J>][<V>%s</V>] Instant win detected." %(this.ipAddress, this.playerName))
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Actividad sospechosa."])
                this.transport.loseConnection()
                return

        timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
        ntimeTaken = timeTaken/100.0 #for fastracing and bigdefilante
        if timeTaken > 5:
            this.room.canChangeMap = False
            canGo = this.room.checkIfShamanCanGoIn() if this.isShaman else True
            if not canGo:
                this.sendSaveRemainingMiceMessage()

            if this.isDead or not this.hasCheese and not this.isOpportunist:
                canGo = False

            if this.room.isTutorial:
                this.sendPacket(Identifiers.send.Tutorial, 2)
                this.hasCheese = False
                reactor.callLater(10, lambda: this.startBulle(this.server.recommendRoom(this.langue)))
                this.sendRoundTime(10)
                return

            if this.room.isEditor:
                if not this.room.EMapValidated and this.room.EMapCode != 0:
                    this.room.EMapValidated = True
                    this.sendPacket(Identifiers.old.send.Map_Validated, [""])

            if canGo:
                this.isDead = True
                this.hasCheese = False
                this.hasEnter = True
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

                this.currentPlace = place

                if place == 1:
                    this.playerScore += (4 if this.room.isRacing else 4 if this.room.isSpeedRace else 16) if not this.room.noAutoScore else 0
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                        this.firstCount += 3
                        this.cheeseCount += 3
                        this.firstMes += 3

                        timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                        if this.room.isSpeedRace or this.room.isRacing:
                            if int(this.room.getPlayerCount()) >= int(this.server.needToFirst):
                                if this.room.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                                    try:
                                        CursorMaps.execute('select Time from Maps where code = ?', [this.room.mapCode])
                                        timeDB = CursorMaps.fetchone()
                                        s = this.server.fastRacingRekorlar["maplar"]
                                        if s.has_key(this.room.mapCode):
                                            isim,sure = s[this.room.mapCode][0],s[this.room.mapCode][1]
                                        if timeDB[0] == 0 or timeTaken < timeDB[0]:
                                            this.server.rekorKaydet(this.playerName,this.room.mapCode,str(t))
                                            RecDate = Utils.getTime()
                                            CursorMaps.execute('update Maps set Time = ?, Player = ?, RecDate = ? where code = ?', [timeTaken, this.playerName, RecDate, this.room.mapCode])
                                            for client in this.room.clients.values():
                                                    client.sendMessage("[<J>#</J>] <J>%s</J> <N>set a new record for this map in <j>%s<n> second." %(this.playerName,t))

                                    except:
                                        pass

                        timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
                        if timeTaken > 100:
                            t = timeTaken / 100.0
                        else:
                            t = timeTaken / 10.0
                        if this.room.isBigdefilante:
                            if int(this.room.getPlayerCount()) >= int(this.server.needToFirst):
                                if this.room.mapCode not in (-1, 31, 41, 42, 54, 55, 59, 60, 62, 89, 92, 99, 114, 801):
                                    try:
                                        CursorMaps.execute('select BDTime from Maps where code = ?', [this.room.mapCode])
                                        timeDB = CursorMaps.fetchone()
                                        if timeDB[0] == 0 or timeTaken < timeDB[0]:
                                            CursorMaps.execute('update Maps set BDTime = ?, BDTimeNick = ? where code = ?', [timeTaken, this.playerName, this.room.mapCode])
                                            for client in this.room.clients.values():
                                                    client.sendMessage("<font color='#98D1EB'>[BD]:</font> <font color='#E56CA3'>New record</font> <font color='#'>" + this.playerName + "</font> <font color='#E56CA3'>by broken second </font><font color='#E56CA3'>(</font><font color='#FFD700'>" + str(t) + "</font><font color='#E56CA3'>s)</font>")

                                    except:
                                        pass

                    if this.room.isSpeedRace or this.room.isRacing:
                        for player in this.room.clients.values():
                            if this.room.getPlayerCountUnique() >= this.server.needToFirst:
                                if player.langueID >= 0:
                                    player.sendMessage("<R>%s</R> is winner" %(this.playerName))
                                player.sendRoundTime(3)
                                this.room.changeMapTimers(3)

                    if this.room.isBigdefilante:
                        for player in this.room.clients.values():
                            player.sendRoundTime(3)
                            this.room.changeMapTimers(3)

                elif place == 2:
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                        this.cheeseCount += 2
                        this.firstCount += 2
                        this.firstMes += 2
                    this.playerScore += (3 if this.room.isRacing else 3 if this.room.isSpeedRace else 14) if not this.room.noAutoScore else 0
                            
                elif place == 3:
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                        this.cheeseCount += 1
                        this.firstCount += 1
                        this.firstMes += 1
                    this.playerScore += (2 if this.room.isRacing else 2 if this.room.isSpeedRace else 12) if not this.room.noAutoScore else 0

                if not place in [1,2,3]:
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                        this.cheeseCount += 1
                    this.playerScore += (1 if this.room.isRacing else 1 if this.room.isSpeedRace else 10) if not this.room.noAutoScore else 0

                if this.selfGet:
                    if not 2100 in this.playerConsumables:
                        this.playerConsumables[2100] = 1
                    else:
                        count = this.playerConsumables[2100] + 1
                        this.playerConsumables[2100] = count
                    this.sendAnimZeldaInventory(4, 2100, 1)

                if this.room.isMulodrome:
                    if this.playerName in this.room.redTeam:
                        this.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    elif this.playerName in this.room.blueTeam:
                        this.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    this.room.sendMulodromeRound()

                if this.room.isDefilante:
                    this.cheeseCount += 3
                    this.firstCount += 3
                    if not this.room.noAutoScore: this.playerScore += this.defilantePoints

                if this.room.getPlayerCountUnique() >= this.server.needToFirst:
                   if this.room.isRacing or this.room.isSpeedRace or this.room.isMeepRace:
                       this.racingRounds += 1
                       if this.racingRounds >= 5:
                           this.addConsumable(2254, 2)
                           this.racingRounds = 0

                   if this.room.isBootcamp:
                       this.bootcampRounds += 1
                       if this.bootcampRounds == 5:
                           this.addConsumable(2261, 2)

                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.room.isBootcamp:
                    if this.playerCode == this.room.currentShamanCode or this.playerCode == this.room.currentSecondShamanCode:
                        this.shamanCheeses += 11
                        this.addConsumable(2253, 2)
                    else:
                        this.cheeseCount += 0

                        count = 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                        this.shopCheeses += count
                        this.shopFraises += count

                        this.sendGiveCurrency(0, count)
                        this.Skills.earnExp(False, 20)

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

                elif this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.isBootcamp:
                    this.bootcampCount += 5

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

                player = this.server.players.get(this.room.currentSecondShamanName if holeType == 2 and this.room.isDoubleMap else this.room.currentShamanName)

                this.sendPlayerWin(place, timeTaken)

                if this.room.getPlayerCount() >= 2 and this.room.checkIfTooFewRemaining() and not this.room.isDoubleMap:
                    enterHole = False
                    for player in this.room.clients.values():
                        if player.isShaman and player.isOpportunist:
                            player.isOpportunist = True
                            player.playerWin(0)
                            enterHole = True
                            break
                    this.room.checkChangeMap()
                else:
                    this.room.checkChangeMap()

            this.room.canChangeMap = True
        else:
            this.isDead = True
            this.sendPlayerDied()
                    

    def sendSaveRemainingMiceMessage(this):
        this.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(this, type, count):
        this.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWinBak(this, place, timeTaken):
        this.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if this.room.isDefilante else 1 if this.room.isBigdefilante else (2 if this.playerName in this.room.blueTeam else 3 if this.playerName in this.room.blueTeam else 0)).writeInt(this.playerCode).writeShort(this.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        this.hasCheese = False


    def sendPlayerWin(this, place, timeTaken):
        this.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if this.room.isDefilante else (2 if this.playerName in this.room.blueTeam else 3 if this.playerName in this.room.blueTeam else 0)).writeInt(this.playerCode).writeShort(this.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        this.hasCheese = False

    def sendCompleteTitleList(this):
        this.titleList = []
        this.titleList.append(0.1)
        this.titleList.extend(this.shopTitleList)
        this.titleList.extend(this.firstTitleList)
        this.titleList.extend(this.cheeseTitleList)
        this.titleList.extend(this.shamanTitleList)
        this.titleList.extend(this.bootcampTitleList)
        this.titleList.extend(this.hardModeTitleList)
        this.titleList.extend(this.divineModeTitleList)
        this.titleList.extend(this.specialTitleList)
        
        if this.privLevel == 8:
            this.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,])
			
        if this.privLevel == 9:
            this.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
			
        if this.privLevel == 10:
            this.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 
			
        if this.privLevel == 11:
            this.titleList.extend([440.1, 442.1, 444.1, 445.1, 446.1, 447.1, 448.1, 449.1, 450.1, 451.1, 452.1, 453.1,]) 

    def sendTitleList(this):
        this.sendPacket(Identifiers.old.send.Titles_List, [this.titleList])

    def sendUnlockedTitle(this, title, stars):
        this.room.sendAll(Identifiers.old.send.Unlocked_Title, [this.playerCode, title, stars])

    def sendMessage(this, message, all = False):
        p = ByteArray().writeUTF(message)
        this.sendPacket([6, 9], p.toByteArray())

    def sendProfile(this, playerName):
        player = this.server.players.get(playerName)
        packet = ByteArray()
        if player != None and not player.isGuest:
            packet = ByteArray().writeUTF(player.playerName).writeInt(player.playerID).writeInt(str(player.regDate)[:10]).writeByte({1:1, 2:1, 3:13, 4:11, 5:11, 6:5, 7:5, 8:10, 9:10, 10:10, 11:10, 12:10, 13:10}[player.privLevel]).writeByte(player.gender).writeUTF(player.tribeName).writeUTF(player.marriage + 
             "\n<N>Estado :</N> <vp>"+str(player.estado)+"</vp>\n"
             "\n<N>First mensuales :</N> <j>Inicia 01/01/2020</j>\n" ##"\n<N>First mensuales :</N> <j>"+str(player.firstMes)+"</j>\n"
             "<N>País :</N> <J>"+urlopen('http://ip-api.com/line/'+player.ipAddress+'?fields=country').read()+"</J>\n")
            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                packet.writeInt(stat)
            packet.writeShort(player.titleNumber).writeShort(len(player.titleList))
            for title in player.titleList:
                packet.writeShort(int(title - title % 1))
                packet.writeByte(int(round(title % 1 * 10)))
 
            packet.writeUTF(player.playerLook + ";" + player.mouseColor)
            packet.writeShort(player.shamanLevel)
            listBadges = player.shopBadges
            packet.writeShort(len(listBadges) * 2)

            for badge in listBadges.items():
                packet.writeShort(badge[0])
                packet.writeShort(badge[1])
 
            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123]]
            packet.writeByte(len(stats))
            for stat in stats:
                packet.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeByte(stat[3])

            shamanBadges = player.shamanBadges
            #shamanBadges = [25, 26, 27, 34, 32]
            packet.writeUnsignedByte(player.equipedShamanBadge).writeUnsignedByte(len(shamanBadges))
            for shamanBadge in shamanBadges:
                packet.writeUnsignedByte(shamanBadge)
            packet.writeBoolean(True).writeInt(0)

            this.sendPacket(Identifiers.send.Profile, packet.toByteArray())

    def sendPlayerBan(this, hours, reason, silent):
        this.sendPacket(Identifiers.old.send.Player_Ban, [3600000 * hours, reason])
        if not silent and this.room != None:
            for player in this.room.clients.values():
                player.sendLangueMessage("", "<ROSE>$Message_Ban", this.playerName, str(hours), reason)

        this.server.disconnectIPAddress(this.ipAddress)
            
##    def add_role(this, role="User"):
##        if (type(role) == str):
##            if (role.lower() in list(this.server.role_list.values())):
##                for i, k in this.server.role_list:
##                    if (k == role.lower()):
##                        this.roles.append(k)
##                        break
##        else:
##            if (type(role) == int):
##                if (role in this.server.role_list):
##                    this.roles.append(this.server.role_list[role])
##
##    def remove_role(this, role="User"):
##        if (type(role) == str):
##            if (role.lower() in list(this.server.role_list.values())):
##                for i, k in this.server.role_list:
##                    if (k == role.lower()):
##                        if (k in this.roles):
##                            del this.roles[this.roles.index(k)]
##                            break
##        else:
##            if (type(role) == int):
##                if (role in this.server.role_list):
##                    role_name = this.server.role_list[role]
##                    if (role_name in this.roles):
##                        del this.roles[this.roles.index(role_name)]
##
##    def is_priv(this, role="User"):
##        if (type(role) == str):
##            if (role.lower() in list(this.server.role_list.values())):
##                for i, k in this.server.role_list:
##                    if (k == role.lower()):
##                        if (k in this.roles):
##                            return True
##        else:
##            if (type(role) == int):
##                if (role in this.server.role_list):
##                    role_name = this.server.role_list[role]
##                    if (role_name in this.roles):
##                        return True
##        return False

    def openChatLog(this, playerName):
        if this.server.chatMessages.has_key(playerName):
            packet = ByteArray().writeUTF(playerName).writeByte(len(this.server.chatMessages[playerName]))
            for message in this.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            this.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
        
    def sendPlayerEmote(this, emoteID, flag, others, lua):
        packet = ByteArray().writeInt(this.playerCode).writeByte(emoteID)
        if not flag == "": packet.writeUTF(flag)
        this.room.sendAllOthers(this, Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray()) if others else this.room.sendAll(Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray())

    def sendEmotion(this, emotion):
        this.room.sendAllOthers(this, Identifiers.send.Emotion, ByteArray().writeInt(this.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(this, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        packet = ByteArray()
        packet.writeInt(objectID)
        packet.writeShort(code)
        packet.writeShort(px)
        packet.writeShort(py)
        packet.writeShort(angle)
        packet.writeByte(vx)
        packet.writeByte(vy)
        packet.writeBoolean(dur)
        if this.isGuest or sendAll:
            packet.writeByte(0)
        else:
            packet.writeBytes(this.Shop.getShamanItemCustom(code))

        if not sendAll:
            this.room.sendAllOthers(this, Identifiers.send.Spawn_Object, packet.toByteArray())
            this.room.objectID = objectID
        else:
            this.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())


    def sendTotem(this, totem, x, y, playerCode):
        this.sendPacket(Identifiers.old.send.Totem, ["%s#%s#%s%s" %(playerCode, x, y, totem)])

    def sendTotemItemCount(this, number):
        if this.room.isTotemEditor:
            this.sendPacket([28, 11], ByteArray().writeShort(number * 2).writeBoolean(False).writeBoolean(True).toByteArray())

    def initTotemEditor(this):
        if this.resetTotem:
            this.sendTotemItemCount(0)
            this.resetTotem = False
        else:
            if not this.totem[1] == "":
                this.tempTotem[0] = this.totem[0]
                this.tempTotem[1] = this.totem[1]
                this.sendTotemItemCount(this.tempTotem[0])
                this.sendTotem(this.tempTotem[1], 400, 204, this.playerCode)
            else:
                this.sendTotemItemCount(0)

    def sendShamanType(this, mode, canDivine):
        this.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(this.shamanColor, 16)).toByteArray())

    def sendBanConsideration(this):
        this.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])
        
    def sendShamanPosition(this, direction):
        this.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(this.playerCode).writeBoolean(direction).toByteArray())

    def sendLangueMessage(this, community, message, *args):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)
        this.sendPacket(Identifiers.send.Message_Langue, packet.toByteArray())

    def sendModMute(this, playerName, hours, reason, only):
        if not only:
            this.room.sendMessage("", "<ROSE>$MuteInfo2", playerName, playerName, hours, reason)
        else:
            player = this.server.players.get(playerName)
            if player:
                player.sendLangueMessage("", "<ROSE>$MuteInfo1", hours, reason)

    def sendModMessage(this, minLevel, message):
        for client in this.players.values():
            if client.privLevel >= minLevel:
                client.sendMessage(message)

    def sendVampireMode(this, others):
        if this.room.getPlayerCountUnique() >= this.server.needToFirst:
            this.isVampire = True
            p = ByteArray().writeInt(this.playerCode).writeInt(-1)
            if others:
                this.room.sendAllOthers(this, Identifiers.send.Vampire_Mode, p.toByteArray())
            else:
                this.room.sendAll(Identifiers.send.Vampire_Mode, p.toByteArray())

    def sendRemoveCheese(this):
        this.room.sendAll(Identifiers.send.Player_Get_Cheese, ByteArray().writeInt(this.playerCode).writeBoolean(False).toByteArray())
 
    def sendServerMessageAdmin(this, message):
        for client in this.server.players.values():
	    if client.privLevel >= 5:
                client.sendPacket([6, 20], ByteArray().writeByte(0).writeUTF(message).writeShort(0).toByteArray())

    def sendGameMode(this, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 11, 2, 10, 18, 16]
        packet = ByteArray().writeByte(len(types))
        for roomType in types:
            packet.writeByte(roomType)
        
        packet.writeByte(mode)
        modeInfo = this.server.getPlayersCountMode(mode, "all")
        if mode != 18:
            packet.writeByte(1).writeByte(this.langueID).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            roomsCount = 0
            for checkRoom in this.server.rooms.values():
                if {1:checkRoom.isNormRoom, 3:checkRoom.isVanilla, 8:checkRoom.isSurvivor or checkRoom.isOldSurvivor, 9:checkRoom.isRacing or checkRoom.isSpeedRace or checkRoom.isMeepRace,  11:checkRoom.isMusic, 2:checkRoom.isBootcamp, 10:checkRoom.isDefilante or checkRoom.isBigdefilante, 18:0, 16:checkRoom.isVillage}[mode] and checkRoom.community == this.langue.lower():
                    roomsCount += 1
                    packet.writeByte(0).writeByte(this.langueID).writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(False)
                
            if roomsCount == 0:
                packet.writeByte(0).writeByte(this.langueID).writeUTF(("" if mode == 1 else (modeInfo[0]).split(" ")[1]) + "1").writeShort(0).writeUnsignedByte(200).writeBoolean(False)
        #Minigames
        else:
##            minigames, privateMinigames, minigamesList, roomsList = ["#bigdefilante", "#oldsurvivor", "#meepracing", "#deathmatch", "#ffarace", "#fastracing", "#utility"], [], dict(), dict()
            minigames, privateMinigames, minigamesList, roomsList = ["#fastracing", "#bigdefilante", "#meepracing", "#deathmatch"], [], dict(), dict()

            
            for minigame in minigames:
                minigamesList[minigame] = 0
                for checkRoom in this.server.rooms.values():
                    if checkRoom.roomName.startswith(minigame) or checkRoom.roomName.startswith("*" + minigame):
                        minigamesList[minigame] = minigamesList.get(minigame) + checkRoom.getPlayerCount()
                    
                    if checkRoom.roomName.startswith(minigame) and checkRoom.community == (this.langue.lower()) and not checkRoom.roomName == (minigame) and not checkRoom.roomName == ("*" + minigame):
                        roomsList[checkRoom.roomName] = [checkRoom.getPlayerCount(), checkRoom.maxPlayers]

            for minigame, count in minigamesList.items():
                packet.writeByte(1).writeByte(this.langueID).writeUTF(str(minigame)).writeUTF(str(count)).writeUTF("mjj").writeUTF((minigame + this.playerName.lower() if minigame == "#utility" else minigame))

            for minigame, count in roomsList.items():
                packet.writeByte(0).writeByte(this.langueID).writeUTF(str(minigame)).writeShort(count[0]).writeUnsignedByte(count[1]).writeBoolean(False)
        this.sendPacket(Identifiers.send.Game_Mode, packet.toByteArray())

    def sendMusicVideo(this, sendAll):
        music = this.room.musicVideos[0]
        packet = ByteArray().writeUTF(music["VideoID"]).writeUTF(music["Title"]).writeShort(this.room.musicTime).writeUTF(music["By"])
        if sendAll:
            this.room.sendAll(Identifiers.send.Music_Video, packet.toByteArray())
        else:
            this.sendPacket(Identifiers.send.Music_Video, packet.toByteArray())

    def checkMusicSkip(this):
        if this.room.isMusic and this.room.isPlayingMusic:
            count = this.room.getPlayerCount()
            count = count if count % 2 == 0 else count + 1
            if this.room.musicSkipVotes >= (count / 2):
                del this.room.musicVideos[0]
                this.room.musicTime = 0
                this.sendMusicVideo(True)
                this.room.musicSkipVotes = 0
        
    def sendBulle(this):
        this.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(0).writeUTF("x").toByteArray())

    def sendLogMessage(this, message):
        this.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(message) >> 16) & 0xFF).writeUnsignedByte((len(message) >> 8) & 0xFF).writeUnsignedByte(len(message) & 0xFF).writeBytes(message).toByteArray())

    def checkSuspectBot(this, playerName, type):
        pass

    def sendLuaMessage(this, message):
        this.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def sendLuaMessageAdmin(this, message):
        for client in this.server.players.values():
	    if client.playerName in ["Fabri", "Omar", "Baited", "Jeikob", "Sebita"]:
		client.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def runLuaAdminScript(this, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            startTime = int(time.time())
            endTime = int(time.time())
            totalTime = endTime - startTime
            message = "<V>["+this.room.roomName+"]<BL> ["+this.playerName+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)"
            this.sendLuaMessage(message)
        except Exception as error:
            this.server.sendStaffMessage(7, "<V>["+this.room.roomName+"]<BL> [Bot: "+this.playerName+"][Exception]: "+str(error))

    def cnTrueOrFalse(this):
        this.canCN = False

    def sendImg(this, id, image, x, y, sla=1000, minigame=0):
       packet = ByteArray()
       packet.writeInt(id)
       packet.writeUTF(image)
       packet.writeByte(7)
       packet.writeInt(sla)
       packet.writeShort(x)
       packet.writeShort(y)
       this.sendPacket([29, 19], packet.toByteArray())
       if minigame == 1:
          reactor.callLater(0.9, this.removeImage, (id))

    def removeImage(this, id):
       packet = ByteArray()
       packet.writeInt(id)
       this.sendPacket([29, 18], packet.toByteArray())

    def sendContagem(this):
       image = "149af14e1ba.png" if this.countP == 0 else "149af0f217c.png" if this.countP == 1 else "149af14bccc.png" if this.countP == 2 else "149aeabbb5e.png"
       this.sendImg(this.countP, image, 300, 240, 1000, 1)
       this.countP += 1
       if this.countP <= 3:
          reactor.callLater(1, this.sendContagem)
       else:
          this.room.canCannon = True
          this.countP = 0

    def sendDeathInventory(this, page=1):
       ids = 504, 505, 506, 507
       for id in ids:
          this.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       message1 = ""
       message2 = '<font color="#9ab7c6"><a href="event:prev">Previous</a></font>'
       message3 = ""
       message4 = ""
       message5 = '<font color="#9ab7c6"><a href="event:next">Next</a></font>'
       message6 = ""
       message7 = ""
       message8 = '<p align="center"><font size="28" face="Soopafresh,Verdana,Arial,sans-serif" color="#9ab7c6">Inventory</font></p>'
       message9 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       if page == 1:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Happy Halloween</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Use !f to choose your cannon. this is only temporary and will be removed in the future.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 15 else '<a href="event:inventory#use#15"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Golden Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">this cannon was forged with the purest gold found in land. It is meant only for the best of all the mice.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 16 else '<a href="event:inventory#use#16"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Silver Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">These cannons might work really well on weremice!</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 17 else '<a href="event:inventory#use#17"><p align="center">Equip</p>'
          this.sendImg(504, "149aeaa271c.png", 233, 145, 300)
          this.sendImg(505, "149af112d8f.png", 391, 145, 301)
          this.sendImg(506, "149af12c2d6.png", 549, 145, 302)

       if page == 2:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Bronze Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Never before was a cannon so hard and durable.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 18 else '<a href="event:inventory#use#18"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Balanced Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">It might be time for a diet, you should eat more cheese.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 19 else '<a href="event:inventory#use#19"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Plate-Spike Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">this cannon was re-inforced with metal plating and spikes. It must not have been deadly enough yet.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 20 else '<a href="event:inventory#use#20"><p align="center">Equip</p>'
          this.sendImg(504, "149af130a30.png", 233, 145, 300)
          this.sendImg(505, "149af0fdbf7.png", 391, 145, 301)
          this.sendImg(506, "149af0ef041.png", 549, 145, 302)

       if page == 3:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Death Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">this cannon was forged by death himself.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 21 else '<a href="event:inventory#use#21"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Diamond Ore Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Why is there diamond in my cannon?</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 22 else '<a href="event:inventory#use#22"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Lightning Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">this cannon is lightning fast and hits as thunder.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 23 else '<a href="event:inventory#use#23"><p align="center">Equip</p>'
          this.sendImg(504, "149af13e210.png", 233, 145, 300)
          this.sendImg(505, "149af129a4c.png", 391, 145, 301)
          this.sendImg(506, "149aeaa06d1.png", 549, 145, 302)

          
       this.sendMBox(message1, 95, 99, 70, 16, "50%", "CB9748", "CB9748", 131458)#message, x, y, bg, border, alpha, color, color, id, fixed
       this.sendMBox(message2, 95, 100, 70, 16, "50%", "8CB7DE", "8CB7DE", 123479)
       this.sendMBox(message3, 95, 131, 70, 16, "50%", "000001", "000001", 130449)
       this.sendMBox(message4, 95, 129, 70, 16, "50%", "CB9748", "CB9748", 131459)
       this.sendMBox(message5, 95, 130, 70, 16, "50%", "324650", "324650", 123480)
       this.sendMBox(message6, 165, 61, 485, 300, "50%", "000001", "000001", 6992)
       this.sendMBox(message7, 165, 59, 485, 300, "50%", "CB9748", "CB9748", 8002)
       this.sendMBox(message8, 165, 60, 485, 300, "50%", "324650", "324650", 23)
       this.sendMBox(message9, 623, 60, 30, 30, "0%", "000000", "000000", 9012)
       this.sendMBox(message10, 179, 110, 140, 245, "50%", "204318", "988183", 9013)
       this.sendMBox(message11, 229, 141, 40, 40, "50%", "697666", "988183", 9893)
       this.sendMBox(message12, 179, 325, 140, 30, "30%", "791275", "000000", 8983)
       this.sendMBox(message13, 337, 110, 140, 245, "50%", "204318", "988183", 9014)
       this.sendMBox(message14, 387, 141, 40, 40, "50%", "697666", "988183", 9894)
       this.sendMBox(message15, 337, 325, 140, 30, "30%", "791275", "000000", 8984)
       this.sendMBox(message16, 495, 110, 140, 245, "50%", "204318", "988183", 9015)
       this.sendMBox(message17, 545, 141, 40, 40, "50%", "697666", "988183", 9895)
       this.sendMBox(message18, 495, 325, 140, 30, "30%", "791275", "000000", 8985)
       this.sendImg(507, "149af1e58d7.png", 601, 124, 300)

    def sendDeathProfile(this):
       ids = 39, 40, 41
       for id in ids:
          this.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       yn = "Yes" if this.deathStats[3] == 0 else "No"
       message1 = ""
       message2 = "<p align=\"center\"><font size=\"28\" face=\"Soopafresh,Verdana,Arial,sans-serif\" color=\"#9ab7c6\">"+this.playerName+"</font></p><p><font color=\"#c0c0d8\"> Settings</font>\n<font color=\"#6b76bf\">\t• Offset X : </font><font color=\"#009b9b\">"+str(this.deathStats[0])+"</font><J> <a href=\"event:offset#offsetX#1\">[+]</a> <a href=\"event:offset#offsetX#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Offset Y : </font><font color=\"#009b9b\">"+str(this.deathStats[1])+"</font><J> <a href=\"event:offset#offsetY#1\">[+]</a> <a href=\"event:offset#offsetY#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Warn status : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Special Cannon Display : </font><font color=\"#009b9b\"><J><a href=\"event:show\">"+yn+"</a></font></p><p><font color=\"#c0c0d8\"> Season</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><font color=\"#6b76bf\">\t• Rank : </font><font color=\"#009b9b\">1</font> \n<p><font color=\"#c0c0d8\"> Global</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">2</font></p><p><font color=\"#c0c0d8\"> Team</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><p><font color=\"#c0c0d8\"> Honour Battle</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p>"
       message3 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       message4 = ""
       message5 = ""
       message6 = ""
       #this.sendPacket([29, 20], '\x00\x00#1\x00X<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>\x02\x06\x00<\x00\x1e\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
       this.sendImg(39, "149af12df23.png", 427, 180, 201)
       this.sendImg(40, "149af10434e.png", this.deathStats[5], this.deathStats[6], 202)
       this.sendImg(41, "149af10637b.png", 152, 90, 203)
       this.sendMBox(message1, 267, 59, 278, 290, "100%", "698358", "698358", 7999, False)
       this.sendMBox(message2, 267, 60, 278, 280, "100%", "324650", "324650", 20)
       this.sendMBox(message3, 518, 59, 30, 30, "0%", "000000", "000000", 9009)
       this.sendMBox(message4, 152, 91, 101, 101, "100%", "000001", "000001", 7239)
       this.sendMBox(message5, 152, 89, 101, 101, "100%", "698358", "698358", 8249)
       this.sendMBox(message6, 152, 90, 101, 101, "100%", "324650", "324650", 270, False)
       
    def sendMBox(this, text, x, y, width, height, alpha, bgcolor, bordercolor, boxid, fixed=True):
       p = ByteArray()
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
       p.writeInt(int(boxid))
       p.writeUTF(text)
       p.writeShort(x)
       p.writeShort(y)
       p.writeShort(width)
       p.writeShort(height)
       p.writeInt(bgcolor)
       p.writeInt(bordercolor)
       p.writeByte(alpha)
       p.writeShort(fixed)
       
       this.sendPacket([29, 20], p.toByteArray())

    def getReturnValues(this, byte):
        this.AntiBots[byte] = True   

    def chatEnable(this):
        this.chatdisabled = False

    def sendAnimZelda(this, type, item):
        if type == 7:
            this.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(this.playerCode).writeByte(type).writeUTF("$De6").writeByte(item).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Anim_Zelda, ByteArray().writeInt(this.playerCode).writeByte(type).writeInt(item).toByteArray())
  
    def sendAnimZelda2(this, type, item=0, case="", id=0):
        packet = ByteArray().writeInt(this.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeUnsignedByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        this.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())

    #def sendAnimZelda(this, type, item=0, case="", id=0):
        #packet = ByteArray().writeInt(this.playerCode).writeByte(type).
        #if type == 7:
            #packet.writeUTF(case).writeUnsignedByte(id)
        #elif type == 5:
          #  packet.writeUTF(case)
        #else:
           # packet.writeInt(item)
       # this.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())

    def sendAnimZeldaInventory(this, id1, id2, count):
        if id1 == 4:
            this.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
        this.room.sendAll([8, 44], ByteArray().writeInt(this.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def sendAnimZeldaInventoryx(this, id1, id2, count):
        if id1 == 4:
            this.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
            #this.sendData("\x64C", this.put("bhh", 0, id2, count))
        #this.room.sendAll([8, 44], ByteArray().writeInt(this.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def premioVillage(this, itemID):
        item = this.server.npcs["Shop"].get(this.lastNpc)[itemID]
        type, id, amount, priceItem, priceAmount = item[0] , item[1] , item[2] , item[4] , item[5]
                
        if this.playerConsumables.has_key(priceItem) and this.playerConsumables.get(priceItem) >= priceAmount:
            count = this.playerConsumables.get(priceItem) - priceAmount
            if count <= 0:
                del this.playerConsumables[priceItem]
            else:
                this.playerConsumables[priceItem] = count
                
            this.updateInventoryConsumable(priceItem, count)
                
            if type == 1:
                this.sendAnimZelda(3, id)
                this.Shop.sendUnlockedBadge(id)
                try: this.shopBadges[id] += 1
                except: this.shopBadges[id] = 1

            elif type == 2:
                this.sendAnimZelda(6, id)
                this.shamanBadges.append(id)
                    
            elif type == 3:
                this.titleList.append(id + 0.1)
                this.sendUnlockedTitle(id, 1)
                    
            elif type == 4:
                this.addConsumable(id, amount)
                
            this.openNpcShop(this.lastNpc)

    def openNpcShop(this, npcName):
        npcShop = this.server.npcs["Shop"].get(npcName)
        this.lastNpc = npcName
            
        data = ByteArray()
        data.writeUTF(npcName)
        data.writeByte(len(npcShop))
        
        i = 0
        while i < len(npcShop):
            item = npcShop[i]
            type, id, amount, priceItem, priceAmount = item[0], item[1], item[2], item[4], item[5]
            if (type == 1 and this.shopBadges.has_key(id)) or (type == 2 and id in this.shamanBadges) or (type == 3 and float(str(id) + ".1") in this.titleList) or (type == 4 and this.playerConsumables.has_key(id) and this.playerConsumables.get(id) + amount > 4667649494949499494949494976649764976464379797667676292929929292929292929929292929292992929293938387474672828299393929373772):
                data.writeByte(2)
            elif not this.playerConsumables.has_key(priceItem) or this.playerConsumables.get(priceItem) < priceAmount:
                data.writeByte(1)
            else:
                data.writeByte(0)
                
            data.writeByte(type)
            data.writeShort(id)
            data.writeShort(amount)
            data.writeByte(item[3])
            data.writeShort(priceItem)
            data.writeShort(priceAmount)
            data.writeInt(0)
			
            i += 1
            
        this.sendPacket(Identifiers.send.NPC_Shop, data.toByteArray())

    def buyNPCItem(this, itemID):
        item = this.server.npcs["Shop"].get(this.lastNpc)[itemID]
        type, id, amount, priceItem, priceAmount = item[0] , item[1] , item[2] , item[4] , item[5]
                
        if this.playerConsumables.has_key(priceItem) and this.playerConsumables.get(priceItem) >= priceAmount:
            count = this.playerConsumables.get(priceItem) - priceAmount
            if count <= 0:
                del this.playerConsumables[priceItem]
            else:
                this.playerConsumables[priceItem] = count
                
            this.updateInventoryConsumable(priceItem, count)
                
            if type == 1:
                this.sendAnimZelda(3, id)
                this.Shop.sendUnlockedBadge(id)
                try: this.shopBadges[id] += 1
                except: this.shopBadges[id] = 1

            elif type == 2:
                this.sendAnimZelda(6, id)
                this.shamanBadges.append(id)
                    
            elif type == 3:
                this.specialTitleList.append(id + 0.1)
                this.sendUnlockedTitle(id, 1)
                this.sendCompleteTitleList()
                this.sendTitleList()
                    
            elif type == 4:
                this.sendNewConsumable(id, amount)
                sum = (this.playerConsumables[id] if this.playerConsumables.has_key(id) else 0) + amount 
                #this.addConsumable(id,amount)
                if this.playerConsumables.has_key(id):
                    this.playerConsumables[id] = sum
                    this.updateInventoryConsumable(id, sum)
                else:
                    this.playerConsumables[id] = sum
                    this.updateInventoryConsumable(id, sum)
                        
            this.openNpcShop(this.lastNpc)

    def addConsumable(this, id, amount):
        amount = amount if amount <= 250 else 250
        this.sendNewConsumable(id, amount)
        sum = amount + this.playerConsumables[id] if id in this.playerConsumables else 0
        this.playerConsumables[id] = amount
        this.updateInventoryConsumable(id, sum)

    def sendInventoryConsumables(this):
        packet = ByteArray().writeShort(len(this.playerConsumables))
        for id in this.playerConsumables.items():
            packet.writeShort(id[0])
            packet.writeUnsignedByte(250 if id[1] > 250 else id[1]).writeByte(0)
            packet.writeBoolean(True)
            packet.writeBoolean(False if id[0] in this.server.inventory or id[0] in range(2111, 2200) else True)
            packet.writeBoolean(True)
            packet.writeBoolean(True)
            packet.writeBoolean(True)
            packet.writeBoolean(False)
            packet.writeBoolean(False)
            packet.writeByte(this.equipedConsumables.index(id[0]) + 1 if id[0] in this.equipedConsumables else 0)
        this.sendPacket(Identifiers.send.Inventory, packet.toByteArray())

    def updateInventoryConsumable(this, id, count):
        this.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray())

    def useInventoryConsumable(this, id):
        if id in [29, 30, 2241, 2330]:
            this.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())

    def getLookUser(this, name):
        for room in this.server.rooms.values():
            for client in room.clients.values():
                if client.playerName == name:
                    return client.playerLook             
        this.Cursor.execute('SELECT Look FROM users WHERE Username = %s', [name])
        return this.Cursor.fetchone()[0]
    
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
                    this.sendTradeResult(playerName, 3)
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
            player.sendTradeResult(this.playerName, 2)

    def tradeAddConsumable(this, id, isAdd):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.playerName:
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

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(False).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(True).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())

    def tradeResult(this, isAccept):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.playerName:
            this.tradeConfirm = isAccept
            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(False).writeBoolean(isAccept).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(True).writeBoolean(isAccept).toByteArray())
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
                        player.playerConsumables[consumable[0]] = count

                for consumable in this.tradeConsumables.items():
                    if player.playerConsumables.has_key(consumable[0]):
                        player.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                    count = this.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del this.playerConsumables[consumable[0]]
                        if consumable[0] in this.equipedConsumables:
                            this.equipedConsumables.remove(consumable[0])
                    else:
                        this.playerConsumables[consumable[0]] = count

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
            this.Cursor.execute("update users set Letters = '' where PlayerID = %s", [this.playerID])

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
        # Settings anti hack
        this.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        this.ac_enabled = True
        this.ac_c = json.loads(this.ac_config)
        this.learning = this.ac_c['learning']
        this.bantimes = this.ac_c['ban_times']
        this.s_list = open('./cheat/anticheat_allow', 'r').read()
        if this.s_list != '':
            this.s_list = this.s_list.split(',')
            this.s_list.remove('')
        else:
            this.s_list = []

        # Settings 
        this.miceName = str(this.config("game.miceName"))
        this.isDebug = bool(int(this.config("game.debug")))
        this.adventureIMG = this.config("game.adventureIMG")
        this.lastChatID = int(this.config("ids.lastChatID"))
        this.serverURL = this.config("server.url").split(", ")
        this.adventureID = int(this.config("game.adventureID"))
        this.needToFirst = int(this.config("game.needToFirst"))
        this.lastPlayerID = int(this.config("ids.lastPlayerID"))
        this.lastTopicID = int(this.config("game.cafelasttopicid"))
        this.lastPostID = int(this.config("game.cafelastpostid"))
        this.lastMapEditeurCode = int(this.config('game.lastMapCodeId'))
        this.initialCheeses = int(this.config("game.initialCheeses"))
        this.initialFraises = int(this.config("game.initialFraises"))
        this.timeEvent = int(this.config("game.timeevent"))
        this.calendarioSystem = eval(this.config("game.calendario"))
        this.calendarioCount = eval(this.config("game.calendarioCount"))
        
        this.shopList = this.configShop("shop.shopList").split(";")
        this.shamanShopList = this.configShop("shop.shamanShopList").split(";")
        this.newVisuList = eval(this.configShop("shop.visuDone"))

        this.ftpHOST = str(this.config("FTP Host"))
        this.ftpUSER = str(this.config("FTP Username"))
        this.ftpPASS = str(this.config("FTP Password"))
        this.dftAvatar = str(this.config("Default Avatar"))

         
        # Integer
        this.activeStaffChat = 0
        this.lastselfID = 0
        this.lastPlayerCode = 0
        this.startServer = datetime.today()

        # Nonetype
        this.rebootTimer = None
        this.rankingTimer = None

        # List
        this.loginKeys = []
        this.packetKeys = []
        this.userMuteCache = []
        this.shopPromotions = []
        this.IPTempBanCache = []
        this.IPPermaBanCache = []
        this.userTempBanCache = []
        this.userPermaBanCache = []
        this.staffChat = []
        this.inventory = [2236, 2202, 2203, 2204, 2227, 2235, 2257, 2261, 2253, 2254, 2260, 2261, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2276, 2277, 2278, 2279, 2280, 2281, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2327, 2328]
        #this.inventory = [2224, 2236]
        this.ranking = [{}, {}, {}, {}]

        # Dict
        this.rooms = {}
        this.players = {}
        this.shopselfs = {}
        this.vanillaMaps = {}
        this.chatMessages = {}
        this.shopListCheck = {}
        this.connectedCounts = {}
        this.reports = {}
        this.cafeTopics = {}
        this.cafePosts = {}
        this.shamanShopListCheck = {}
        this.fastRacingRekorlar = {"maplar":{},"siraliKayitlar":[],"kayitlar":{}}
        this.statsPlayer = {"racingCount":[1500,10000,10000,10000], "survivorCount":[1000,800,20000,10000], "racingBadges":[124,125,126,127], "survivorBadges":[120,121,122,123]}
        this.shopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2220:32, 2236:36, 2204:40, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:70, 2255:72, 2256:128, 2257:135, 2258:136, 2259:137, 2260:138, 2261:140, 2262:141, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175, 2281:176, 2282:177, 2283:178, 2284:179, 2285:180, 2286:183, 2287:185, 2288:186, 2289:187, 2290:189, 2291:191, 2292:192, 2293:194, 2294:195, 2295:196, 2296:197, 2297:199, 2298:200, 2299:201, 230100:203, 230101:204, 230102:205, 230103:206, 230104:207, 230105:208, 230106:210, 230107:211, 230108:212, 230110: 214, 230111: 215, 230112: 216, 230113: 217, 230114: 220, 230115: 222, 230116: 223, 230117: 224, 230118: 225, 230119: 226, 230120: 227, 230121: 228, 230122: 229, 230123: 231, 230124: 232, 230125: 233, 230126: 234, 230127: 235, 230128: 236, 230129: 237, 230130: 238, 230131: 239, 230132: 241, 230133: 242, 230134: 243, 230135: 244, 230136: 245}
        this.hardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
        this.divineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
        this.shamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
        this.firstTitleList = {281:9.1, 562:10.1, 843:11.1, 1124:12.1, 1405:42.1, 1686:43.1, 1967:44.1, 2248:45.1, 2529:46.1, 2810:47.1, 3091:48.1, 3372:49.1, 3653:50.1, 3934:51.1, 4215:52.1, 4496:53.1, 4777:54.1, 5058:55.1, 5339:56.1, 5620:57.1, 5901:58.1, 6182:59.1, 6463:60.1, 6744:61.1, 7025:62.1, 7306:63.1, 7587:64.1, 7868:65.1, 8149:66.1, 8430:67.1, 8711:68.1, 8992:69.1, 9273:231.1, 9554:232.1, 9835:233.1, 10116:70.1, 10397:224.1, 10678:225.1, 10959:226.1, 11240:227.1, 11521:202.1, 11802:228.1, 12083:229.1, 12364:230.1, 12645:71.1}
        this.cheeseTitleList = {281:5.1, 562:6.1, 843:7.1, 1124:8.1, 1405:35.1, 1686:36.1, 1967:37.1, 2248:26.1, 2529:27.1, 2810:28.1, 3091:29.1, 3372:30.1, 3653:31.1, 3934:32.1, 4215:33.1, 4496:34.1, 4777:38.1, 5058:39.1, 5339:40.1, 5620:41.1, 5901:72.1, 6182:73.1, 6463:74.1, 6744:75.1, 7025:76.1, 7306:77.1, 7587:78.1, 7868:79.1, 8149:80.1, 8430:81.1, 8711:82.1, 8992:83.1, 9273:84.1, 9554:85.1, 9835:86.1, 10116:87.1, 10397:88.1, 10678:89.1, 10959:90.1, 11240:91.1, 11521:92.1, 11802:234.1, 12083:235.1, 12364:236.1, 12645:237.1, 12926:238.1, 13207:93.1}
        this.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
        this.bootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}


        # Files
        this.parseSWF = this.parseFile("./extra/jsons/infoSWF.json")
        this.captchaList = this.parseFile("./extra/jsons/captchas.json")
        this.promotions = this.parseFile("./extra/jsons/promotions.json")
        this.serverList = this.parseFile("./extra/jsons/serverList.json")
        this.menu = this.parseFile("./extra/jsons/menu.json")
        this.npcs = this.parseFile("./extra/jsons/npcs.json")

        # Others
        #this.CursorCafe = CursorCafe
        this.parseFunctions()
        this.getVanillaMaps()
        this.parsePromotions()
        this.menu = this.Menu()
        this.rankingTimer = reactor.callLater(1, this.getRanking)
        reactor.callLater(1, this.rekorlariYukle)

    def rekorlariYukle(this):
        CursorMaps.execute("select Code,Time,Player from maps where not Player = ''")
        recs = CursorMaps.fetchall()
        t= this.fastRacingRekorlar
        for rs in recs:
            mapkod,isim,sure = rs["Code"],rs["Player"],rs["Time"]
            t["maplar"][mapkod] = [isim,sure]
            if not t["kayitlar"].has_key(isim):
                t["kayitlar"][isim] = {}
            t["kayitlar"][isim][mapkod]=[mapkod,sure]    
        
        for isim in t["kayitlar"]:
            t["siraliKayitlar"].append([isim,len(t["kayitlar"][isim])])
			
        print("[%s] %s Records loaded: %s" %(time.strftime("%H:%M:%S"), config.get("configGame", "game.miceName"),len(recs)))


    def rekorKaydet(this,isim,mapkod,sure):    
        t= this.fastRacingRekorlar
        eskiisim = False
        if t["maplar"].has_key(mapkod):
            eskiisim,sure = t["maplar"][mapkod][0],t["maplar"][mapkod][1]
            if t["kayitlar"].has_key(eskiisim) and t["kayitlar"][eskiisim].has_key(mapkod):
                del t["kayitlar"][eskiisim][mapkod]
   
        t["maplar"][mapkod] = [isim,sure]
        if not t["kayitlar"].has_key(isim):
                t["kayitlar"][isim] = {}
        t["kayitlar"][isim][mapkod] = [mapkod,sure]  
        
        t["siraliKayitlar"] = []
        for isim in t["kayitlar"]:
            t["siraliKayitlar"].append([isim,len(t["kayitlar"][isim])])
        
        CursorMaps.execute("update maps set Time = ?, Player = ? where Code = ?", [sure, isim, mapkod])
    
    def updateConfig(this):
        this.configs('game.lastMapCodeId', str(this.lastMapEditeurCode))
        this.configs("ids.lastPlayerID", str(this.lastPlayerID))
        this.configs("ids.lastChatID", str(this.lastChatID))
        this.configs("game.timeevent", str(this.timeEvent))

##    def getPointsColor(this, playerName, aventure, itemID, itemType, itemNeeded):
##        for client in this.players.values():
##            if client.playerName == playerName:
##                if int(itemID) in client.aventureCounts.keys():
##                    if client.aventureCounts[int(itemID)][1] >= int(itemNeeded):
##                        return 1
##        return 0
##
##    def getAventureCounts(this, playerName, aventure, itemID, itemType):
##        for client in this.players.values():
##            if client.playerName == playerName:
##                if int(itemID) in client.aventureCounts.keys():
##                    return client.aventureCounts[int(itemID)][1]
##        return 0
##
##    def getAventureItems(this, playerName, aventure, itemType, itemID):
##        c = 0
##        for client in this.players.values():
##            if client.playerName == playerName:
##                if aventure == 24:
##                    if itemType == 0 and itemID == 1:
##                        return client.aventureSaves
##                    elif itemType == 0 and itemID == 2:
##                        for item in client.aventureCounts.keys():
##                            if item in range(38, 44):
##                                c += client.aventureCounts[item][1]
##                        return c
##        return 0
        
    def parseFunctions(this):
        # SWF
        data = this.parseSWF
        this.CKEY = data["key"]
        this.Version = data["version"]

        keys = data["packetKeys"]
        i = 0
        while i < len(keys):
            this.packetKeys.append(keys[i])
            i += 1

        login = data["loginKeys"]
        i = 0
        while i < len(login):
            this.loginKeys.append(login[i])
            i += 1

        # Shop
        for item in this.shopList:
            values = item.split(",")
            this.shopListCheck[values[0] + "|" + values[1]] = [int(values[5]), int(values[6])]

        for item in this.shamanShopList:
            values = item.split(",")
            this.shamanShopListCheck[values[0]] = [int(values[3]), int(values[4])]

        # DB
        
        Cursor.execute("select Username from UserPermaBan")
        rs = Cursor.fetchone()
        if rs:
            this.userPermaBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempBan")
        rs = Cursor.fetchone()
        if rs:
            this.userTempBanCache.append(rs[0])

        Cursor.execute("select Username from UserTempMute")
        rs = Cursor.fetchone()
        if rs:
            this.userMuteCache.append(rs[0])

    def Menu(this):
        with open("./extra/jsons/menu.json", "r") as f:
            T = eval(f.read())
        return T

    def config(this, setting):
        return config.get("configGame", setting, 0)

    def configShop(this, setting):
        return config.get("configShop", setting, 0)

    def configs(this, setting, value):
        config.set("configGame", setting, value)
        with open("./extra/configs.properties", "w") as f:
            config.write(f)

    def parseFile(this, directory):
        with open(directory, "r") as f:
            return eval(f.read())

    def updateBlackList(this):
        with open("./extra/jsons/serverList.json", "w") as f:#kaydedimi 
            json.dump(this.serverList, f)

    def getVanillaMaps(this):
        for fileName in os.listdir("./extra/maps/vanilla"):
            with open("./extra/maps/vanilla/"+fileName) as f:
                this.vanillaMaps[int(fileName[:-4])] = f.read()

    def closeServer(this):
        this.updateConfig()
        for client in this.players.values():
            client.updateDatabase()
            client.transport.loseConnection()
            del this.players[client.playerName]

        os._exit(0)

    def sendServerRestart(this, no, sec):
        if sec > 0 or no != 5:
            this.sendServerRestartSEC(120 if no == 0 else (60 if no == 1 else (30 if no == 2 else (20 if no == 3 else (10 if no == 4 else sec)))))
            if this.rebootTimer != None:
                this.rebootTimer.cancel()
            this.rebootTimer = reactor.callLater(60 if no == 0 else (30 if no == 1 else (10 if no == 2 or no == 3 else 1)), lambda : this.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else (sec - 1 if no == 5 else 0)))
        return
    
    def sendServerRestartSEC(this, seconds):
        this.sendPanelRestartMessage(seconds)
        this.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(this, seconds):
        if seconds == 120:
            print '[%s] [SERVER] The server will restart in 2 minutes.' % time.strftime('%H:%M:%S')
        elif seconds < 120 and seconds > 1:
            print '[%s] [SERVER] The server will restart in %s seconds.' % (time.strftime('%H:%M:%S'), seconds)
        else:
            print '[%s] [SERVER] The server will restart in 1 second.' % time.strftime('%H:%M:%S')
            for client in this.players.values():
                client.updateDatabase()

            os._exit(0)

   

    def buildCaptchaCode(this):
        CC = "".join([random.choice(this.captchaList.keys()) for x in range(4)])
        words, px, py, lines = list(CC), 0, 1, []
        for count in range(1, 17):
            wc, values = 1, []
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

    def checkAlreadyExistingGuest(this, playerName):
        if not playerName: playerName = "Souris"
        if this.checkConnectedAccount(playerName):
            playerName += "_%s" %("".join([random.choice(string.ascii_lowercase) for x in range(4)]))
        return playerName

    def checkConnectedAccount(this, playerName):
        return this.players.has_key(playerName)

    def disconnectIPAddress(this, ip):
        for player in this.players.values():
            if player.ipAddress == ip:
                player.transport.loseConnection()

    def checkExistingUser(this, playerName):
        Cursor.execute("select 1 from Users where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def recommendRoom(this, langue, prefix=""):
        count = 0
        result = ""
        while result == "":
            count += 1
            if this.rooms.has_key("%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)):
                if this.rooms["%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)].getPlayerCount() < 25:
                    result = str(count)
            else:
                result = str(count)
        return result

    def checkRoom(this, roomName, langue):
        found = False
        x = 0
        result = roomName
        if this.rooms.has_key(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName):
            room = this.rooms.get(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if this.rooms.has_key((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x)):
                room = this.rooms.get((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result


    def addClientToRoom(this, player, roomName):
        if this.rooms.has_key(roomName):
            this.rooms[roomName].addClient(player)
        else:
            room = Room(this, roomName)
            this.rooms[roomName] = room
            room.addClient(player, True)
            room.mapChange()

    def banPlayer(this, playerName, bantime, reason, modname, silent):        
        found = False

        client = this.players.get(playerName)
        if client != None:
            found = True
            if not modname == "Server":
                client.banHours += bantime
                this.modoPwetIslem(playerName,bantime,reason,modname,"ban")
                this.saveCasier(playerName,"BAN",modname,bantime,reason)
                #Cursor.execute("insert into  values (%s, %s, %s, %s, %s, 'Online', %s)", [playerName, modName, bantime, reason, int(time.time() / 10), player.ipAddress])
                Cursor.execute("insert into BanLog values (%s, %s, %s, %s, %s, 'Online', %s)", [playerName, modname, bantime, reason, int(time.time() / 10), client.ipAddress])
            else:
                this.sendStaffMessage(5, "[BAN] Server banned player "+playerName+" for 1 hour. Reason: Vote Populaire.")

            Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])

            if bantime >= 361 or client.banHours >= 361:
                this.userPermaBanCache.append(playerName)
                Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [client.ipAddress, modname, reason])

            if client.banHours >= 361:
                this.IPPermaBanCache.append(client.ipAddress)
                Cursor.execute("insert into IPPermaBan values (%s, %s, %s)", [client.ipAddress, modname, reason])

            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)
                this.tempBanIP(client.ipAddress, bantime)

            client.sendPlayerBan(bantime, reason, silent)
            
        if not found and not modname == "Server" and bantime >= 1:
            if this.checkExistingUser(playerName):
                found = True
                totalBanTime = this.getTotalBanHours(playerName) + bantime
                if (totalBanTime >= 361 and bantime <= 360) or bantime >= 361:
                    this.userPermaBanCache.append(playerName)
                    Cursor.execute("insert into UserPermaBan values (%s, %s, %s)", [playerName, modname, reason])

                if bantime >= 1 and bantime <= 360:
                    this.tempBanUser(playerName, bantime, reason)

                    this.saveCasier(playerName,"BAN",modname,bantime,reason)

                Cursor.execute("update Users SET BanHours = %s WHERE Username = %s", [bantime, playerName])
            return found

    def checkTempBan(this, playerName):
        Cursor.execute("select 1 from UserTempBan where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def removeTempBan(this, playerName):
        if playerName in this.userTempBanCache:
            this.userTempBanCache.remove(playerName)
        Cursor.execute("delete from UserTempBan where Username = %s", [playerName])

    def tempBanUser(this, playerName, bantime, reason):
        if this.checkTempBan(playerName):
            this.removeTempBan(playerName)

        this.userTempBanCache.append(playerName)
        Cursor.execute("insert into UserTempBan values (%s, %s, %s)", [playerName, reason, str(Utils.getTime() + (bantime * 60 * 60))])

    def getTempBanInfo(this, playerName):
        Cursor.execute("select Reason, Time from UserTempBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return [rs[0], rs[1]]
        else:
            return ["Without a reason", 0]

    def getPermBanInfo(this, playerName):
        Cursor.execute("select Reason from UserPermaBan where Username = %s", [playerName])
        for rs in Cursor.fetchall():
            return rs[0]
        else:
            return "Without a reason"

    def checkPermaBan(this, playerName):
        Cursor.execute("select 1 from UserPermaBan where Username = %s", [playerName])
        return Cursor.fetchone() != None

    def removePermaBan(this, playerName):
        if playerName in this.userPermaBanCache:
            this.userPermaBanCache.remove(playerName)
        Cursor.execute("delete from UserPermaBan where Username = %s", [playerName])
        Cursor.execute("update Users set UnRanked = 0 where Username = %s", [playerName])

    def tempBanIP(this, ip, time):
        if not ip in this.IPTempBanCache:
            this.IPTempBanCache.append(ip)
            if ip in this.IPTempBanCache:
                reactor.callLater(time, lambda: this.IPTempBanCache.remove(ip))

    def getTotalBanHours(this, playerName):
        Cursor.execute("select BanHours from Users where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return 0

    def voteBanPopulaire(this, playerName, playerVoted, ip):
        player = this.players.get(playerName)
        if player != None and player.privLevel == 1 and not ip in player.voteBan:
            player.voteBan.append(ip)
            if len(player.voteBan) == 10:
                this.banPlayer(playerName, 1, "Vote Populaire", "Server", False)
            this.sendStaffMessage(7, "The player <V>%s</V> is voting against <V>%s</V> [<R>%s</R>/10]" %(playerVoted, playerName, len(player.voteBan)))

    def muteUser(this, playerName, mutetime, reason):
        this.userMuteCache.append(playerName)
        Cursor.execute("insert into UserTempMute values (%s, %s, %s)", [playerName, str(Utils.getTime() + (mutetime * 60 * 60)), reason])

    def removeModMute(this, playerName):
        if playerName in this.userMuteCache:
            this.userMuteCache.remove(playerName)
        Cursor.execute("delete from UserTempMute where Username = %s", [playerName])

    def getModMuteInfo(this, playerName):
        Cursor.execute("select Reason, Time from UserTempMute where Username = %s", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return [rs[0], rs[1]]
        else:
            return ["Without a reason", 0]

    def mutePlayer(this, playerName, hours, reason, modName):
        player = this.players.get(playerName)
        if player != None:
            player.sendServerMessageAdmin("<V>%s<BL> ha muteado a <V>%s<BL> por <V>%s <V>%s<BL> Razón: %s" %(modName, playerName, hours, "hora" if hours == 1 else "horas", reason))
            if playerName in this.userMuteCache:
                this.removeModMute(playerName)
   
            player.isMute = True
            player.sendModMute(playerName, hours, reason, False)
            player.sendModMute(playerName, hours, reason, True)
            #this.muteUser(playerName, hours, reason)
            this.muteUser(playerName, hours, reason)
            this.saveCasier(playerName,"MUTE",modName,hours,reason)
            this.modoPwetIslem(playerName,hours,reason,modName,"mute")
    
    def modoPwetIslem(this,playerName,hours,reason,modName,islem):
        if this.reports.has_key(playerName):
            r = this.reports[playerName]
            d = "banned" if islem=="ban" else "muted"
            if islem == "mute":
                r["isMuted"] = True
                r["muteHours"] = int(hours)
                r["muteReason"] = reason
                r["mutedBy"] = modName
            elif islem == "ban":
                r["status"] = "banned"
                r["bannedby"] = modName
                r["banhours"] = hours
                r["banreason"] = reason
            for isim in r["reporters"]:  
                oyuncu = this.players.get(isim) 
                if oyuncu:
                    oyuncu.playerKarma += 1
                    oyuncu.sendMessage(playerName+" has been "+d+". Karma +1 ("+str(oyuncu.playerKarma)+")")
            for player in this.players.values():
                if player.isModoPwet:
                    player.modoPwet.openModoPwet(True)
    
    def saveCasier(this,playerName,state,bannedby,time,reason=""):
        suan = Utils.getTime()       
        Cursor.execute("insert into bmlog values (%s,%s,%s,%s,%s,%s)", [playerName,state,suan,bannedby,time,reason]) 

    def desmutePlayer(this, playerName, modName):
        player = this.players.get(playerName)
        if player != None:
            this.sendStaffMessage(5, "[MUTE] %s remove mute. %s." %(modName, playerName))
            this.removeModMute(playerName)
            player.isMute = False

    def sendStaffChat(this, type, langue, identifiers, packet):
        minLevel = 0 if type == -1 or type == 0 else 1 if type == 1 else 7 if type == 3 or type == 4 else 5 if type == 2 or type == 5 else 6 if type == 7 or type == 6 else 3 if type == 8 else 4 if type == 9 else 10 if type == 10 else 0
        for client in this.players.values():
            if client.privLevel >= minLevel and client.langue == langue or type == 1 or type == 4 or type == 5:
                client.sendPacket(identifiers, packet)

                    
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
                return player.Skills.getShamanBadge()
        return 0

    def getTribeHouse(this, tribeName):
        Cursor.execute("select House from Tribe where Name = %s", [tribeName])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return -1

    def getPlayerID(this, playerName):
        if playerName.startswith("*"):
            return 0
        elif this.players.has_key(playerName):
            return this.players[playerName].playerID
        else:
            Cursor.execute("select PlayerID from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def getPlayerPrivlevel(this, playerName):
        if playerName.startswith("*"):
            return 0
        elif this.players.has_key(playerName):
            return this.players[playerName].privLevel
        else:
            Cursor.execute("select PrivLevel from Users where Username = %s", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return 0

    def getPlayerName(this, playerID):
        Cursor.execute("select Username from Users where PlayerID = %s", [playerID])
        rs = Cursor.fetchone()
        if rs:
            return rs[0]
        else:
            return ""

    def getPlayerRoomName(this, playerName):
        if this.players.has_key(playerName):
            return this.players[playerName].roomName
        else:
            return ""

    def getPlayersCountMode(this, mode, langue):
        modeName = {1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 18: "", 16: "village"}[mode]
        playerCount = 0
        for room in this.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor or room.isOldSurvivor if mode == 8 else room.isRacing or room.isSpeedRace or room.isMeepRace if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante or room.isBigdefilante if mode == 10 else room.isVillage if mode == 16 else True) and (room.community == langue.lower() or langue == "all")):
                playerCount += room.getPlayerCount()
        return ["%s %s" %(this.miceName, modeName), playerCount]

    def parsePromotions(this):
        needUpdate = False
        i = 0
        while i < len(this.promotions):
            item = this.promotions[i]                
            if item[3] < 1000:
                item[3] = Utils.getTime() + item[3] * 86400 + 30
                needUpdate = True
            
            this.shopPromotions.append([item[0], item[1], item[2], item[3]])
            i += 1

        if needUpdate:
            with open("./extra/promotions.json", "w") as f:
                json.dump(this.promotions, f)
        
        this.checkPromotionsEnd()

    def checkPromotionsEnd(this):
        needUpdate = False
        for promotion in this.shopPromotions:
            if Utils.getHoursDiff(promotion[3]) <= 0:
                this.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(this.promotions):
                    if this.promotions[i][0] == promotion[0] and this.promotions[i][1] == promotion[1]:
                        del this.promotions[i]
                    i += 1

        if needUpdate:
            with open("./extra/promotions.json", "w") as f:
                json.dump(this.promotions, f)

    def sendWholeServer(this, identifiers, result):
        for player in this.players.values():
            player.sendPacket(identifiers, result)

    def checkMessage(this, client, message):
        list = client.listanegra
        i = 0
        while i < len(list):
            if re.search("[^a-zA-Z]*".join(list[i]), message.lower()):
                this.sendStaffMessage(7, "[<V>"+client.roomName+"<BL>] <font color='#1EC9B5'>"+client.playerName+"</font> <BL>ha dicho un mensaje de la <V>BlackList<BL>: <BL>[ <font color='#D8D931'>"+str(message)+"</font><BL> ].")
                this.mutePlayer(client.playerName, 3, "SPAM.", "Rabot")
                return True
            i += 1

        return False

    def setVip(this, playerName, days):
        player = this.players.get(playerName)
        if ((player != None and player.privLevel == 1) or this.getPlayerPrivlevel(playerName) == 1):
            Cursor.execute("update users set viptime = %s where Username = %s" if player != None else "update users SET viptime = %s, PrivLevel = 2 where Username = %s", [Utils.getTime() + (days * 24 * 3600), playerName])
            if player != None:
                player.privLevel = 2

            this.sendStaffMessage(7, "<V>"+playerName+"</V> se ha convertido en VIP por <V>"+str(days)+"</V> días.")
            return True
        
        return False
        
    def buyVIP(this, playerName, days):
        player = this.players.get(playerName)
        if ((player != None and player.privLevel == 1) or this.getPlayerPrivlevel(playerName) == 1):
            Cursor.execute("update users set viptime = %s where Username = %s" if player != None else "update users SET viptime = %s, PrivLevel = 2 where Username = %s", [Utils.getTime() + (days * 24 * 3600), playerName])
            if player != None:
                player.privLevel = 2

            this.sendStaffMessage(7, "<V>"+playerName+"</V> ha comprado VIP por <V>"+str(days)+"</V> días.")
            return True
        
        return False

    def getPlayerCode(this, playerName):
        player = this.players.get(Utils.parsePlayerName(playerName))
        return player.playerCode if player != None else 0

    def sendStaffMessage(this, minLevel, message, tab=False,ModoPwet=False):
        for player in this.players.values():
            if str(type(minLevel)) == "<type 'int'>" and player.privLevel >= minLevel:
                if ModoPwet:
                    if player.isModoPwetNotifications:
                        player.sendMessage(message, tab)
                else:
                    player.sendMessage(message, tab)
            elif minLevel == "admin" and player.playerName in ["Fabri"]:
                player.sendMessage(message, tab)
                
    def sendGlobalMessage(this, message):
        this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF(message).toByteArray())

    def getRanking(this):
        this.rankingTimer = reactor.callLater(300, this.getRanking)
        this.rankingsList = [{}, {}, {}, {}, {}]

        Cursor.execute("select Username, FirstCount from Users where PrivLevel < 3 order by FirstCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            this.rankingsList[0][count] = [playerName, this.players[playerName].firstCount if this.checkConnectedAccount(playerName) else rs[1]]
            count += 1
        
        Cursor.execute("select Username, CheeseCount from Users where PrivLevel < 3 order by CheeseCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            this.rankingsList[1][count] = [playerName, this.players[playerName].cheeseCount if this.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, ShamanSaves from Users where PrivLevel < 3 order by ShamanSaves desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            this.rankingsList[2][count] = [playerName, this.players[playerName].shamanSaves if this.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, BootcampCount from Users where PrivLevel < 3 order by BootcampCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            this.rankingsList[3][count] = [playerName, this.players[playerName].bootcampCount if this.checkConnectedAccount(playerName) else rs[1]]
            count += 1

        Cursor.execute("select Username, Coins from Users where PrivLevel < 3 order by Coins desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs[0]
            this.rankingsList[4][count] = [playerName, this.players[playerName].nowCoins if this.checkConnectedAccount(playerName) else rs[1]]
            count += 1

class Room:
    def __init__(this, server, name):

        # String
        this.mapXML = ""
        this.mapName = ""
        this.EMapXML = ""
        this.roomPassword = ""
        this.forceNextMap = "-1"
        this.currentSyncName = ""
        this.currentShamanName = ""
        this.currentSecondShamanName = ""

        # Integer
        this.addTime = 0
        this.mapCode = -1
        this.cloudID = -1
        this.EMapCode = 0
        this.objectID = 0
        this.redCount = 0
        this.mapPerma = -1
        this.blueCount = 0
        this.musicTime = 0
        this.mapStatus = -1
        this.mapNoVotes = 0
        this.currentMap = 0
        this.receivedNo = 0
        this.EMapLoaded = 0
        this.roundTime = 120
        this.mapYesVotes = 0
        this.receivedYes = 0
        this.roundsCount = -1
        this.maxPlayers = 200
        this.numCompleted = 0
        this.numGetCheese = 0
        this.companionBox = -1
        this.gameStartTime = 0
        this.lastRoundCode = 0
        this.FSnumCompleted = 0
        this.SSnumCompleted = 0
        this.musicSkipVotes = 0
        this.forceNextShaman = -1
        this.currentSyncCode = -1
        this.changeMapAttemps = 0
        this.currentShamanCode = -1
        this.currentShamanType = -1
        this.mulodromeRoundCount = 0
        this.gameStartTimeMillis = 0
        this.currentSecondShamanCode = -1
        this.currentSecondShamanType = -1

        # Bool
        this.isMusic = False
        this.isClosed = False
        this.noShaman = False
        this.isEditor = False
        this.isRacing = False
        this.isSnowing = False
        this.isVillage = False
        this.isVanilla = False
        this.is801Room = False
        this.countStats = True
        this.isFixedMap = False
        this.isNormRoom = False
        this.isTutorial = False
        this.isBootcamp = False
        this.isSurvivor = False
        this.isOldSurvivor = False
        this.isVotingBox = False
        this.autoRespawn = False
        this.noAutoScore = False
        this.isDoubleMap = False
        this.specificMap = False
        this.mapInverted = False
        this.isDefilante = False
        this.isBigdefilante = False
        this.isMulodrome = False
        this.canChangeMap = True
        this.isVotingMode = False
        this.isTribeHouse = False
        this.isNoShamanMap = False
        this.EMapValidated = False
        this.isTotemEditor = False
        this.canChangeMusic = True
        this.initVotingMode = True
        this.disableAfkKill = False
        this.isPlayingMusic = False
        this.noShamanSkills = False
        this.never20secTimer = False
        this.isTribeHouseMap = False
        this.changed20secTimer = False
        this.catchTheCheeseMap = False
        this.isDeathmatch = False
        this.canCannon = False
        this.isUtility = False
        this.discoRoom = False
        this.isSpeedRace = False
        this.isFFARace = False
        this.isMeepRace = False
        this.isEvent = False
        this.isPositioncmd = False
        this.isFuncorp = False
        this.isFly = False
        this.isFlyMod = False

        # Bool
        this.killAfkTimer = None
        this.endSnowTimer = None
        this.changeMapTimer = None
        this.voteCloseTimer = None
        this.startTimerLeft = None
        this.autoRespawnTimer = None
        this.contagemDeath = None

        # List Arguments
        this.anchors = []
        this.redTeam = []
        this.blueTeam = []
        this.roomTimers = []
        this.musicVideos = []
        this.lastHandymouse = [-1, -1]
        this.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.mapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.adminsRoom = []
        this.playersBan = []
        
        # Dict
        this.clients = {}
        this.currentTimers = {}
        this.currentShamanSkills = {}
        this.currentSecondShamanSkills = {}

        # Others
        this.name = name
        this.server = server
        this.CursorMaps = CursorMaps

        if this.name.startswith("*"):
            this.community = "xx"
            this.roomName = this.name
        else:
            this.community = this.name.split("-")[0].lower()
            this.roomName = this.name.split("-")[1]

        roomNameCheck = this.roomName[1:] if this.roomName.startswith("*") else this.roomName
        if this.roomName.startswith("\x03[Editeur] "):
            this.countStats = False
            this.isEditor = True
            this.never20secTimer = True

        elif this.roomName.startswith("\x03[Tutorial] "):
            this.countStats = False
            this.currentMap = 900
            this.specificMap = True
            this.noShaman = True
            this.never20secTimer = True
            this.isTutorial = True

        elif this.roomName.startswith("\x03[Totem] "):
            this.countStats = False
            this.specificMap = True
            this.currentMap = 444
            this.isTotemEditor = True
            this.never20secTimer = True

        elif this.roomName.startswith("*\x03"):
            this.countStats = False
            this.isTribeHouse = True
            this.autoRespawn = True
            this.never20secTimer = True
            this.noShaman = True
            this.disableAfkKill = True
            this.isFixedMap = True
            this.roundTime = 0

        elif roomNameCheck.startswith("music"):
            this.isMusic = True

        elif roomNameCheck.startswith("racing"):
            this.isRacing = True
            this.noShaman = True
            this.noAutoScore = False
            this.never20secTimer = True
            this.roundTime = 63

        elif roomNameCheck.startswith("bootcamp"):
            this.isBootcamp = True
            this.countStats = False
            this.roundTime = 360
            this.never20secTimer = True
            this.autoRespawn = True
            this.noShaman = True

        elif roomNameCheck.startswith("vanilla"):
            this.isVanilla = True

        elif roomNameCheck.startswith("survivor"):
            this.isSurvivor = True
            this.roundTime = 90

        elif roomNameCheck.startswith("#bigdefilante"):
            this.isBigdefilante = True
            this.noShaman = True
            this.noAutoScore = False
   
        elif roomNameCheck.startswith("#fly"):
            this.isFlyMod = True
            this.isVanilla = True
            this.roundTime = 120
            this.noShaman = True
            
        elif this.roomName.startswith("#meepracing"):
            this.isMeepRace = True
            this.roundTime = 63
            this.noShaman = True

        elif this.roomName.startswith("#fastracing"):
            this.isSpeedRace = True
            this.roundTime = 63
            this.noShaman = True

        elif this.roomName.startswith("#ffarace"):
            this.isFFARace = True
            this.roundTime = 63
            this.noShaman = True
            
        elif this.roomName.startswith("#deathmatch"):
            this.isDeathmatch = True
            this.roundTime = 90
            this.noShaman = True            

        elif this.roomName.startswith("#utility"):
            this.isUtility = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True
            this.disableAfkKill = True
            

        elif roomNameCheck.startswith("defilante"):
            this.isDefilante = True
            this.noShaman = True
            this.countStats = False
            this.noAutoScore = False

        elif roomNameCheck.startswith("801") or roomNameCheck.startswith("village"):
            if roomNameCheck.startswith("village"):
                this.isVillage = True
            else:
                this.is801Room = True
            this.roundTime = 2700
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True
            this.disableAfkKill = True
        else:
            this.isNormRoom = True
        this.mapChange()

    def addTextPopUpStaff(this, id, type, text, targetPlayer, x, y, width):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeByte(4)
        if targetPlayer == '':
            this.sendAll([29, 23], p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([29, 23], p.toByteArray())
        return

    def startTimer(this):
        for player in this.clients.values():
            player.sendMapStartTimer(False)

    def mapChange(this):
        if this.changeMapTimer != None: this.changeMapTimer.cancel()
        for client in this.clients.values(): client.activeArtefact = 0

        for room in this.server.rooms.values():
            for playerCode, client in room.clients.items():
                if this.isDeathmatch:
                    if not this.contagemDeath is None:
                        this.contagemDeath.cancel()
        
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
                for player in this.clients.values():
                    player.sendPacket(Identifiers.old.send.Vote_Box, [this.mapName, this.mapYesVotes, this.mapNoVotes])
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
                CursorMaps.execute("update Maps set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?" if isDel else "update Maps set YesVotes = ?, NoVotes = ? where Code = ?", [TotalYes, TotalNo, this.mapCode])
                this.isVotingMode = False
                this.receivedNo = 0
                this.receivedYes = 0
                for player in this.clients.values():
                    player.qualifiedVoted = False
                    player.isVoted = False

            this.initVotingMode = True
            this.lastRoundCode = (this.lastRoundCode + 1) % 127

            if this.isSurvivor:
                for player in this.clients.values():
                    if not player.isDead and (not player.isVampire if this.mapStatus == 0 else not player.isShaman):
                        if not this.noAutoScore: player.playerScore += 10

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
                        player.Skills.earnExp(True, numCom)

                player2 = this.clients.get(this.currentSecondShamanName)
                if player2 != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentSecondShamanName, numCom2])
                    if not this.noAutoScore: player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.Skills.earnExp(True, numCom2)

            if this.getPlayerCount() >= this.server.needToFirst:
                this.giveSurvivorStats() if this.isSurvivor else this.giveRacingStats() if this.isSpeedRace or this.isRacing else None

            this.currentSyncCode = -1
            this.currentShamanCode = -1
            this.currentShamanType = -1
            this.currentSecondShamanCode = -1
            this.currentSecondShamanType = -1

            this.currentSyncName = ""
            this.currentShamanName = ""
            this.currentSecondShamanName = ""
            
            this.currentShamanSkills = {}
            this.currentSecondShamanSkills = {}
            
            this.changed20secTimer = False
            this.isDoubleMap = False
            this.isNoShamanMap = False
            this.FSnumCompleted = 0
            this.SSnumCompleted = 0
            this.objectID = 0
            this.numGetCheese = 0
            this.addTime = 0
            this.cloudID = -1
            this.companionBox = -1
            this.lastHandymouse = [-1, -1]
            this.isTribeHouseMap = False
            this.canChangeMusic = True
            this.canChangeMap = True
            this.changeMapAttemps = 0
            
            this.getSyncCode()
            this.anchors = []
            this.mapStatus = (this.mapStatus + 1) % 10

            this.numCompleted = 0
                
            this.currentMap = this.selectMap()
            this.checkMapXML()
            

            if this.currentMap in [range(44, 54), range(138, 144)] or this.mapPerma == 8 and this.getPlayerCount() >= 3:
                this.isDoubleMap = True

            if this.mapPerma in [7, 17, 42] or (this.isSurvivor and this.mapStatus == 0):
                this.isNoShamanMap = True

            if this.currentMap in range(108, 114):
                this.catchTheCheeseMap = True

            this.gameStartTime = Utils.getTime()
            this.gameStartTimeMillis = time.time()

            for player in this.clients.values():
                player.resetPlay()

            for player in this.clients.values():
                player.startPlay()

                if player.isHidden:
                    player.sendPlayerDisconnect()

            if this.isSpeedRace:
                CursorMaps.execute('select Time,Player from Maps where code = ?', [this.mapCode])
                rs = CursorMaps.fetchone()
                if rs[0] > 0:
                    if rs[0] > 100:
                        t = rs[0] / 100.0
                    else:
                        t = rs[0] / 10.0
                    for player in this.clients.values():
                        if player.langueID >= 0 and not player.langueID == 3 and not player.langueID == 6:
                            player.sendMessage("<n>Best record by <J>"+str(rs[1])+"</J> <n>with second</n> (<v>"+str(t)+"</v>s)")
                        if player.langueID == 3:
                            player.sendMessage("[<J>#</J>] <N>O recorde deste mapa foi batido por</N> <J>"+str(rs[1])+"</J>(<V>"+str(t)+"</V>s)") 
                        if player.langueID == 6:
                            player.sendMessage("[<J>#</J>] <bl>En iyi rekor <J>"+str(rs[1])+"</J> <bl>tarafından (<v>"+str(t)+"</v>s) saniyede kırıldı")
                else:
                        for player in this.clients.values():
                            if player.langueID >= 0 and not player.langueID == 3 and not player.langueID == 6:
                                player.sendMessage("<R>(@%s)</R> <n>map has not broken record</n>"% (this.mapCode))
                            if player.langueID == 3:
                                player.sendMessage("[<J>#</J>] <R>(@%s)</R> <N>não há registro quebrado no mapa." %(this.mapCode))
                            if player.langueID == 6:
                                player.sendMessage("<R>(@%s)</R> <bl>haritada kırılan bir rekor yok</font>" %(this.mapCode))

            if this.isBigdefilante:
                CursorMaps.execute('select BDTime,BDTimeNick from Maps where code = ?', [this.mapCode])
                rs = CursorMaps.fetchone()
                if rs[0] > 0:
                    if rs[0] > 100:
                        t = rs[0] / 100.0
                    else:
                        t = rs[0] / 10.0
                    for player in this.clients.values():
                        player.sendMessage("[<J>#</J>] <J>"+str(rs[1])+"</J> <N>quebrado por segundo (<J>"+ str(t) +"</J><R>s</R>)")
                else:
                    for player in this.clients.values():
                        player.sendMessage("[<J>#</J>] </font> <N>(<R>@"+str(this.mapCode)+"</R>) não há record quebrados neste mapa.</N>")

           
           # if this.getPlayerCount() >= this.server.needToFirst:
                   #if not this.isEditor and not this.isVillage and not this.isTribeHouse and not this.isSurvivor and not this.isMusic:
                      # for player in this.clients.values():
                            #player.sendPacket([5, 51], ByteArray().writeByte(52).writeByte(1).writeShort(1).writeShort(random.randint(0, 30)).writeShort(-100).toByteArray())
                           # player.sendPacket([100, 101], "\x01\x01")



            if player in this.clients.values():
                if player.pet != 0:
                    if Utils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        this.sendAll(Identifiers.send.Pet, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.pet).toByteArray())

            if this.isSurvivor and this.mapStatus == 0:
                reactor.callLater(5, this.sendVampireMode)

            if this.isMulodrome:
                this.mulodromeRoundCount += 1
                this.sendMulodromeRound()

                if this.mulodromeRoundCount <= 10:
                    for player in this.clients.values():
                        if player.playerName in this.blueTeam:
                            this.setNameColor(player.playerName, 0x979EFF)
                        elif player.playerName in this.redTeam:
                            this.setNameColor(player.playerName, 0xFF9396)
                else:
                    this.sendAll(Identifiers.send.Mulodrome_End)

            if this.isDeathmatch:
               this.canCannon = False
               for client in this.clients.values():
                  reactor.callLater(3, client.sendContagem)

            if this.isRacing or this.isDefilante or this.isSpeedRace or this.isMeepRace:
                this.roundsCount = (this.roundsCount + 1) % 10
                player = this.clients.get(this.getHighestScore())
                this.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(this.roundsCount).writeInt(player.playerCode if player != None else 0).toByteArray())
                if this.roundsCount == 9:
                    for client in this.clients.values():
                        client.playerScore = 0
                        
            this.startTimerLeft = reactor.callLater(3, this.startTimer)
            if not this.isFixedMap and not this.isTribeHouse and not this.isTribeHouseMap:
                this.changeMapTimer = reactor.callLater(this.roundTime + this.addTime, this.mapChange)
            
            this.killAfkTimer = reactor.callLater(30, this.killAfk)
            if this.autoRespawn or this.isTribeHouseMap:
                this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)

    def getPlayerCount(this):
        return len(filter(lambda player: not player.isHidden, this.clients.values()))

    def getPlayerCountUnique(this):
        ipList = []
        for player in this.clients.values():
            if not player.ipAddress in ipList:
                ipList.append(player.ipAddress)
        return len(ipList)

    def getPlayerList(this):
        result = []
        for player in this.clients.values():
            if not player.isHidden:
                result.append(player.getPlayerData())
        return result

    def addClient(this, player, newRoom=False):
        this.clients[player.playerName] = player

        player.room = this
        if not newRoom:
            player.isDead = True
            this.sendAllOthers(player, [144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())
            player.startPlay()

    def removeClient(this, player):
        if player.playerName in this.clients:
            del this.clients[player.playerName]
            player.resetPlay()
            player.isDead = True
            player.playerScore = 0
            player.sendPlayerDisconnect()

            if this.isMulodrome:
                if player.playerName in this.redTeam: this.redTeam.remove(player.playerName)
                if player.playerName in this.blueTeam: this.blueTeam.remove(player.playerName)

                if len(this.redTeam) == 0 and len(this.blueTeam) == 0:
                    this.mulodromeRoundCount = 10
                    this.sendMulodromeRound()

            if len(this.clients) == 0:
                for timer in [this.autoRespawnTimer, this.changeMapTimer, this.endSnowTimer, this.killAfkTimer, this.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()
                        
                del this.server.rooms[this.name]
            else:
                if player.playerCode == this.currentSyncCode:
                    this.currentSyncCode = -1
                    this.currentSyncName = ""
                    this.getSyncCode()
                this.checkChangeMap()

    def checkChangeMap(this):
        if (not (this.isBootcamp or this.autoRespawn or this.isTribeHouse and this.isTribeHouseMap or this.isFixedMap)):
            alivePeople = filter(lambda player: not player.isDead, this.clients.values())
            if not alivePeople:
                this.mapChange()

    def sendMessage(this, message1, message2, AP, *args):
        for player in this.clients.values():
            if player.playerName != AP:
                player.sendLangueMessage(message1, message2, *args)

    def sendAll(this, identifiers, packet=""):
        for player in this.clients.values():
            player.sendPacket(identifiers, packet)

    def sendAllOthers(this, senderClient, identifiers, packet=""):
        for player in this.clients.values():
            if not player == senderClient:
                player.sendPacket(identifiers, packet)
                
    def sendAllChat(this, playerCode, playerName, message, langueID, isOnly, renk):
        if renk:
            message = '<font color="%s">%s</font>' % (renk, message)
        p = ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(langueID).writeUTF(message)
        if not isOnly:
            for client in this.clients.values():
                client.sendPacket(Identifiers.send.Chat_Message, p.toByteArray())
        else:
            client = this.clients.get(playerName)
            if client != None:
                client.sendPacket(Identifiers.send.Chat_Message, p.toByteArray())
#            this.server.sendStaffMessage(7, "[<V>SPAM</V>][<V>" + client.roomName + "</V>][<T>" + client.playerName + "</T>] sent a link in the message: [<J>" + str(message) + "</J>].")

    def getSyncCode(this):
        if this.getPlayerCount() > 0:
            if this.currentSyncCode == -1:
                player = random.choice(this.clients.values())
                this.currentSyncCode = player.playerCode
                this.currentSyncName = player.playerName
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
            if this.isEditor:
                return this.EMapCode

            elif this.isTribeHouse:
                tribeName = this.roomName[2:]
                runMap = this.server.getTribeHouse(tribeName)

                if runMap == 0:
                    this.mapCode = 0
                    this.mapName = "@NiceMice"
                    this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    this.mapYesVotes = 0
                    this.mapNoVotes = 0
                    this.mapPerma = 22
                    this.mapInverted = False
                else:
                    run = this.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        this.mapCode = 0
                        this.mapName = "@NiceMice"
                        this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        this.mapYesVotes = 0
                        this.mapNoVotes = 0
                        this.mapPerma = 22
                        this.mapInverted = False

            elif this.is801Room:
                return 1234567890
            elif this.isVillage:
                return 801

            elif this.isVanilla:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                map = random.choice(this.mapList)
                while map == this.currentMap:
                    map = random.choice(this.mapList)
                return map
                
            else:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                return this.selectMapStatus()
        return -1

    def selectMapStatus(this):
        maps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]
        selectPerma = (17 if this.mapStatus % 2 == 0 else 17) if this.isRacing or this.isFFARace or this.isMeepRace or this.isSpeedRace else (13 if this.mapStatus % 2 == 0 else 3) if this.isBootcamp else 18 if this.isDefilante else 18 if this.isBigdefilante else (11 if this.mapStatus == 0 else 10) if this.isSurvivor else 10 if this.isOldSurvivor else 19 if this.isMusic and this.mapStatus % 2 == 0 else 41 if this.isDeathmatch else 45 if this.isUtility else 0
        isMultiple = False

        if this.isNormRoom:
            if this.mapStatus < len(maps) and maps[this.mapStatus] != -1:
                isMultiple = maps[this.mapStatus] == 0
                selectPerma = maps[this.mapStatus]
            else:
                map = random.choice(this.mapList)
                while map == this.currentMap:
                    map = random.choice(this.mapList)
                return map

        elif this.isVanilla or (this.isMusic and this.mapStatus % 2 != 0):
            map = random.choice(this.mapList)
            while map == this.currentMap:
                map = random.choice(this.mapList)
            return map

        CursorMaps.execute("select * from Maps where Code != "+ str(this.currentMap) +" and Perma = 1 order by random() limit 1" if isMultiple else "select * from Maps where Code != "+ str(this.currentMap) + " and Perma = "+ str(selectPerma) +" order by random() limit 1")
        rs = CursorMaps.fetchone()
        if rs:
           this.mapCode = rs["Code"]
           this.mapName = rs["Name"]
           this.mapXML = rs["XML"]
           this.mapYesVotes = rs["YesVotes"]
           this.mapNoVotes = rs["NoVotes"]
           this.mapPerma = rs["Perma"]
           this.mapInverted = random.randint(0, 100) > 85
        else:
           map = random.choice(this.mapList)
           while map == this.currentMap:
               map = random.choice(this.mapList)
           return map
            
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
            CursorMaps.execute("select Code from Maps where Perma = ?", [int(str(code))])
            for rs in CursorMaps.fetchall():
                mapList.append(rs["Code"])

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
        CursorMaps.execute("select Name, XML, YesVotes, NoVotes, Perma from Maps where Code = ?", [mapCode])
        rs = CursorMaps.fetchone()
        if rs:
            mapInfo = rs["Name"], rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]
        return mapInfo

    def checkIfDeathMouse(this):
        return len(filter(lambda player: not player.isDead, this.clients.values())) <= 1

    def checkIfTooFewRemaining(this):
        return len(filter(lambda player: not player.isDead, this.clients.values())) <= 2

    def getAliveCount(this):
        return len(filter(lambda player: not player.isDead, this.clients.values()))

    def getDeathCountNoShaman(this):
        return len(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, this.clients.values()))

    def getHighestScore(this):
        playerScores = []
        playerID = 0
        for player in this.clients.values():
            playerScores.append(player.playerScore)
                    
        for player in this.clients.values():
            if player.playerScore == max(playerScores):
                playerID = player.playerCode
        return playerID

    def getSecondHighestScore(this):
        playerScores = []
        playerID = 0
        for player in this.clients.values():
            playerScores.append(player.playerScore)
        playerScores.remove(max(playerScores))

        if len(playerScores) >= 1:
            for player in this.clients.values():
                if player.playerScore == max(playerScores):
                    playerID = player.playerCode
        return playerID

    def getShamanCode(this):
        if this.currentShamanCode == -1:
            if this.currentMap in this.noShamanMaps or this.isNoShamanMap or this.noShaman:
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
                for player in this.clients.values():
                    if player.playerCode == this.currentShamanCode:
                        this.currentShamanName = player.playerName
                        this.currentShamanType = player.shamanType
                        this.currentShamanSkills = player.playerSkills
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
                tempClient = random.choice(this.clients.values())
                this.currentSecondShamanCode = tempClient.playerCode

            for player in this.clients.values():
                if player.playerCode == this.currentShamanCode:
                    this.currentShamanName = player.playerName
                    this.currentShamanType = player.shamanType
                    this.currentShamanSkills = player.playerSkills
                    break

                if player.playerCode == this.currentSecondShamanCode:
                    this.currentSecondShamanName = player.playerName
                    this.currentSecondShamanType = player.shamanType
                    this.currentSecondShamanSkills = player.playerSkills
                    break

        return [this.currentShamanCode, this.currentSecondShamanCode]

    def closeVoting(this):
        this.initVotingMode = False
        this.isVotingBox = False
        if this.voteCloseTimer != None: this.voteCloseTimer.cancel()
        this.mapChange()

    def killShaman(this):
        for player in this.clients.values():
            if player.playerCode == this.currentShamanCode:
                player.isDead = True
                player.sendPlayerDied()
        this.checkChangeMap()

    def killAfk(this):
        if this.isEditor or this.isTotemEditor or this.isBootcamp or this.isTribeHouseMap or this.disableAfkKill:
            return
            
        if ((Utils.getTime() - this.gameStartTime) < 32 and (Utils.getTime() - this.gameStartTime) > 28):
            for player in this.clients.values():
                if not player.isDead and player.isAfk:
                    player.isDead = True
                    if not this.noAutoScore: player.playerScore += 1
                    player.sendPlayerDied()
            this.checkChangeMap()

    def checkIfDoubleShamansAreDead(this):
        player1 = this.clients.get(this.currentShamanName)
        player2 = this.clients.get(this.currentSecondShamanName)
        return (False if player1 == None else player1.isDead) and (False if player2 == None else player2.isDead)

    def checkIfShamanIsDead(this):
        player = this.clients.get(this.currentShamanName)
        return False if player == None else player.isDead

    def checkIfShamanCanGoIn(this):
        for player in this.clients.values():
            if player.playerCode != this.currentShamanCode and player.playerCode != this.currentSecondShamanCode and not player.isDead:
                return False
        return True

    def giveShamanSave(this, shamanName, type):
        if not this.countStats:
            return

        player = this.clients.get(shamanName)
        if player != None:
            if type == 0:
                player.shamanSaves += 11
            elif type == 1:
                player.hardModeSaves += 11
            elif type == 2:
                player.divineModeSaves += 11
            if player.privLevel != 0:
                counts = [player.shamanSaves, player.hardModeSaves, player.divineModeSaves]
                titles = [this.server.shamanTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if titles[type].has_key(counts[type]):
                    title = titles[type][counts[type]]
                    player.checkAndRebuildTitleList(rebuilds[type])
                    player.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    player.sendCompleteTitleList()
                    player.sendTitleList()

    def respawnMice(this):
        for player in this.clients.values():
            if player.isDead:
                player.isDead = False
                player.playerStartTimeMillis = time.time()
                this.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

        if this.autoRespawn or this.isTribeHouseMap:
            this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)

    def respawnSpecific(this, playerName):
        player = this.clients.get(playerName)
        if player != None and player.isDead:
            player.resetPlay()
            player.isAfk = False
            player.playerStartTimeMillis = time.time()
            this.sendAll([144, 2], ByteArray().writeBytes(player.getPlayerData()).writeBoolean(False).writeBoolean(True).toByteArray())

    def sendMulodromeRound(this):
        this.sendAll(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(this.mulodromeRoundCount).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
        if this.mulodromeRoundCount > 10:
            this.sendAll(Identifiers.send.Mulodrome_End)
            this.sendAll(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if this.blueCount == this.redCount else (1 if this.blueCount < this.redCount else 0)).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
            this.isMulodrome = False
            this.mulodromeRoundCount = 0
            this.redCount = 0
            this.blueCount = 0
            this.redTeam = []
            this.blueTeam = []
            this.isRacing = False
            this.never20secTimer = False
            this.noShaman = False

    def checkMapXML(this):
        if int(this.currentMap) in this.server.vanillaMaps:
            this.mapCode = int(this.currentMap)
            this.mapName = "_Village" if this.mapCode == 801 else "@NiceMice"
            this.mapXML = str(this.server.vanillaMaps[int(this.currentMap)])
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 41
            this.currentMap = -1
            this.mapInverted = False

    def sendVampireMode(this):
        player = this.clients.get(this.currentSyncName)
        if player != None:
            player.sendVampireMode(False)

    def bindKeyBoard(this, playerName, key, down, yes):
        player = this.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())

    def addPhysicObject(this, id, x, y, bodyDef):
        this.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef["dynamic"]) if bodyDef.has_key("dynamic") else False).writeByte(int(bodyDef["type"]) if bodyDef.has_key("type") else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if bodyDef.has_key("width") else 0).writeShort(int(bodyDef["height"]) if bodyDef.has_key("height") else 0).writeBoolean(bool(bodyDef["foreground"]) if bodyDef.has_key("foreground") else False).writeShort(int(bodyDef["friction"]) if bodyDef.has_key("friction") else 0).writeShort(int(bodyDef["restitution"]) if bodyDef.has_key("restitution") else 0).writeShort(int(bodyDef["angle"]) if bodyDef.has_key("angle") else 0).writeBoolean(bodyDef.has_key("color")).writeInt(int(bodyDef["color"]) if bodyDef.has_key("color") else 0).writeBoolean(bool(bodyDef["miceCollision"]) if bodyDef.has_key("miceCollision") else True).writeBoolean(bool(bodyDef["groundCollision"]) if bodyDef.has_key("groundCollision") else True).writeBoolean(bool(bodyDef["fixedRotation"]) if bodyDef.has_key("fixedRotation") else False).writeShort(int(bodyDef["mass"]) if bodyDef.has_key("mass") else 0).writeShort(int(bodyDef["linearDamping"]) if bodyDef.has_key("linearDamping") else 0).writeShort(int(bodyDef["angularDamping"]) if bodyDef.has_key("angularDamping") else 0).writeBoolean(False).writeUTF("").toByteArray())

    def removeObject(this, objectId):
        this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBoolean(True).toByteArray())

    def movePlayer(this, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        player = this.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).toByteArray())

    def setNameColor(this, playerName, color):
        if this.clients.has_key(playerName):
            this.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(this.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def addPopup(this, id, type, text, targetPlayer, x, y, width, fixedPos):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeBoolean(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Popup, p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Popup, p.toByteArray())
    
    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(this, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def bindMouse(this, playerName, yes):
        player = this.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBoolean(yes).toByteArray())
			
    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
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
        packet = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Show_Color_Picker, packet.toByteArray())

    def startSnowSchedule(this, power):
        if this.isSnowing:
            this.startSnow(0, power, False)

    def startSnow(this, millis, power, enabled):
        this.isSnowing = enabled
        this.sendAll(Identifiers.send.Snow, ByteArray().writeBoolean(enabled).writeShort(power).toByteArray())
        if enabled:
            this.endSnowTimer = reactor.callLater(millis, lambda: this.startSnowSchedule(power))

    def giveSurvivorStats(this):
        for player in this.clients.values():
            if not player.isNewPlayer:
                player.survivorStats[0] += 11
                if player.isShaman:
                    player.survivorStats[1] += 11
                    player.survivorStats[2] += this.getDeathCountNoShaman()
                elif not player.isDead:
                    player.survivorStats[3] += 11

                i = 0
                while i < 3:
                    if player.survivorStats[i] >= this.server.statsPlayer["survivorCount"][i] and not this.server.statsPlayer["survivorBadges"][i] in player.shopBadges:
                        player.Shop.sendUnlockedBadge(this.server.statsPlayer["survivorBadges"][i])
                        try: player.shopBadges[this.server.statsPlayer["survivorBadges"][i]] += 1
                        except: player.shopBadges[this.server.statsPlayer["survivorBadges"][i]] = 1
                        player.Shop.checkAndRebuildBadges()
                    i += 1

    def giveRacingStats(this):
        for player in this.clients.values():
            if not player.isNewPlayer:
                player.racingStats[0] += 1
                if player.hasCheese or player.hasEnter:
                    player.racingStats[1] += 1
                if player.hasEnter:
                    if player.currentPlace <= 3:
                        player.racingStats[2] += 11
                    if player.currentPlace == 1:
                        player.racingStats[3] += 11

                i = 0
                while i < 3:
                    if player.racingStats[i] >= this.server.statsPlayer["racingCount"][i] and not this.server.statsPlayer["racingBadges"][i] in player.shopBadges:
                        player.Shop.sendUnlockedBadge(this.server.statsPlayer["racingBadges"][i])
                        try: player.shopBadges[this.server.statsPlayer["racingBadges"][i]] += 1
                        except: player.shopBadges[this.server.statsPlayer["racingBadges"][i]] = 1
                        player.Shop.checkAndRebuildBadges()
                    i += 1

    def send20SecRemainingTimer(this):
        if not this.changed20secTimer:
            if not this.never20secTimer and this.roundTime + (this.gameStartTime - Utils.getTime()) > 21:
                this.changed20secTimer = True
  

    def changeMapTimers(this, seconds):
        if this.changeMapTimer != None: this.changeMapTimer.cancel()
        this.changeMapTimer = reactor.callLater(seconds, this.mapChange)

    def newConsumableTimer(this, code):
        this.roomTimers.append(reactor.callLater(10, lambda: this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBoolean(False).toByteArray())))

if __name__ == "__main__":
    # Connection Settings
    config = ConfigParser.ConfigParser()
    config.read("./extra/configs.properties")

    # MySQL Connection Settings #
    Database, Cursor = None, None
    Database = MySQLdb.connect("localhost","root","","nie")
    Database.isolation_level = None 
    Cursor = Database.cursor()
    Database.autocommit(True)

    # SQLite Maps Connection Settings
    DatabaseMaps, CursorMaps = None, None
    DatabaseMaps = sqlite3.connect("./db/Maps.db", check_same_thread = False)
    DatabaseMaps.text_factory = str
    DatabaseMaps.isolation_level = None
    DatabaseMaps.row_factory = sqlite3.Row
    CursorMaps = DatabaseMaps.cursor()
    
    # Connection Server
    S = Server()
    os.system("title {} Work Line".format(config.get("configGame", "game.miceName")))
    os.system("color f6")
    print("="*60).center(80)
    portList = []
    portBugs = []
    for port in [11801, 12801, 13801, 14801]:
        try:
            reactor.listenTCP(port, S)
            portList.append(port)
        except:
            exit()
    print(str(portList)).center(80)
    print("="*60).center(80)

    print("[%s] %s Server Connected." %(time.strftime("%H:%M:%S"), config.get("configGame", "game.miceName")))
    threading.Thread(target=reactor.run(), args=(False,)).start()
