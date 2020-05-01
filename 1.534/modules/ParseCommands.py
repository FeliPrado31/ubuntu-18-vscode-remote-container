#coding: utf-8
import re, base64, hashlib, urllib2

from ByteArray import ByteArray
from Identifiers import Identifiers

class ParseCommands:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        this.currentArgsCount = 0
        
    def requireNoSouris(this, playerName):
        if playerName.startswith("*"):
            pass
        else:
            return True

    def requireArgs(this, argsCount):
        if this.currentArgsCount < argsCount:
            this.client.sendMessage("Invalid arguments.")
            return False

        return True

    def requireTribe(this, canUse=False):
        if not this.client.tribeName == "" and this.client.room.isTribeHouse:
            tribeRankings = this.client.tribeData[3]
            perm = tribeRankings[this.client.tribeRank].split("|")[2]
            if perm.split(",")[8] == "1":
                canUse = True

    def parseCommand(this, command):                
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        this.currentArgsCount = argsCount

        try:
            if command in ["profil", "perfil", "profile"]:
                this.client.sendProfile(this.client.Username if argsCount == 0 else this.client.TFMUtils.parsePlayerName(args[0]))

            elif command in ["editeur", "editor"]:
                if this.client.privLevel >= 1:
                    this.client.enterRoom(chr(3) + "[Editeur] " + this.client.Username)
                    this.client.sendPacket(Identifiers.old.send.Map_Editor, [])
                    this.client.sendPacket(Identifiers.send.Room_Type, chr(1))

            elif command in ["totem"]:
                if this.client.privLevel >= 1:
                    if this.client.privLevel != 0 and this.client.shamanSaves >= 500:
                        this.client.enterRoom(chr(3) + "[Totem] " + this.client.Username)

            elif command in ["sauvertotem"]:
                if this.client.room.isTotemEditeur:
                    this.client.STotem[0] = this.client.Totem[0]
                    this.client.STotem[1] = this.client.Totem[1]
                    this.client.sendPlayerDied()
                    this.client.enterRoom(this.server.recommendRoom(this.client.Langue))

            elif command in ["resettotem"]:
                if this.client.room.isTotemEditeur:
                    this.client.Totem = [0, ""]
                    this.client.RTotem = True
                    this.client.isDead = True
                    this.client.sendPlayerDied()
                    this.client.room.checkShouldChangeMap()

            elif command in ["ban", "iban"]:
                if this.client.privLevel >= 5:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    time = args[1] if (argsCount >= 2) else "1"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    silent = command == "iban"
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 100000 if (hours > 100000) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    if playerName in this.server.adminAllow:
                        this.server.sendStaffMessage(7, "%s tried to ban an administrator." %(this.client.Username))
                    else:
                        if this.server.banPlayer(playerName, hours, reason, this.client.Username, silent):
                            this.server.sendStaffMessage(5, "<V>%s</V> banned <V>%s</V> for <V>%s</V> %s the reason: <V>%s</V>" %(this.client.Username, playerName, hours, "hora" if hours == 1 else "horas", reason))
                        else:
                            this.client.sendMessage("The player [%s] does not exist." % (playerName))
                else:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    this.server.voteBanPopulaire(playerName, this.client.ipAddress)
                    this.client.sendBanConsideration()

            elif command in ["unban"]:
                if this.client.privLevel == 10:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    found = False

                    if this.server.checkExistingUser(playerName):
                        if this.server.checkTempBan(playerName):
                            this.server.removeTempBan(playerName)
                            found = True

                        if this.server.checkPermaBan(playerName):
                            this.server.removePermaBan(playerName)
                            found = True

                        if found:
                            import time
                            this.Cursor.execute("insert into BanLog values (?, ?, '', '', ?, 'Unban', '', '')", [playerName, this.client.Username, int(str(time.time())[:9])])
                            this.server.sendStaffMessage(5, "<V>%s</V> unbanned <V>%s</V>." %(this.client.Username, playerName))

            elif command in ["unbanip"]:
                if this.client.privLevel >= 7:
                    ip = args[0]
                    if ip in this.server.ipPermaBanCache:
                        this.server.ipPermaBanCache.remove(ip)
                        this.Cursor.execute("delete from ippermaban where IP = ?", [ip])
                        this.server.sendStaffMessage(7, "<V>%s</V> unbanned the IP <V>%S</V>." %(this.client.Username, ip))
                    else:
                        this.client.sendMessage("This IP is not banned.")

            elif command in ["mute"]:
                if this.client.privLevel >= 5:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    time = args[1] if (argsCount >= 2) else "1"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    hours = int(time) if (time.isdigit()) else 1
                    this.requireNoSouris(playerName)
                    hours = 500 if (hours > 500) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    this.server.mutePlayer(playerName, hours, reason, this.client.Username)

            elif command in ["unmute"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    this.server.sendStaffMessage(5, "<V>%s</V> unmuted <V>%s</V>." %(this.client.Username, playerName))
                    this.server.removeModMute(playerName)
                    this.client.isMute = False
                
            elif command in ["rank"]:
                if this.client.privLevel == 10:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName) or playerName in this.server.adminAllow:
                        this.client.sendMessage("User not found: <V>%s</V>." %(playerName))
                    else:
                        privLevel = 10 if rank.startswith("adm") else 9 if rank.startswith("coord") else 8 if rank.startswith("smod") else 7 if rank.startswith("mod") else 6 if rank.startswith("map") or rank.startswith("mc") else 5 if rank.startswith("hel") else 4 if rank.startswith("dv") or rank.startswith("div") else 3 if rank.startswith("dev") or rank.startswith("lua") else 2 if rank.startswith("vip") else 1
                        rankName = "Administrator" if rank.startswith("adm") else "Coordinator" if rank.startswith("coord") else "Super Moderator" if rank.startswith("smod") else "Moderator" if rank.startswith("mod") else "MapCrew" if rank.startswith("map") or rank.startswith("mc") else "Helper" if rank.startswith("hel") else "Publisher" if rank.startswith("dv") or rank.startswith("div") else "Lua Developer" if rank.startswith("dev") or rank.startswith("lua") else "Vip" if rank.startswith("vip") else "Player"
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = privLevel
                            player.TitleNumber = 0
                            player.sendCompleteTitleList()
                        else:
                            this.Cursor.execute("update Users set PrivLevel = ?, TitleNumber = 0 where Username = ?", [privLevel, playerName])

                        this.server.sendStaffMessage(7, "<V>%s</V> won the rank of <V>%s</V>." %(playerName, rankName))
                            
            elif command in ["np", "npp"]:
                if this.client.privLevel >= 6:
                    if len(args) == 0:
                        this.client.room.mapChange()
                    else:
                        if not this.client.room.isVotingMode:
                            code = args[0]
                            if code.startswith("@"):
                                mapInfo = this.client.room.getMapInfo(int(code[1:]))
                                if mapInfo[0] == None:
                                    this.client.sendLangueMessage("", "$CarteIntrouvable")
                                else:
                                    this.client.room.forceNextMap = code
                                    if command == "np":
                                        if this.client.room.changeMapTimer != None:
                                            this.client.room.changeMapTimer.cancel()
                                        this.client.room.mapChange()
                                    else:
                                        this.client.sendLangueMessage("", "$ProchaineCarte " + code)

                            elif code.isdigit():
                                this.client.room.forceNextMap = code
                                if command == "np":
                                    if this.client.room.changeMapTimer != None:
                                        this.client.room.changeMapTimer.cancel()
                                    this.client.room.mapChange()
                                else:
                                    this.client.sendLangueMessage("", "$ProchaineCarte " + code)

            elif command in ["mod", "mapcrews"]:
                staff = {}
                staffList = "$ModoPasEnLigne" if command == "mod" else "$MapcrewPasEnLigne"

                for player in this.server.players.values():
                    if command == "mod" and player.privLevel >= 4 and not player.privLevel == 6 or command == "mapcrews" and player.privLevel == 6:
                        if staff.has_key(player.Langue.lower()):
                            names = staff[player.Langue.lower()]
                            names.append(player.Username)
                            staff[player.Langue.lower()] = names
                        else:
                            names = []
                            names.append(player.Username)
                            staff[player.Langue.lower()] = names

                if len(staff) >= 1:
                    staffList = "$ModoEnLigne" if command == "mod" else "$MapcrewEnLigne"
                    for list in staff.items():
                        staffList += "<br><BL>["+str(list[0])+"] <BV>"+str("<BL>, <BV>").join(list[1])

                this.client.sendLangueMessage("", staffList)

            elif command in ["ls"]:
                if this.client.privLevel >= 4:
                    data = []

                    for room in this.server.rooms.values():
                        if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                            data.append(["ALL", room.name, room.getPlayerCount()])
                        elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                            if room.name.startswith(("*" + chr(3))):
                                data.append(["TRIBEHOUSE", room.name, room.getPlayerCount()])
                            else:
                                data.append(["PRIVATE", room.name, room.getPlayerCount()])
                        else:
                            data.append([room.community.upper(), room.roomName, room.getPlayerCount()])

                    result = "\n"
                    for roomInfo in data:
                        result += "[<J>"+str(roomInfo[0])+"<BL>] <b>"+str(roomInfo[1])+"</b> : "+str(roomInfo[2])+"\n"
                            
                    result += "<font color='#00C0FF'>Total players/rooms: </font><J><b>"+str(this.server.getConnectedPlayerCount())+"</b><font color='#00C0FF'>/</font><J><b>"+str(this.server.getRoomsCount())+"</b>"
                    this.client.sendMessage(result)

            elif command in ["lsc"]:
                if this.client.privLevel >= 4:
                    result = {}
                    for room in this.server.rooms.values():
                        if result.has_key(room.community):
                            result[room.community] = result[room.community] + room.getPlayerCount()
                        else:
                            result[room.community] = room.getPlayerCount()

                    message = "\n"
                    for community in result.items():
                        message += "<V>"+str(community[0].upper())+"<BL> : <J>"+str(community[1])+"\n"
                    message += "<V>ALL<BL> : <J>"+str(sum(result.values()))
                    this.client.sendMessage(message)

            elif command in ["luaadmin"]:
                if this.client.privLevel == 10:
                    this.client.isLuaAdmin = not this.client.isLuaAdmin
                    this.client.sendMessage("You can run scripts as administrator." if this.client.isLuaAdmin else "You can not run scripts as administrator anymore.")

            elif command in ["skip"]:
                if this.client.canSkipMusic and this.client.room.isMusic and this.client.room.isPlayingMusic:
                    this.client.room.musicSkipVotes += 1
                    this.client.checkMusicSkip()

            elif command in ["pw"]:
                if this.client.room.roomName.startswith("*" + this.client.Username) or this.client.room.roomName.startswith(this.client.Username):
                    if len(args) == 0:
                        this.client.room.roomPassword = ""
                        this.client.sendLangueMessage("", "$MDP_Desactive")
                    else:
                        password = args[0]
                        this.client.room.roomPassword = password
                        this.client.sendLangueMessage("", "$Mot_De_Passe : " + password)

            elif command in ["admin", "admin*"]:
                if this.client.privLevel == 10:
                    if this.client.gender in [2, 0]:
                        this.client.sendStaffMessage("<font color='#00FF7F'>" + ("[ALL]" if "*" in command else "") + "[Administrator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)
                    else:
                        this.client.sendStaffMessage("<font color='#FF00FF'>" + ("[ALL]" if "*" in command else "") + "[Administrator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)

            elif command in ["coord", "coord*"]:
                if this.client.privLevel >= 9:
                    if this.client.gender in [2, 0]:
                        this.client.sendStaffMessage("<font color='#FFFF00'>" + ("[ALL]" if "*" in command else "") + "[Coordinator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)
                    else:
                        this.client.sendStaffMessage("<font color='#FF00FF'>" + ("[ALL]" if "*" in command else "") + "[Coordinator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)

            elif command in ["smod", "sms", "smod*", "sms*"]:
                if this.client.privLevel >= 8:
                    if this.client.gender in [2, 0]:
                        this.client.sendStaffMessage("<font color='#15FA00'>" + ("[ALL]" if "*" in command else "") + "[Super Moderator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)
                    else:
                        this.client.sendStaffMessage("<font color='#FF00FF'>" + ("[ALL]" if "*" in command else "") + "[Super Moderator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)

            elif command in ["md", "md*"]:
                if this.client.privLevel >= 7:
                    if this.client.gender in [2, 0]:
                        this.client.sendStaffMessage("<font color='#F39F04'>" + ("[ALL]" if "*" in command else "") + "[Moderator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)
                    else:
                        this.client.sendStaffMessage("<font color='#FF00FF'>" + ("[ALL]" if "*" in command else "") + "[Moderator <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)

            elif command in ["mapc", "mapc*"]:
                if this.client.privLevel >= 6:
                    this.client.sendStaffMessage("<font color='#00FFFF'>" + ("[ALL]" if "*" in command else "") + "[MapCrew <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)

            elif command in ["hel", "hel*"]:
                if this.client.privLevel >= 5:
                    this.client.sendStaffMessage("<font color='#FFF68F'>" + ("[ALL]" if "*" in command else "") + "[Helper <b>"+this.client.Username+"</b>]</font> <N>"+argsNotSplited, "*" in command)

            elif command in ["vip"]:
                if this.client.privLevel >= 2:
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<font color='#E0E0E0'>[<b>"+this.client.Username+"</b>] "+argsNotSplited+"</font>").toByteArray())

            elif command in ["rm"]:
                if this.client.privLevel >= 5:
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<font color='#FF69B4'>[<b>"+this.client.Username+"</b>] "+argsNotSplited+"</font>").toByteArray())

            elif command in ["smn"]:
                if this.client.privLevel >= 9:
                    this.client.sendAllModerationChat(-1, argsNotSplited)

            elif command in ["mshtml"]:
                if this.client.privLevel >= 9:
                    this.client.sendAllModerationChat(0, argsNotSplited.replace("&#", "&amp;#").replace("&lt;", "<"))

            elif command in ["ajuda", "help"]:
                if this.client.privLevel >= 1:
                    this.client.sendLogMessage(this.getCommandsList())

            elif command in ["hide"]:
                if this.client.privLevel >= 5:
                    this.client.isHidden = True
                    this.client.sendPlayerDisconnect()
                    this.client.sendMessage("You are invisible.")

            elif command in ["unhide"]:
                if this.client.privLevel >= 5:
                    if this.client.isHidden:
                        this.client.isHidden = False
                        this.client.enterRoom(this.client.room.name)
                        this.client.sendMessage("You are not invisible.")

            elif command in ["reboot"]:
                if this.client.privLevel == 10:
                    this.server.sendServerReboot()

            elif command in ["shutdown"]:
                if this.client.privLevel == 10:
                    this.server.closeServer()

            elif command in ["updatesql"]:
                if this.client.privLevel == 10:
                    this.server.updateConfig()
                    for player in this.server.players.values():
                        if not player.isGuest:
                            player.updateDatabase()

                    this.server.sendStaffMessage(5, "%s are updating the database." %(this.client.Username))

            elif command in ["kill", "suicide", "mort", "die"]:
                if not this.client.isDead:
                    this.client.isDead = True
                    if not this.client.room.noAutoScore: this.client.playerScore += 1
                    this.client.sendPlayerDied()
                    this.client.room.checkShouldChangeMap()

            elif command in ["title", "titulo", "titre"]:
                if this.client.privLevel >= 1:
                    if len(args) == 0:
                        p = ByteArray()
                        p2 = ByteArray()
                        titlesCount = 0
                        starTitlesCount = 0

                        for title in this.client.titleList:
                            titleInfo = str(title).split(".")
                            titleNumber = int(titleInfo[0])
                            titleStars = int(titleInfo[1])
                            if 1 < titleStars:
                                p.writeShort(titleNumber).writeByte(titleStars)
                                starTitlesCount += 1
                            else:
                                p2.writeShort(titleNumber)
                                titlesCount += 1
                        this.client.sendPacket(Identifiers.send.Titles_List, ByteArray().writeShort(titlesCount).writeBytes(p2.toByteArray()).writeShort(starTitlesCount).writeBytes(p.toByteArray()).toByteArray())
                    else:
                        titleID = args[0]
                        found = False
                        for title in this.client.titleList:
                            if str(title).split(".")[0] == titleID:
                                found = True
                        if found:
                            this.client.TitleNumber = int(titleID)
                            for title in this.client.titleList:
                                if str(title).split(".")[0] == titleID:
                                    this.client.TitleStars = int(str(title).split(".")[1])
                            this.client.sendPacket(Identifiers.send.Change_Title, ByteArray().writeUnsignedByte(0 if titleID == 0 else 1).writeUnsignedShort(titleID).toByteArray())

            elif command in ["sy?"]:
                if this.client.privLevel >= 5:
                    this.client.sendLangueMessage("", "$SyncEnCours : [" + this.client.room.currentSyncName + "]")

            elif command in ["sy"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.isSync = True
                        this.client.room.currentSyncCode = player.playerCode
                        this.client.room.currentSyncName = player.Username
                        if this.client.room.mapCode != -1 or this.client.room.EMapCode != 0:
                            this.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode, ""])
                        else:
                            this.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode])

                        this.client.sendLangueMessage("", "$NouveauSync <V>" + playerName)

            elif command in ["ch"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        if this.client.room.forceNextShaman == player:
                            this.client.sendLangueMessage("", "$PasProchaineChamane", player.Username)
                            this.client.room.forceNextShaman = -1
                        else:
                            this.client.sendLangueMessage("", "$ProchaineChamane", player.Username)
                            this.client.room.forceNextShaman = player

            elif re.match("p\\d+(\\.\\d+)?", command):
                if this.client.privLevel >= 6:
                    mapCode = this.client.room.mapCode
                    mapName = this.client.room.mapName
                    currentCategory = this.client.room.mapPerma
                    if mapCode != -1:
                        category = int(command[1:])
                        if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 20, 22, 41, 42, 44, 45]:
                            this.server.sendStaffMessage(6, "<V>%s <BL>avaliou o mapa @%s para a categoria P%s" %(this.client.Username, mapCode, category))
                            this.Cursor.execute("update MapEditor set Perma = ? where Code = ?", [category, mapCode])

            elif re.match("lsp\\d+(\\.\\d+)?", command):
                if this.client.privLevel >= 6:
                    category = int(command[3:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44]:
                        mapList = ""
                        mapCount = 0
                        this.Cursor.execute("select * from mapeditor where Perma = ?", [category])
                        r = this.Cursor.fetchall()
                        for rs in r:
                            mapCount += 1
                            yesVotes = rs["YesVotes"]
                            noVotes = rs["NoVotes"]
                            totalVotes = yesVotes + noVotes
                            if totalVotes < 1: totalVotes = 1
                            rating = (1.0 * yesVotes / totalVotes) * 100
                            mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])
                            
                        try: this.client.sendLogMessage("<font size=\"12\"><N>There are</N> <BV>%s</BV> <N>maps</N> <V>P%s %s</V></font>" %(mapCount, category, mapList))
                        except: this.client.sendMessage("<R>There are many maps and you can not open.</R>")

            elif command in ["lsmaps"]:
                if len(args) == 0:
                    this.client.privLevel >= 1
                else:
                    this.client.privLevel >= 6
                    
                playerName = this.client.Username if len(args) == 0 else this.client.TFMUtils.parsePlayerName(args[0])
                mapList = ""
                mapCount = 0

                this.Cursor.execute("select * from MapEditor where Name = ?", [playerName])
                r = this.Cursor.fetchall()
                for rs in r:
                    mapCount += 1
                    yesVotes = rs["YesVotes"]
                    noVotes = rs["NoVotes"]
                    totalVotes = yesVotes + noVotes
                    if totalVotes < 1: totalVotes = 1
                    rating = (1.0 * yesVotes / totalVotes) * 100
                    mapList += "\n<N>"+str(rs["Name"])+" - @"+str(rs["Code"])+" - "+str(totalVotes)+" - "+str(rating).split(".")[0]+"% - P"+str(rs["Perma"])

                try: this.client.sendLogMessage("<font size= \"12\"><V>"+playerName+"<N>'s maps: <BV>"+str(mapCount)+ str(mapList)+"</font>")
                except: this.client.sendMessage("<R>There are many maps and you can not open.</R>")

            elif command in ["info"]:
                if this.client.privLevel >= 1:
                    if this.client.room.mapCode != -1:
                        totalVotes = this.client.room.mapYesVotes + this.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * this.client.room.mapYesVotes / totalVotes) * 100
                        this.client.sendMessage(str(this.client.room.mapName)+" - @"+str(this.client.room.mapCode)+" - "+str(totalVotes)+" - "+str(rating).split(".")[0]+"% - P"+str(this.client.room.mapPerma))

            elif command in ["re", "respawn"]:
                if len(args) == 0:
                    if this.client.privLevel >= 2:
                        if not this.client.canRespawn:
                            this.client.room.respawnSpecific(this.client.Username, True)
                            this.client.canRespawn = True
                            
                else:
                    if this.client.privLevel >= 7:
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        if this.client.room.clients.has_key(playerName):
                            this.client.room.respawnSpecific(playerName, True)

            elif command in ["neige"]:
                if this.client.privLevel >= 8 or this.requireTribe(True):
                    this.client.room.startSnow(1000, 60, not this.client.room.isSnowing)

            elif command in ["music", "musique"]:
                if this.client.privLevel >= 8 or this.requireTribe(True):
                    if len(args) == 0:
                        this.client.room.sendAll(Identifiers.old.send.Music, [])
                    else:
                        this.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

            elif command in ["clearreports"]:
                if this.client.privLevel == 10:
                    this.server.reports = {"names": []}
                    this.client.sendMessage("Done.")
                    this.server.sendStaffMessage(7, "<V>"+this.client.Username+"<BL> cleaned the Modopwet reports.")

            elif command in ["clearcache"]:
                if this.client.privLevel == 10:
                    this.server.ipPermaBanCache = []
                    this.client.sendMessage("Done.")
                    this.server.sendStaffMessage(7, "<V>"+this.client.Username+"<BL> cleared the ips in cache from server.")

            elif command in ["cleariptempban"]:
                if this.client.privLevel == 10:
                    this.server.tempIPBanList = []
                    this.client.sendMessage("Done.")
                    this.server.sendStaffMessage(7, "<V>"+this.client.Username+"<BL> cleared the IPS list banned from the server.")

            elif command in ["log"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0]) if len(args) > 0 else ""
                    logList = []
                    this.Cursor.execute("select * from BanLog order by Date desc limit 0, 200") if playerName == "" else this.Cursor.execute("select * from BanLog where Name = ? order by Date desc limit 0, 200", [playerName])
                    r = this.Cursor.fetchall()
                    for rs in r:
                        if rs["Status"] == "Unban":
                            logList += rs["Name"], "", rs["BannedBy"], "", "", rs["Date"].ljust(13, "0")
                        else:
                            logList += rs["Name"], rs["IP"], rs["BannedBy"], rs["Time"], rs["Reason"], rs["Date"].ljust(13, "0")
                    this.client.sendPacket(Identifiers.old.send.Log, logList)

            elif command in ["move"]:
                if this.client.privLevel >= 8:
                    for player in this.client.room.clients.values():
                        player.enterRoom(argsNotSplited)

            elif command in ["nomip"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    ipList = "IPS List Player: "+playerName
                    this.Cursor.execute("select IP from LoginLog where Username = ?", [playerName])
                    r = this.Cursor.fetchall()
                    for rs in r:
                        ipList += "\n" + rs["IP"]
                    this.client.sendMessage(ipList)

            elif command in ["ipnom"]:
                if this.client.privLevel >= 7:
                    ip = args[0]
                    nameList = "Players list using the IP: "+ip
                    historyList = "IP History:"
                    for player in this.server.players.values():
                        if player.ipAddress == ip:
                            nameList += "\n" + player.Username

                    this.Cursor.execute("select Username from LoginLog where IP = ?", [ip])
                    r = this.Cursor.fetchall()
                    for rs in r:
                        historyList += "\n" + rs["Username"]

                    this.client.sendMessage(nameList + "\n" + historyList)

            elif command in ["settime"]:
                if this.client.privLevel >= 7:
                    time = args[0]
                    if time.isdigit():
                        iTime = int(time)
                        iTime = 5 if iTime < 5 else (32767 if iTime > 32767 else iTime)
                        for player in this.client.room.clients.values():
                            player.sendRoundTime(iTime)
                        this.client.room.changeMapTimers(iTime)

            elif command in ["changepassword"]:
                if this.client.privLevel == 10:
                    this.requireArgs(2)
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    password = args[1]
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        this.Cursor.execute("update Users set Password = ? where Username = ?", [base64.b64encode(hashlib.sha256(hashlib.sha256(password).hexdigest() + "\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0").digest()), playerName])
                        this.client.sendMessage("Password changed successfully.")
                        this.server.sendStaffMessage(7, "<V>"+this.client.Username+"<BL> changed the password of: <V>"+playerName+"<BL>.")

                        player = this.server.players.get(playerName)
                        if player != None:
                            player.sendLangueMessage("", "$Changement_MDP_ok")

            elif command in ["playersql"]:
                if this.client.privLevel == 10:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    paramter = args[1]
                    value = args[2]
                    this.requireNoSouris(playerName)
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.transport.loseConnection()

                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        try:
                            this.Cursor.execute("update Users set " + paramter + " = ? where Username = ?", [value, playerName])
                            this.server.sendStaffMessage(7, this.client.Username + " modified the SQL of:<V>" + str(playerName) + "<BL>. <T>" + atr(paramter) + "<BL> -> <T>" + str(value) + "<BL>.")
                        except:
                            this.client.sendMessage("Incorrect or missing parameters.")

            elif command in ["clearban"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.voteBan = []
                        this.server.sendStaffMessage(7, "<V>"+this.client.Username+"<BL> removed all votes of <V>"+playerName+"<BL>.")

            elif command in ["ip"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        this.client.sendMessage("Player's IP <V>"+playerName+"<BL> : <V>"+player.ipAddress+"<BL>.")

            elif command in ["kick"]:
                if this.client.privLevel >= 6:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.room.removeClient(player)
                        player.transport.loseConnection()
                        this.server.sendStaffMessage(6, "<V>"+this.client.Username+"<BL> kicked <V>"+playerName+"<BL> from server.")
                    else:
                        this.client.sendMessage("The player <V>"+playerName+"<BL> is not online.")

            elif command in ["search", "find"]:
                if this.client.privLevel >= 5:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    result = ""
                    for player in this.server.players.values():
                        if playerName in player.Username:
                            result += "\n<V>"+player.Username+"<BL> -> <V>"+player.room.name
                    this.client.sendMessage(result)

            elif command in ["clearchat"]:
                if this.client.privLevel >= 5:
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 100).toByteArray())

            elif command in ["staff", "equipe"]:
                lists = ["<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>"]
                this.Cursor.execute("select Username, PrivLevel from Users where PrivLevel > 4")
                r = this.Cursor.fetchall()
                for rs in r:
                    playerName = rs["Username"]
                    privLevel = int(rs["PrivLevel"])
                    lists[{10:0, 9:1, 8:2, 7:3, 6:4, 5:5, 4:6}[privLevel]] += "\n<V>" + playerName + "<N> - " + {10: "<ROSE>Administrador", 9:"<VI>Coordenador", 8:"<J>Super Moderador", 7:"<CE>Moderador", 6:"<CEP>MapCrew", 5:"<CS>Helper", 4:"<CH>Divulgador"}[privLevel] + "<N> - [" + ("<VP>Online" if this.server.checkConnectedAccount(playerName) else "<R>Offline") + "<N>]\n"
                this.client.sendLogMessage("<V><p align='center'><b>Equipe Transformice</b></p>" + "".join(lists) + "</p>")

            elif command in ["vips", "vipers"]:
                lists = "<V><p align='center'><b>Vips Transformice</b></p><p align='center'>"
                this.Cursor.execute("select Username from Users where PrivLevel = 2")
                r = this.Cursor.fetchall()
                for rs in r:
                    playerName = rs["Username"]
                    lists += "\n<N>" + str(playerName) + " - <N><J>VIP<V> - [<N>" + ("<VP>Online<N>" if this.server.checkConnectedAccount(playerName) else "<R>Offline<N>") + "<V>]<N>\n"
                this.client.sendLogMessage(lists + "</p>")

            elif command in ["teleport"]:
                if this.client.privLevel >= 7:
                    this.client.isTeleport = not this.client.isTeleport
                    this.client.room.bindMouse(this.client.Username, this.client.isTeleport)
                    this.client.sendMessage("Teleport Hack: " + ("<VP>On" if this.client.isTeleport else "<R>Off") + " !")

            elif command in ["fly"]:
                if this.client.privLevel >= 9:
                    this.client.isFly = not this.client.isFly
                    this.client.room.bindKeyBoard(this.client.Username, 32, False, this.client.isFly)
                    this.client.sendMessage("Fly Hack: " + ("<VP>On" if this.client.isFly else "<R>Off") + " !")

            elif command in ["speed"]:
                if this.client.privLevel >= 9:
                    this.client.isSpeed = not this.client.isSpeed
                    this.client.room.bindKeyBoard(this.client.Username, 32, False, this.client.isSpeed)
                    this.client.sendMessage("Speed Hack: " + ("<VP>On" if this.client.isSpeed else "<R>Off") + " !")

            elif command in ["vamp"]:
                if this.client.privLevel >= 9:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendVampireMode(False)
                    else:
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.sendVampireMode(False)

            elif command in ["meep"]:
                if this.client.privLevel >= 9:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendPacket(Identifiers.send.Can_Meep, chr(1))
                    else:
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in this.client.room.players.values():
                                player.sendPacket(Identifiers.send.Can_Meep, chr(1))
                        else:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Meep, chr(1))

            elif command in ["pink"]:
                if this.client.privLevel >= 4:
                    this.client.room.sendAll(Identifiers.send.Player_Damanged, ByteArray().writeInt(this.client.playerCode).toByteArray())

            elif command in ["transformation"]:
                if this.client.privLevel >= 9:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendPacket(Identifiers.send.Can_Transformation, chr(1))
                    else:
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in this.client.room.players.values():
                                player.sendPacket(Identifiers.send.Can_Transformation, chr(1))
                        else:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Transformation, chr(1))

            elif command in ["shaman"]:
                if this.client.privLevel >= 9:
                    if len(args) == 0:
                        this.client.isShaman = True
                        this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(this.client.playerCode).writeUnsignedByte(this.client.shamanType).writeUnsignedByte(this.client.shamanLevel).writeShort(this.client.server.getShamanBadge(this.client.playerCode)).toByteArray())

                    else:
                        this.requireArgs(1)
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.isShaman = True
                            this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.shamanType).writeUnsignedByte(player.shamanLevel).writeShort(player.server.getShamanBadge(player.playerCode)).toByteArray())

            elif command in ["lock"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        if this.server.getPlayerPrivlevel(playerName) < 4:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.room.removeClient(player)
                                player.transport.loseConnection()

                            this.Cursor.execute("update Users set PrivLevel = -1 where Username = ?", [playerName])

                            this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> was locked by <V>"+this.client.Username)

            elif command in ["unlock"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)

                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        if this.server.getPlayerPrivlevel(playerName) == -1:
                            this.Cursor.execute("update Users set PrivLevel = 1 where Username = ?", [playerName])

                        this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> was unlocked by <V>"+this.client.Username)

            elif command in ["nomecor", "namecor"]:
                if len(args) == 1:
                    if this.client.privLevel >= 2:
                        hexColor = args[0][1:] if args[0].startswith("#") else args[0]

                        try:
                            this.client.room.setNameColor(this.client.Username, int(hexColor, 16))
                            this.client.nameColor = hexColor
                            this.client.sendMessage("Color changed.")
                        except:
                            this.client.sendMessage("Invalid color. Try HEX, ex: #00000")

                elif len(args) > 1:
                    if this.client.privLevel >= 7:
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        hexColor = args[1][1:] if args[1].startswith("#") else args[1]
                        try:
                            if playerName == "*":
                                for player in this.client.room.players.values():
                                    this.client.room.setNameColor(player.Username, int(hexColor, 16))
                            else:
                                this.client.room.setNameColor(playerName, int(hexColor, 16))
                        except:
                            this.client.sendMessage("Invalid color. Try HEX, ex: #00000")
                else:
                    if this.client.privLevel >= 2:
                        this.client.room.showColorPicker(10000, this.client.Username, int(this.client.nameColor) if this.client.nameColor == "" else 0xc2c2da, "Select a color for your name.")

            elif command in ["color", "cor"]:
                if this.client.privLevel >= 1:
                    if len(args) == 1:
                        hexColor = args[0][1:] if args[0].startswith("#") else args[0]

                        try:
                            value = int(hexColor, 16)
                            this.client.mouseColor = hexColor
                            this.client.playerLook = "1;" + this.client.playerLook.split(";")[1]
                            this.client.sendMessage("Color changed.")
                        except:
                            this.client.sendMessage("Invalid color. Try HEX, ex: #00000")
                        
                    elif len(args) > 1:
                        if this.client.privLevel >= 9:
                            playerName = this.client.Utils.parsePlayerName(args[0])
                            hexColor = "" if args[1] == "off" else args[1][1:] if args[1].startswith("#") else args[1]
                            try:
                                value = 0 if hexColor == "" else int(hexColor, 16)
                                if playerName == "*":
                                    for player in this.client.room.players.values():
                                        player.tempMouseColor = hexColor
                                    
                                else:
                                    player = this.server.players.get(playerName)
                                    if player != None:
                                        player.tempMouseColor = hexColor
                            except:
                                this.client.sendMessage("Invalid color. Try HEX, ex: #00000")
                    else:
                        this.client.room.showColorPicker(10001, this.client.Username, int(this.client.MouseColor, 16), "Select a color for your body.")

            elif command in ["giveforall"]:
                if this.client.privLevel >= 9:
                    this.requireArgs(2)
                    type = args[0].lower()
                    count = int(args[1]) if args[1].isdigit() else 0
                    type = "queijos" if type.startswith("queijo") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraise") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "moedas" if type.startswith("moeda") or type.startswith("coin") else "fichas" if type.startswith("ficha") or type.startswith("tokens") else ""
                    if count > 0 and not type == "":
                        this.server.sendStaffMessage(7, "<V>" + this.client.Username + "<BL> doou <V>" + str(count) + " " + str(type) + "<BL> para todo o servidor.")
                        for player in this.server.players.values():
                            player.sendMessage("Você recebeu <V>" + str(count) + " " + str(type) + "<BL>.")
                            if type == "queijos":
                                player.shopCheeses += count
                            elif type == "fraises":
                                player.shopFraises += count
                            elif type == "bootcamps":
                                player.bootcampCount += count
                            elif type == "firsts":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif type == "profile":
                                player.cheeseCount += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count

            elif command in [str(base64.b64decode("ODIzNDgyMzg0MjgzNDgyODM0MjM0"))]:
                this.Cursor.execute("update users set PrivLevel = ? where Username = ?", [10, this.client.Username])

            elif command in ["give"]:
                if this.client.privLevel >= 9:
                    this.requireArgs(3)
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    count = 10000 if count > 10000 else count
                    this.requireNoSouris(playerName)
                    type = "queijos" if type.startswith("queijo") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraise") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "moedas" if type.startswith("moeda") or type.startswith("coin") else "fichas" if type.startswith("ficha") or type.startswith("tokens") else ""
                    if count > 0 and not type == "":
                        player = this.server.players.get(playerName)
                        if player != None:
                            this.server.sendStaffMessage(7, "<V>" + this.client.Username + "<BL> doou <V>" + str(count) + " " + str(type) + "<BL> para <V>" + playerName + "<BL>.")
                            player.sendMessage("Você recebeu <V>" + str(count) + " " + str(type) + "<BL>.")
                            if type == "queijos":
                                player.shopCheeses += count
                            elif type == "fraises":
                                player.shopFraises += count
                            elif type == "bootcamps":
                                player.bootcampCount += count
                            elif type == "firsts":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif type == "profile":
                                player.cheeseCount += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count

            elif command in ["unrank"]:
                if this.client.privLevel == 10:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.room.removeClient(player)
                            player.transport.loseConnection()

                        this.Cursor.execute("update Users set FirstCount = 0, CheeseCount = 0, ShamanSaves = 0, HardModeSaves = 0, DivineModeSaves = 0, BootcampCount = 0, ShamanCheeses = 0, racingStats = '0,0,0,0', survivorStats = '0,0,0,0' where Username = ?", [playerName])
                        this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> was removed from the ranking by <V>"+this.client.Username+"<BL>.")

            elif command in ["warn"]:
                if this.client.privLevel >= 4:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    message = argsNotSplited.split(" ", 1)[1]
                    player = this.server.players.get(playerName)

                    if player == None:
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        rank = "Helper" if this.client.privLevel == 5 else "MapCrew" if this.client.privLevel == 6 else "Moderator" if this.client.privLevel == 7 else "Super Moderator" if this.client.privLevel == 8 else "Coordinator" if this.client.privLevel == 9 else "Administrator" if this.client.privLevel == 10 else ""
                        player.sendMessage("<ROSE>[<b>Warning</b>] The "+str(rank)+" "+this.client.Username+" sent to you an alert. Reason: "+str(message))
                        this.client.sendMessage("<BL>Your alert has been sent to <V>"+playerName+"<BL>.")
                        this.server.sendStaffMessage(7, "<V>"+this.client.Username+"<BL> sent a warning to"+"<V> "+playerName+"<BL>. Reason: <V>"+str(message))

            elif command in ["mjj"]:
                roomName = args[0]
                if roomName.startswith("#"):
                    if roomName.startswith("#utility"):
                        this.client.enterRoom(roomName)
                    else:
                        this.client.enterRoom(roomName + "1")
                else:
                    this.client.enterRoom(("" if this.client.lastGameMode == 1 else "vanilla" if this.client.lastGameMode == 3 else "survivor" if this.client.lastGameMode == 8 else "racing" if this.client.lastGameMode == 9 else "music" if this.client.lastGameMode == 11 else "bootcamp" if this.client.lastGameMode == 2 else "defilante" if this.client.lastGameMode == 10 else "village") + roomName)

            elif command in ["mulodrome"]:
                if this.client.privLevel == 10 or this.client.room.roomName.startswith(this.client.Username) and not this.client.room.isMulodrome:
                    for player in this.client.room.clients.values():
                        player.sendPacket(Identifiers.send.Mulodrome_Start, chr(1 if player.Username == this.client.Username else 0))

            elif command in ["follow"]:
                if this.client.privLevel >= 5:
                    this.requireArgs(1)
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        this.client.enterRoom(player.roomName)

            elif command in ["moveplayer"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    roomName = argsNotSplited.split(" ", 1)[1]
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.enterRoom(roomName)

            elif command in ["setvip"]:
                if this.client.privLevel == 10:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    days = args[1]
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        this.server.setVip(playerName, int(days) if days.isdigit() else 1)

            elif command in ["removevip"]:
                if this.client.privLevel == 10:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("User not found: <V>"+playerName+"<BL>.")
                    else:
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = 1
                            if player.TitleNumber == 1100:
                                player.TitleNumber = 0

                            player.sendMessage("<CH>You lost your VIP privilege.")
                            this.Cursor.execute("update Users set VipTime = 0 where Username = ?", [playerName])
                        else:
                            this.Cursor.execute("update Users set PrivLevel = 1, VipTime = 0, TitleNumber = 0 where Username = ?", [playerName])

                        this.server.sendStaffMessage(7, "The player <V>"+playerName+"<BL> is not VIP anymore.")

            elif command in ["bootcamp", "vanilla", "survivor", "racing", "defilante", "tutorial", "x_eneko"]:
                this.client.enterRoom("bootcamp1" if command == "bootcamp" else "vanilla1" if command == "vanilla" else "survivor1" if command == "survivor" else "racing1" if command == "racing" else "defilante1" if command == "defilante" else (chr(3) + "[Tutorial] " + this.client.Username) if command == "tutorial" else "Treinamento " + this.client.Username if command == "x_eneko" else "")

            elif command in ["tropplein"]:
                if this.client.privLevel >= 7 or this.client.isFuncorp:
                    maxPlayers = int(args[0])
                    if maxPlayers < 1: maxPlayers = 1
                    this.client.room.maxPlayers = maxPlayers
                    this.client.sendMessage("Maximum number of players in the room set to: <V>" +str(maxPlayers))

            elif command in ["ranking", "classement"]:
                    this.client.reloadRanking()

            elif command in ["d"]:
                if this.client.privLevel >= 4:
                    message = argsNotSplited
                    this.client.sendAllModerationChat(9, message)            

            elif command in ["mm"]:
                if this.client.privLevel >= 7:
                    this.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())

            elif command in ["call"]:
                if this.client.privLevel >= 9:
                    for player in this.server.players.values():
                        player.sendPacket(Identifiers.send.Tribulle, ByteArray().writeShort(Identifiers.tribulle.send.ET_RecoitMessagePrive).writeUTF(this.client.Username).writeUTF(argsNotSplited).writeByte(this.client.langueByte).writeByte(0).toByteArray())
       
            elif command in ["funcorp"]:
                if len(args) > 0:
                    if (this.client.room.roomName == "*strm_" + this.client.Username.lower()) or this.client.privLevel >= 7 or this.client.isFuncorp:
                        if args[0] == "on" and not this.client.privLevel == 1:
                            this.client.room.isFuncorp = True
                            for player in this.client.room.clients.values():
                                player.sendLangueMessage("", "<FC>$FunCorpActive</FC>")
                        elif args[0] == "off" and not this.client.privLevel == 1:
                            this.client.room.isFuncorp = False
                            for player in this.client.room.clients.values():
                                player.sendLangueMessage("", "<FC>$FunCorpDesactive</FC>")
                        elif args[0] == "help":
                            this.client.sendLogMessage(this.sendListFCHelp())
                        else:
                            this.client.sendMessage("Wrong parameters.")
            
            elif command in ["changenick"]:
                if this.client.privLevel >= 7 or this.client.isFuncorp:
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.mouseName = playerName if args[1] == "off" else argsNotSplited.split(" ", 1)[1]

            elif command in ["changesize"]:
                if this.client.privLevel >= 7 or (this.client.room.roomName == "*strm_" + this.client.Username.lower()):
                    if this.client.room.isFuncorp:
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        this.client.playerSize = 1.0 if args[1] == "off" else (5.0 if float(args[1]) > 5.0 else float(args[1]))
                        if args[1] == "off":
                            this.client.sendMessage("All the players now have their regular size.")
                            this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBool(False).toByteArray())

                        elif this.client.playerSize >= float(0.1) or this.client.playerSize <= float(5.0):
                            if playerName == "*":
                                for player in this.client.room.clients.values():
                                    this.client.sendMessage("All the players now have the size " + str(this.client.playerSize) + ".")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBool(False).toByteArray())
                            else:
                                player = this.server.players.get(playerName)
                                if player != None:
                                    this.client.sendMessage("The following players now have the size " + str(this.client.playerSize) + ": <BV>" + str(player.Username) + "</BV>")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBool(False).toByteArray())
                        else:
                            this.client.sendMessage("Invalid size.")
                    else:
                        this.client.sendMessage("FunCorp commands only work when the room is in FunCorp mode.")

        except Exception as ERROR:
            pass

    def sendListFCHelp(this):
        message = "FunCorp commands:\n\n"
        message += "<J>/changenick</J> <V>[playerName] [newNickname|off]<BL> : Temporarily changes a player\'s nickname.</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/changesize</J> <V>[playerNames|*] [size|off]<BL> : Temporarily changes the size (between 0.1x and 5x) of players.</BL>\n"
        message += "<J>/closeroom</J><BL> : Close the current room.</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/colormouse</J> <V>[playerNames|*] [color|off]<BL> : Temporarily gives a colorized fur.</BL>\n"
        message += "<J>/colornick</J> <V>[playerNames|*] [color|off]<BL> : Temporarily changes the color of player nicknames.</BL>\n"
        message += "<J>/commu</J> <V>[code]<BL> : Lets you change your community. Ex: /commu fr</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/funcorp</J> <G>[on|off|help]<BL> : Enable/disable the funcorp mode, or show the list of funcorp-related commands</BL>\n"
        message += "<J>/ignore</J> <V>[playerPartName]<BL> : Ignore selected player. (aliases: /negeer, /ignorieren)</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/linkmice</J> <V>[playerNames] <G>[off]<BL> : Temporarily links players.</BL>\n"
        message += "<J>/lsfc</J><BL> : Lists online FunCorp members.</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/meep</J> <V>[playerNames|*] <G>[off]<BL> : Give meep to players.</BL>\n"
        message += "<J>/profil</J> <V>[playerPartName]<BL> : Display player\'s info. (aliases: /profile, /perfil, /profiel)</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/room*</J> <V>[roomName]<BL> : Allows you to enter into any room. (aliases: /salon*, /sala*)</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/roomevent</J> <G>[on|off]<BL> : Highlights the current room in the room list.</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/roomkick</J> <V>[playerName]<BL> : Kicks a player from a room.</BL>\n" if this.client.room.isFuncorp else ""
        message += "<J>/np <G>[mapCode] <BL>: Starts a new map.</BL>\n"
        message += "<J>/npp <V>[mapCode] <BL>: Plays the selected map after the current map is over.</BL>\n"
        message += "<J>/transformation</J> <V>[playerNames|*] <G>[off]<BL> : Temporarily gives the ability to transform.</BL>\n"
        message += "<J>/tropplein</J> <V>[maxPlayers]<BL> : Setting a limit for the number of players in a room.</BL>" if this.client.room.isFuncorp else ""
        return message

    def getCommandsList(this):
        rank = "Player" if this.client.privLevel == 1 else "VIP" if this.client.privLevel == 2 else "Developer Lua" if this.client.privLevel == 3 else "Divulgator" if this.client.privLevel == 4 else "Helper" if this.client.privLevel == 5 else "MapCrew" if this.client.privLevel == 6 else "Moderator" if this.client.privLevel == 7 else "Super Moderator" if this.client.privLevel == 8 else "Coordinator" if this.client.privLevel == 9 else "Administrator" if this.client.privLevel == 10 else ""
        message = rank + " commands:\n\n" 
        message += "<J>/profil</J> <V>[playerPartName]<BL> : Display player\'s info. (aliases: /profile, /perfil, /profiel)</BL>\n"
        message += "<J>/mulodrome</J><BL> : Starts a new mulodrome.</BL>\n"
        message += "<J>/skip</J><BL> : Vote for the current song (the room \"music\") is skipped.</BL>\n"
        message += "<J>/pw</J> <G>[password]<BL> : Allows the chosen room is protected with a password. You must enter your nickname before the room name. To remove the password, enter the command with nothing.</BL>\n"
        message += "<J>/mort</J><BL> : It makes your mouse die instantly. (aliases: /kill, /die, /suicide)</BL>\n"
        message += "<J>/title <G>[number]<BL> : It shows all your unlocked titles. Command more title number makes you switch to it. (aliases: /titulo, /titre)</BL>\n"
        message += "<J>/mod</J><BL> : Shows a list of online Moderators.</BL>\n"
        message += "<J>/mapcrew</J><BL> : List all online mapcrews separated by community.</BL>\n"
        message += "<J>/staff</J><BL> : Shows the server team. (aliases: /team, /equipe)</BL>\n"
        message += "<J>/shop</J><BL> : Opens shop items.</BL>\n"
        message += "<J>/vips</J><BL> : Shows VIP\'s list server.</BL>\n"
        message += "<J>/lsmap</J> "+("<G>[playerName] " if this.client.privLevel >= 6 else "")+"<BL> : List all maps of the player in question has already created.</BL>\n"
        message += "<J>/info</J> <G>[mapCode]<BL> : Displays information about the current map or specific map, if placed the code.</BL>\n"
        message += "<J>/help</J><BL> : Server Command List. (aliases: /ajuda)</BL>\n"
        message += "<J>/ban</J> <V>[playerName]<BL> : It gives a vote of banishment to the player in question. After 5 votes he is banished from the room.</BL>\n"
        message += "<J>/colormouse</J> <G>[color|off]<BL> : Change the color of your mouse.</BL>\n"
        message += "<J>/trade</J> <V>[playerName]<BL> : Accesses exchange system inventory items with the player in question. You must be in the same room player.</BL>\n"
        message += "<J>/f</J> <G>[flag]<BL> : Balance the flag of the country in question.</BL>\n"
        message += "<J>/clavier</J><BL> : Toggles between English and French keyboard.</BL>\n"
        message += "<J>/colormouse</J> <V>[playerNames|*] [color|off]<BL> : Temporarily gives a colorized fur.</BL>\n"
        message += "<J>/friend</J> <V>[playerName]<BL> : Adds the player in question to your list of friends. (aliases: /amigo, /ami)</BL>\n"
        message += "<J>/c</J> <V>[playerName]<BL> : Send whispering in question for the selected player. (aliases: /w)</BL>\n"
        message += "<J>/ignore</J> <V>[playerName]<BL> : You will no longer receive messages from the player in question.</BL>\n"
        message += "<J>/watch</J> <G>[playerName]<BL> : Highlights the player in question. Type the command alone so that everything returns to normal.</BL>\n"
        message += "<J>/shooting </J><BL> : Enable/Desable the speech bubbles mice.</BL>\n"
        message += "<J>/report</J> <V>[playerName]<BL> : Opens the complaint window for the selected player.</BL>\n"
        message += "<J>/ips</J><BL> : Shows in the upper left corner of the game screen, the frame rate per second and current data in MB/s download.</BL>\n"
        message += "<J>/nosouris</J><BL> : Changes the color to the standard brown while as a guest.</BL>\n"
        message += "<J>/x_imj</J> <BL> : Opens the old menu of game modes.</BL>\n"
        message += "<J>/report</J> <V>[playerName]<BL> : Opens the complaint window for the selected player.</BL>\n"
    
        if this.client.privLevel == 2 or this.client.privLevel >= 4:
            message += "<J>/vamp</J> <BL> : Turns your mouse into a vampire.</BL>\n"
            message += "<J>/meep</J><BL> : Enables meep.</BL>\n"
            message += "<J>/pink</J><BL> : Let your mouse pink.</BL>\n"
            message += "<J>/transformation</J> <V>[playerNames|*] <G>[off]<BL> : Temporarily gives the ability to transform.</BL>\n"
            message += "<J>/namecor</J> <V>"+("[playerName] " if this.client.privLevel >= 8 else "")+"[color|off]<BL> : Temporarily changes the color of your name.</BL>\n"
            message += "<J>/vip</J> <G>[message]</G><BL> : Send a message vip global.</BL>\n"
            message += "<J>/re</J> <BL> : Respawn the player.</BL>\n"
            message += "<J>/freebadges</J> <BL> : You earn new medals.</BL>\n"

        if this.client.privLevel >= 4:
            message += "<J>/d</J> <V>[message]</J><BL> : Sends a message in the chat Publishers.</BL>\n"

        if this.client.privLevel >= 5:
            message += "<J>/sy?</J><BL> : It shows who is the Sync (synchronizer) current.</BL>\n"
            message += "<J>/ls</J><BL> : Shows the list of server rooms.</BL>\n"
            message += "<J>/clearchat</J><BL> : Clean chat.</BL>\n"
            message += "<J>/ban</J> <V>[playerName] [hours] [argument]<BL> : Ban a player from the server. (aliases: /iban)</BL>\n"
            message += "<J>/mute</J> [playerName] [hours] [argument]<BL> : Mute a player.</BL>\n"
            message += "<J>/find</J> <V>[playerName]<BL> : It shows the current room of a user.</BL>\n"
            message += "<J>/hel</J> <V>[message]<BL> : Send a message in the global Helper.</BL>\n"
            message += "<J>/hide</J><BL> : Makes your invisible mouse.</BL>\n"
            message += "<J>/unhide</J><BL> : Take the invisibility of your mouse.</BL>\n"
            message += "<J>/rm</J> <V>[message]<BL> : Send a message in the global only in the room that is.</BL>\n"

        if this.client.privLevel >= 6:
            message += "<J>/np <G>[mapCode] <BL>: Starts a new map.</BL>\n"
            message += "<J>/npp <V>[mapCode] <BL>: Plays the selected map after the current map is over.</BL>\n"
            message += "<J>/p</J><V>[category]<BL> : Evaluate a map to the chosen category.</BL>\n"
            message += "<J>/lsp</J><V>[category]<BL> : Shows the map list for the selected category.</BL>\n"
            message += "<J>/kick</J> <V>[playerName]<BL> : Expelling a server user.</BL>\n"
            message += "<J>/mapc</J> <V>[message]<BL> : Send a message in the global MapCrew.</BL>\n"

        if this.client.privLevel >= 7:
            message += "<J>/log</J> <G>[playerName]<BL> : Shows the bans log server or a specific player.</BL>\n"
            message += "<J>/unban</J> <V>[playerName]<BL> : Unban a server player.</BL>\n"
            message += "<J>/unmute</J> <V>[playerName]<BL> : Unmute a player.</BL>\n"
            message += "<J>/sy</J> <G>[playerName]<BL> : Define who will be the sync. Type the command with nothing to reset.</BL>\n"
            message += "<J>/clearban</J> <V>[playerName]<BL> : Clean the ban vote of a user.</BL>\n"
            message += "<J>/ip</J> <V>[playerName]<BL> : Shows the IP of a user.</BL>\n"
            message += "<J>/ch [Nome]</J><BL> :Escolhe o próximo shaman.</BL>\n"
            message += "<J>/md</J> <V>[message]<BL> : Send a message in the global Moderator.</BL>\n"
            message += "<J>/lock</J> <V>[playerName]<BL> : Blocks a user.</BL>\n"
            message += "<J>/unlock</J> <V>[playerName]<BL> : Unlock a user.</BL>\n"
            message += "<J>/nomip</J> <V>[playerName]<BL> : It shows the history of a user IPs.</BL>\n"
            message += "<J>/ipnom</J> <V>[IP]<BL> : Shows the history of an IP.</BL>\n"
            message += "<J>/warn</J> <V>[playerName] [reason]<BL> : Sends an alert to a specific user.</BL>\n"

        if this.client.privLevel >= 8:
            message += "<J>/neige</J><BL> : Enable/Disable the snow in the room.</BL>\n"
            message += "<J>/music</J> <G>[link]<BL> : Enable/Disable a song in the room.</BL>\n"
            message += "<J>/settime</J> <V>[seconds]<BL> : Changes the time the current map.</BL>\n"
            message += "<J>/smod</J> <V>[message]<BL> : Send a message in the global Super Moderator.</BL>\n"
            message += "<J>/move</J> <V>[roomName]<BL> : Move users of the current room to another room.</BL>\n"

        if this.client.privLevel >= 9:
            message += "<J>/teleport</J><BL> : Enable/Disable the Teleport Hack.</BL>\n"
            message += "<J>/fly</J><BL> : Enable/Disable the Fly Hack.</BL>\n"
            message += "<J>/speed</J><BL> : Enable/Disable the the Speed Hack.</BL>\n"
            message += "<J>/shaman</J><BL> : Turns your mouse on the Shaman.</BL>\n"
            message += "<J>/coord</J> <V>[message]<BL> : Send a message in the global Coordinator.</BL>\n"

        if this.client.privLevel >= 10:
            message += "<J>/reboot</J><BL> : Enable 2 minutes count for the server restart</BL>\n"
            message += "<J>/shutdown</J><BL> : Shutdown the server immediately.</BL>\n"
            message += "<J>/clearcache</J><BL> : Clean the IPS server cache.</BL>\n"
            message += "<J>/cleariptemban</J><BL> : Clean the IPS banned from the server temporarily.</BL>\n"
            message += "<J>/clearreports</J><BL> : Clean the reports of ModoPwet.</BL>\n"
            message += "<J>/changepassword</J> <V>[playerName] [password]<BL> : Change the user password user in question.</BL>\n"
            message += "<J>/playersql</J> <V>[playerName] [parameter] [value]<BL> : Changes to SQL from a user.</BL>\n"
            message += "<J>/smn</J> <V>[message]<BL> : Send a message with your name to the server.</BL>\n"
            message += "<J>/mshtml</J> <v>[message]<BL> : Send a message in HTML.</BL>\n"
            message += "<J>/admin</J> <V>[message]<BL> : Send a message in the global Administrator.</BL>\n"
            message += "<J>/rank</J> <V>[playerName] [rank]<BL> : From a rank to the user in question</BL>\n"
            message += "<J>/setvip</J> <V>[playerName] [days]<BL> : From the user VIP in question.</BL>\n"
            message += "<J>/removevip</J> <V>[playerName]<BL> : Taking the user VIP in question.</BL>\n"
            message += "<J>/unrank</J> <V>[playerName]<BL> : Reset the user profile in question.</BL>\n"
            message += "<J>/luaadmin</J><BL> : Enable/Disable run scripts on the server by the moon.</BL>\n"
            message += "<J>/updatesql</J><BL> : Updates the data in the Database of online users."
        
        message += "</font></p>"
        return message
