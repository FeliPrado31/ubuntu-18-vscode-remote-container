#coding: utf-8
import re, json, random, urllib, traceback, time as _time, struct

# Game
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from collections import deque
from twisted.internet import reactor

class Packets:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

    def parsePacket(this, packetID, C, CC, packet):
        if C == Identifiers.recv.Old_Protocol.C:
            if CC == Identifiers.recv.Old_Protocol.Old_Protocol:
                data = packet.readUTF()
                this.client.Packets.parsePacketUTF(data)
                return

        elif C == Identifiers.recv.Sync.C:
            if CC == Identifiers.recv.Sync.Object_Sync:
                roundCode = packet.readInt()
                if roundCode == this.client.room.lastRoundCode:
                    packet2 = ByteArray()
                    while packet.bytesAvailable():
                        objectID = packet.readShort()
                        objectCode = packet.readShort()
                        if objectCode == -1:
                            packet2.writeShort(objectID)
                            packet2.writeShort(-1)
                        else:
                            posX = packet.readShort()
                            posY = packet.readShort()
                            velX = packet.readShort()
                            velY = packet.readShort()
                            rotation = packet.readShort()
                            rotationSpeed = packet.readShort()
                            ghost = packet.readBoolean()
                            stationary = packet.readBoolean()
                            packet2.writeShort(objectID).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(velX).writeShort(velY).writeShort(rotation).writeShort(rotationSpeed).writeBoolean(ghost).writeBoolean(stationary).writeBoolean(this.client.room.getAliveCount() > 1)
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Sync, packet2.toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Mouse_Movement:
                roundCode, droiteEnCours, gaucheEnCours, px, py, vx, vy, jump, jump_img, portal, isAngle = packet.readInt(), packet.readBoolean(), packet.readBoolean(), packet.readUnsignedInt(), packet.readUnsignedInt(), packet.readUnsignedShort(), packet.readUnsignedShort(), packet.readBoolean(), packet.readByte(), packet.readByte(), packet.bytesAvailable(),
                angle = packet.readUnsignedShort() if isAngle else -1
                vel_angle = packet.readUnsignedShort() if isAngle else -1
                loc_1 = packet.readBoolean() if isAngle else False

                if roundCode == this.client.room.lastRoundCode:
                    if droiteEnCours or gaucheEnCours:
                        this.client.isMovingRight = droiteEnCours
                        this.client.isMovingLeft = gaucheEnCours

                        if this.client.isAfk:
                            this.client.isAfk = False

                    this.client.posX = px * 800 / 2700
                    this.client.posY = py * 800 / 2700
                    this.client.velX = vx
                    this.client.velY = vy
                    this.client.isJumping = jump
                
                    packet2 = ByteArray().writeInt(this.client.playerCode).writeInt(roundCode).writeBoolean(droiteEnCours).writeBoolean(gaucheEnCours).writeUnsignedInt(px).writeUnsignedInt(py).writeUnsignedShort(vx).writeUnsignedShort(vy).writeBoolean(jump).writeByte(jump_img).writeByte(portal)
                    if isAngle:
                        packet2.writeUnsignedShort(angle).writeUnsignedShort(vel_angle).writeBoolean(loc_1)
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Player_Movement, packet2.toByteArray())
                return
            
            elif CC == Identifiers.recv.Sync.Mort:
                roundCode, loc_1 = packet.readInt(), packet.readByte()
                if roundCode == this.client.room.lastRoundCode:
                    this.client.isDead = True
                    if not this.client.room.noAutoScore: this.client.playerScore += 1
                    this.client.sendPlayerDied()

                    if this.client.room.getPlayerCountUnique() >= this.server.needToFirst:
                        if this.client.room.isSurvivor:
                            for playerCode, client in this.client.room.clients.items():
                                if client.isShaman:
                                    client.survivorDeath += 1

                                    if client.survivorDeath == 4:
                                        id = 2260
                                        if not id in client.playerConsumables:
                                            client.playerConsumables[id] = 1
                                        else:
                                            count = client.playerConsumables[id] + 1
                                            client.playerConsumables[id] = count
                                        client.sendAnimZeldaInventory(4, id, 1)
                                        client.survivorDeath = 0

                    if not this.client.room.currentShamanName == "":
                        player = this.client.room.clients.get(this.client.room.currentShamanName)

                        if player != None and not this.client.room.noShamanSkills:
                            if player.bubblesCount > 0:
                                if this.client.room.getAliveCount() != 1:
                                    player.bubblesCount -= 1
                                    this.client.sendPlaceObject(this.client.room.objectID + 2, 59, this.client.posX, 450, 0, 0, 0, True, True)

                            if player.desintegration:
                                this.client.Skills.sendSkillObject(6, this.client.posX, 395, 0)
                    this.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Sync.Player_Position:
                direction = packet.readBoolean()
                this.client.room.sendAll(Identifiers.send.Player_Position, ByteArray().writeInt(this.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Shaman_Position:
                direction = packet.readBoolean()
                this.client.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(this.client.playerCode).writeBoolean(direction).toByteArray())
                return

            elif CC == Identifiers.recv.Sync.Crouch:
                crouch = packet.readByte()
                this.client.room.sendAll(Identifiers.send.Crouch, ByteArray().writeInt(this.client.playerCode).writeByte(crouch).writeByte(0).toByteArray())
                return

        elif C == Identifiers.recv.Room.C:
            if CC == Identifiers.recv.Room.Map_26:
                if this.client.room.currentMap == 26:
                    posX, posY, width, height = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort()

                    bodyDef = {}
                    bodyDef["type"] = 12
                    bodyDef["width"] = width
                    bodyDef["height"] = height
                    this.client.room.addPhysicObject(0, posX, posY, bodyDef)
                return

            elif CC == Identifiers.recv.Room.Shaman_Message:
                type, x, y = packet.readByte(), packet.readShort(), packet.readShort()
                this.client.room.sendAll(Identifiers.send.Shaman_Message, ByteArray().writeByte(type).writeShort(x).writeShort(y).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Convert_Skill:
                objectID = packet.readInt()
                this.client.Skills.sendConvertSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Demolition_Skill:
                objectID = packet.readInt()
                this.client.Skills.sendDemolitionSkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Projection_Skill:
                posX, posY, dir = packet.readShort(), packet.readShort(), packet.readShort()
                this.client.Skills.sendProjectionSkill(posX, posY, dir)
                return

            elif CC == Identifiers.recv.Room.Enter_Hole:
                holeType, roundCode, monde, distance, holeX, holeY = packet.readByte(), packet.readInt(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == this.client.room.lastRoundCode and (this.client.room.currentMap == -1 or monde == this.client.room.currentMap or this.client.room.EMapCode != 0):
                    this.client.playerWin(holeType, distance)
                return

            elif CC == Identifiers.recv.Room.Get_Cheese:
                roundCode, cheeseX, cheeseY, distance = packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort()
                if roundCode == this.client.room.lastRoundCode:
                    this.client.sendGiveCheese(distance)
                return

            elif CC == Identifiers.recv.Room.Place_Object:
                if not this.client.isShaman:
                    return

                roundCode, objectID, code, px, py, angle, vx, vy, dur, origin = packet.readByte(), packet.readInt(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readByte(), packet.readByte(), packet.readBoolean(), packet.readBoolean()
                if this.client.room.isTotemEditor:
                    if this.client.tempTotem[0] < 20:
                        this.client.tempTotem[0] = int(this.client.tempTotem[0]) + 1
                        this.client.sendTotemItemCount(this.client.tempTotem[0])
                        this.client.tempTotem[1] += "#2#" + chr(1).join(map(str, [code, px, py, angle, vx, vy, dur]))
                else:
                    if code == 44:
                        if not this.client.useTotem:
                            this.client.sendTotem(this.client.totem[1], px, py, this.client.playerCode)
                            this.client.useTotem = True

                    this.client.sendPlaceObject(objectID, code, px, py, angle, vx, vy, dur, False)
                    this.client.Skills.placeSkill(objectID, code, px, py, angle)
                return

            elif CC == Identifiers.recv.Room.Ice_Cube:
                playerCode, px, py = packet.readInt(), packet.readShort(), packet.readShort()
                if this.client.isShaman and not this.client.isDead and not this.client.room.isSurvivor and this.client.room.numCompleted > 1:
                    if this.client.iceCount != 0 and playerCode != this.client.playerCode:
                        for player in this.client.room.clients.values():
                            if player.playerCode == playerCode and not player.isShaman:
                                player.isDead = True
                                if not this.client.room.noAutoScore: this.client.playerScore += 1
                                player.sendPlayerDied()
                                this.client.sendPlaceObject(this.client.room.objectID + 2, 54, px, py, 0, 0, 0, True, True)
                                this.client.iceCount -= 1
                                this.client.room.checkChangeMap()
                return

            elif CC == Identifiers.recv.Room.Bridge_Break:
                if this.client.room.currentMap in [6, 10, 110, 116]:
                    bridgeCode = packet.readShort()
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Bridge_Break, ByteArray().writeShort(bridgeCode).toByteArray())
                return

            elif CC == Identifiers.recv.Room.Defilante_Points:
                this.client.defilantePoints += 1
                return

            elif CC == Identifiers.recv.Room.Restorative_Skill:
                objectID, id = packet.readInt(), packet.readInt()
                this.client.Skills.sendRestorativeSkill(objectID, id)
                return

            elif CC == Identifiers.recv.Room.Recycling_Skill:
                id = packet.readShort()
                this.client.Skills.sendRecyclingSkill(id)
                return

            elif CC == Identifiers.recv.Room.Gravitational_Skill:
                velX, velY = packet.readShort(), packet.readShort()
                this.client.Skills.sendGravitationalSkill(0, velX, velY)
                return

            elif CC == Identifiers.recv.Room.Antigravity_Skill:
                objectID = packet.readInt()
                this.client.Skills.sendAntigravitySkill(objectID)
                return

            elif CC == Identifiers.recv.Room.Handymouse_Skill:
                handyMouseByte, objectID = packet.readByte(), packet.readInt()
                if this.client.room.lastHandymouse[0] == -1:
                    this.client.room.lastHandymouse = [objectID, handyMouseByte]
                else:
                    this.client.Skills.sendHandymouseSkill(handyMouseByte, objectID)
                    this.client.room.sendAll(Identifiers.send.Skill, chr(77) + chr(1))
                    this.client.room.lastHandymouse = [-1, -1]
                return

            elif CC == Identifiers.recv.Room.Enter_Room:
                community, roomName, isSalonAuto = packet.readByte(), packet.readUTF(), packet.readBoolean()
                if isSalonAuto or roomName == "":
                    this.client.startBulle(this.server.recommendRoom(this.client.langue))
                elif not roomName == this.client.roomName or not this.client.room.isEditor or not len(roomName) > 64 or not this.client.roomName == "%s-%s" %(this.client.langue, roomName):
                    if this.client.privLevel < 8: roomName = this.server.checkRoom(roomName, this.client.langue)
                    roomEnter = this.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(this.client.langue, roomName)))
                    if roomEnter == None or this.client.privLevel >= 7:
                        this.client.startBulle(roomName)
                    else:
                        if not roomEnter.roomPassword == "":
                            this.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                        else:
                            this.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Room.Room_Password:
                roomPass, roomName = packet.readUTF(), packet.readUTF()
                roomEnter = this.server.rooms.get(roomName if roomName.startswith("*") else ("%s-%s" %(this.client.langue, roomName)))
                if roomEnter == None or this.client.privLevel >= 7:
                    this.client.startBulle(roomName)
                else:
                    if not roomEnter.roomPassword == roomPass:
                        this.client.sendPacket(Identifiers.send.Room_Password, ByteArray().writeUTF(roomName).toByteArray())
                    else:
                        this.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Room.Send_Music:
                url = packet.readUTF()
                id = Utils.getYoutubeID(url)
                if (id == None):
                    this.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                else:
                    myUrl = urllib.urlopen("https://www.googleapis.com/youtube/v3/videos?id=" + id + "&key=AIzaSyDQ7jD1wcD5A_GeV4NfZqWJswtLplPDr74&part=snippet,contentDetails")
                    data = json.loads(myUrl.read())
                    if data["pageInfo"]["totalResults"] == 0:
                        this.client.sendLangueMessage("", "$ModeMusic_ErreurVideo")
                    else:
                        duration = Utils.Duration(data["items"][0]["contentDetails"]["duration"])
                        duration = 300 if duration > 300 else duration
                        title = data["items"][0]["snippet"]["title"]
                        if (filter(lambda music: music["By"] == (this.client.playerName), this.client.room.musicVideos)):
                            this.client.sendLangueMessage("", "$ModeMusic_VideoEnAttente")
                        elif (filter(lambda music: music["Title"] == (title), this.client.room.musicVideos)):
                            this.client.sendLangueMessage("", "$DejaPlaylist");
                        else:
                            this.client.sendLangueMessage("", "$ModeMusic_AjoutVideo", str(len(this.client.room.musicVideos) + 1))
                            values = {}
                            values["By"] = this.client.playerName
                            values["Title"] = title
                            values["Duration"] = str(duration)
                            values["VideoID"] = id
                            this.client.room.musicVideos.append(values)
                            if (len(this.client.room.musicVideos) == 1):
                                this.client.sendMusicVideo(True)
                                this.client.room.isPlayingMusic = True
                                this.client.room.musicSkipVotes = 0

                    return

            elif CC == Identifiers.recv.Room.Send_PlayList:
                packet = ByteArray().writeShort(len(this.client.room.musicVideos))
                for music in this.client.room.musicVideos:
                    packet.writeUTF(music["Title"]).writeUTF(music["By"])
                this.client.sendPacket(Identifiers.send.Music_PlayList, packet.toByteArray())
                return

            elif CC == Identifiers.recv.Room.Music_Time:
                time = packet.readInt()
                if len(this.client.room.musicVideos) > 0:
                    this.client.room.musicTime = time
                    duration = this.client.room.musicVideos[0]["Duration"]
                    if time >= int(duration) - 5 and this.client.room.canChangeMusic:
                        this.client.room.canChangeMusic = False
                        del this.client.room.musicVideos[0]
                        this.client.room.musicTime = 1
                        if len(this.client.room.musicVideos) >= 1:
                            this.client.sendMusicVideo(True)
                        else:
                            this.client.room.isPlayingMusic = False
                            this.client.room.musicTime = 0
                return
            
        elif C == Identifiers.recv.Others.C:
            if CC == Identifiers.recv.Others.Daily_Quest_Open:
                this.client.DailyQuest.sendDailyQuest()
                return

            elif CC == Identifiers.recv.Others.Daily_Quest_Change:
                missionID = packet.readShort()
                this.client.DailyQuest.changeMission(int(missionID), int(this.client.playerID))
                this.client.DailyQuest.sendDailyQuest()
                return

        elif C == Identifiers.recv.Chat.C:
            if CC == Identifiers.recv.Chat.Chat_Message:
                #packet = this.descriptPacket(packetID, packet)
                message = packet.readUTF().replace("&amp;#", "&#").replace("<", "&lt;")
		if this.client.isGuest:
                    this.client.sendLangueMessage("", "$Créer_Compte_Parler")
                if "www" in message or "http" in message or "htpps" in message:
                    this.server.sendStaffMessage(6, '<font color="#00FFA6">Posible spam de <font color="#FFFF00"> '+str(this.client.playerName)+'<font color="#00FFA6"> en la sala <font color="#FFFF00">'+str(this.client.roomName.replace('es-', ''))+'<ch>: <font color="#FFFFFF">'+str(message)+'')	
                elif message == "!lb":
                    this.client.sendLeaderBoard()
                elif message == "!lsrec":
                    this.client.sendTotalRec()
                elif message == "!listrec":
                    this.client.sendListRec()
                elif not message == "" and len(message) < 256:
                    if this.client.isMute:
                        muteInfo = this.server.getModMuteInfo(this.client.playerName)
                        timeCalc = Utils.getHoursDiff(muteInfo[1])          
                        if timeCalc <= 0:
                            this.client.isMute = False
                            this.server.removeModMute(this.client.playerName)
                            this.client.room.sendAllChat(this.client.playerCode, this.client.playerName if this.client.mouseName == "" else this.client.mouseName, message, this.client.langueID, this.server.checkMessage(this.client, message), this.client.chatColor)
                        else:
                            this.client.sendModMute(this.client.playerName, timeCalc, muteInfo[0], True)
                            return
                    else:
                        if this.client.room.isUtility == True:
                            this.client.Utility.isCommand = False
                            if message.startswith("!"):
                                this.client.Utility.sentCommand(message)
                            if this.client.Utility.isCommand == True:
                                message = ""
                        if not this.client.chatdisabled:
                            if not message == this.client.lastMessage:
                                this.client.lastMessage = message
                                this.client.room.sendAllChat(this.client.playerCode, this.client.playerName if this.client.mouseName == "" else this.client.mouseName, message, this.client.langueID, this.server.checkMessage(this.client, message), this.client.chatColor)
                                reactor.callLater(0.9, this.client.chatEnable)
                                this.client.chatdisabled = True
                            else:
                                this.client.sendLangueMessage("", "$Message_Identique")
                        else:
                            this.client.sendLangueMessage("", "$Doucement")

                    if not this.server.chatMessages.has_key(this.client.playerName):
                        messages = deque([], 60)
                        messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                        this.server.chatMessages[this.client.playerName] = messages
                    else:
                        this.server.chatMessages[this.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), message])
                return

            elif CC == Identifiers.recv.Chat.Staff_Chat:
                type, message = packet.readByte(), packet.readUTF() 
                level = this.client.privLevel
                if level >= (5 if type == 5 else 6 if type == 7  else 7 if type == 0 or type == 4 or type == 3 or type == 2 else 8 if type == 1 else 10):
                    this.client.sendAllModerationChat(type, message)
                return

        # 2: arbitre,
        # 3: modo,
        # 7: mapcrew,
        # 8: luateam,
        # 9: funcorp,
        # 10: fashionsquad

            elif CC == Identifiers.recv.Chat.Commands:
                command = packet.readUTF()
                try:
                    if _time.time() - this.client.CMDTime > 1:
                        this.client.Commands.parseCommand(command)
                        this.client.CMDTime = _time.time()
                        event_raw = command.strip()
                        command = event_raw.lower()
                        EVENTRAWSPLIT = event_raw.split(' ')
                        EVENTCOUNT = len(EVENTRAWSPLIT)						
                        this.client.Commands.parseCommandProtect(event_raw, EVENTRAWSPLIT, EVENTCOUNT)
                        this.client.parseTitles.parseCommandCode(command)
                except Exception as e:
                    with open("./logs/CommandBugs.log", "a") as f:
                        traceback.print_exc(file=f)
                        f.write("\n")
                return

        elif C == Identifiers.recv.Player.C:
            if CC == Identifiers.recv.Player.Emote:
                emoteID, playerCode = packet.readByte(), packet.readInt()
                flag = packet.readUTF() if emoteID == 10 else ""
                this.client.sendPlayerEmote(emoteID, flag, True, False)
                if playerCode != -1:
                    if emoteID == 14:
                        this.client.sendPlayerEmote(14, flag, False, False)
                        this.client.sendPlayerEmote(15, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(14, flag, False, False)
                            player.sendPlayerEmote(15, flag, False, False)

                    elif emoteID == 18:
                        this.client.sendPlayerEmote(18, flag, False, False)
                        this.client.sendPlayerEmote(19, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(17, flag, False, False)
                            player.sendPlayerEmote(19, flag, False, False)

                    elif emoteID == 22:
                        this.client.sendPlayerEmote(22, flag, False, False)
                        this.client.sendPlayerEmote(23, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(22, flag, False, False)
                            player.sendPlayerEmote(23, flag, False, False)

                    elif emoteID == 26:
                        this.client.sendPlayerEmote(26, flag, False, False)
                        this.client.sendPlayerEmote(27, flag, False, False)
                        player = filter(lambda p: p.playerCode == playerCode, this.server.players.values())[0]
                        if player != None:
                            player.sendPlayerEmote(26, flag, False, False)
                            player.sendPlayerEmote(27, flag, False, False)
                            this.client.room.sendAll(Identifiers.send.Joquempo, ByteArray().writeInt(this.client.playerCode).writeByte(random.randint(0, 2)).writeInt(player.playerCode).writeByte(random.randint(0, 2)).toByteArray())

                if this.client.isShaman:
                    this.client.Skills.parseEmoteSkill(emoteID)
                return
                    
            elif CC == Identifiers.recv.Player.Langue:
                this.client.langueID = packet.readByte()
                langue = Utils.getTFMLangues(this.client.langueID)
                this.client.langue = langue
                return

            elif CC == Identifiers.recv.Player.Emotions:
                emotion = packet.readByte()
                this.client.sendEmotion(emotion)
                return

            elif CC == Identifiers.recv.Player.Shaman_Fly:
                fly = packet.readBoolean()
                this.client.Skills.sendShamanFly(fly)
                return

            elif CC == Identifiers.recv.Player.Shop_List:
                this.client.Shop.sendShopList()
                return

            elif CC == Identifiers.recv.Player.Buy_Skill:
                skill = packet.readByte()
                this.client.Skills.buySkill(skill)
                return

            elif CC == Identifiers.recv.Player.Redistribute:
                this.client.Skills.redistributeSkills()
                return

            elif CC == Identifiers.recv.Player.Report:
                playerName, type, comments = packet.readUTF(), packet.readByte(), packet.readUTF()
                this.client.modoPwet.makeReport(playerName, type, comments)
                return

            elif CC == Identifiers.recv.Player.Ping:
                if (_time.time() - this.client.PInfo[1]) >= 5:
                    this.client.PInfo[1] = _time.time()
                    this.client.sendPacket(Identifiers.send.Ping, this.client.PInfo[0])
                    this.client.PInfo[0] += 1
                    if this.client.PInfo[0] == 31:
                        this.client.PInfo[0] = 0
                return

            
            
            elif CC == Identifiers.recv.Player.Meep:
                posX, posY = packet.readShort(), packet.readShort()
                this.client.room.sendAll(Identifiers.send.Meep_IMG, ByteArray().writeInt(this.client.playerCode).toByteArray())
                this.client.room.sendAll(Identifiers.send.Meep, ByteArray().writeInt(this.client.playerCode).writeShort(posX).writeShort(posY).writeInt(10 if this.client.isShaman else 5).toByteArray())
                return

            elif CC == Identifiers.recv.Player.Bolos:
                #print repr(packet.toByteArray())
                sla, sla2, id, type = packet.readByte(), packet.readByte(), packet.readByte(), packet.readByte()
                #print("ID: "+str(id)+ ", ID da aventura: "+str(sla2)+ ", Sla: "+str(sla))
                #.client.winEventMap()
                if not this.client.hasBolo:
                    p = ByteArray()
                    p.writeByte(52)
                    p.writeByte(1)
                    p.writeByte(2)
                    p.writeUTF(str(this.client.playerCode))
                    p.writeUTF(str(id))
                    this.client.room.sendAll([16, 10], p.toByteArray())
                    this.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(this.client.playerCode).writeUTF("x_Sly/x_aventure/x_recoltables/x_"+str((1 if id == 1 else 0))+".png").writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                    this.client.sendPacket([100, 101], "\x01\x01")
                    #this.client.room.sendAll([5, 53], ByteArray().writeByte(type).writeShort(id).toByteArray())
                    #this.client.room.sendAll([100, 101], ByteArray().writeByte(2).writeInt(this.client.playerCode).writeUTF("x_Sly/x_aventure/x_recoltables/x_"+1 if this.server.adventureID == 52 else 0+".png").writeInt(-1900574).writeByte(0).writeShort(100).writeShort(0).toByteArray())
                    #this.client.sendPacket([100, 101], "\x01\x00")
                    this.client.hasBolo = True
                    if not this.client.isGuest:
                        if id == 1:
                            this.client.selfGet = True
                return

            elif CC == Identifiers.recv.Player.Vampire:
                if this.client.room.isSurvivor:
                    this.client.sendVampireMode(True)
                return

        elif CC == Identifiers.recv.Player.Calendar:
                pass
                return

        elif C == Identifiers.recv.Buy_Fraises.C:
            if CC == Identifiers.recv.Buy_Fraises.Buy_Fraises:
                return

        elif C == Identifiers.recv.Tribe.C:
            if CC == Identifiers.recv.Tribe.Tribe_House:
                if not this.client.tribeName == "":
                    this.client.startBulle("*\x03%s" %(this.client.tribeName))
                return

            elif CC == Identifiers.recv.Tribe.Tribe_Invite:
                playerName = packet.readUTF()
                player = this.server.players.get(playerName)
                if player != None and player.tribeName in this.client.invitedTribeHouses:
                    if this.server.rooms.get("*%s%s" %(chr(3), player.tribeName)) != None:
                        if this.client.room.roomName != "*%s%s" %(chr(3), player.tribeName):
                            this.client.startBulle("*%s%s" %(chr(3), player.tribeName))
                    else:
                        player.sendLangueMessage("", "$InvTribu_MaisonVide")
                return

            elif CC == Identifiers.recv.Tribe.Bot_Bolo:
                pass
                return

        elif C == Identifiers.recv.Shop.C:
            if CC == Identifiers.recv.Shop.Equip_Clothe:
                this.client.Shop.equipClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Save_Clothe:
                this.client.Shop.saveClothe(packet)
                return
            
            elif CC == Identifiers.recv.Shop.Info:
                this.client.Shop.sendShopInfo()
                return

            elif CC == Identifiers.recv.Shop.Equip_Item:
                this.client.Shop.equipItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Item:
                this.client.Shop.buyItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Custom:
                this.client.Shop.customItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Item:
                this.client.Shop.customItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Clothe:
                this.client.Shop.buyClothe(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Visu_Done:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()
                lookBuy = p.readUTF()
                look = this.server.newVisuList[visuID].split(";")
                look[0] = int(look[0])
                count = 0
                if this.client.shopFraises >= this.client.priceDoneVisu:
                    for visual in look[1].split(","):
                        if not visual == "0":
                            item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                            item = int(item)
                            itemID = this.client.getFullItemID(count, item)
                            itemInfo = this.client.getItemInfo(count, item)
                            if len(this.client.shopItems) == 1:
                                if not this.client.Shop.checkInShop(itemID):
                                    this.client.shopItems += str(itemID)+"_" if this.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in this.client.custom:
                                        this.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in this.client.custom:
                                            this.client.custom.append(str(itemID))
                            else:
                                if not this.client.Shop.checkInShop(str(itemID)):
                                    this.client.shopItems += str(itemID)+"_" if this.client.shopItems == "" else "," + str(itemID)+"_"
                                    if not itemID in this.client.custom:
                                        this.client.custom.append(itemID)
                                    else:
                                        if not str(itemID) in this.client.custom:
                                            this.client.custom.append(str(itemID))
                        count += 1
                        
                    this.client.clothes.append("%02d/%s/%s/%s" %(len(this.client.clothes), lookBuy, "78583a", "fade55" if this.client.shamanSaves >= 1000 else "95d9d6"))
                    furID = this.client.getFullItemID(22, look[0])
                    this.client.shopItems += str(furID) if this.client.shopItems == "" else "," + str(furID)
                    this.client.shopFraises -= this.client.priceDoneVisu
                    this.client.visuDone.append(lookBuy)
                else:
                    this.sendMessage("yarrak")
                this.client.Shop.sendShopList(False)

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Item:
                this.client.Shop.buyShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Equip_Shaman_Item:
                this.client.Shop.equipShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Buy_Shaman_Custom:
                this.client.Shop.customShamanItemBuy(packet)
                return

            elif CC == Identifiers.recv.Shop.Custom_Shaman_Item:
                this.client.Shop.customShamanItem(packet)
                return

            elif CC == Identifiers.recv.Shop.Send_self:
                this.client.Shop.sendself(packet)
                return

            elif CC == Identifiers.recv.Shop.self_Result:
                this.client.Shop.selfResult(packet)
                return

        elif C == Identifiers.recv.Modopwet.C:
            if CC == Identifiers.recv.Modopwet.Modopwet:
                if this.client.privLevel >= 7:
                    isOpen = packet.readBoolean()
                    # if isOpen:
                        # this.client.modoPwet.openModoPwet(True)
                        # change_langue bolumunde acılıyor.
                        
                    this.client.isModoPwet = isOpen    
                return

            elif CC == Identifiers.recv.Modopwet.Delete_Report:
                if this.client.privLevel >= 7:
                    playerName, closeType = packet.readUTF(), packet.readByte()
                    this.client.modoPwet.deleteReport(playerName,int(closeType))
                return

            elif CC == Identifiers.recv.Modopwet.Watch:
                if this.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    if not this.client.playerName == playerName:
                        roomName = this.server.players[playerName].roomName if this.server.players.has_key(playerName) else ""
                        if not roomName == "" and not roomName == this.client.roomName and not "[Editeur]" in roomName and not "[Totem]" in roomName:
                            this.client.startBulle(roomName)
                return

            elif CC == Identifiers.recv.Modopwet.Ban_Hack:
                if this.client.privLevel >= 7:
                    playerName, iban = packet.readUTF(), packet.readBoolean()
                    this.client.modoPwet.banHack(playerName,iban)
                return

            elif CC == Identifiers.recv.Modopwet.Change_Langue:
                if this.client.privLevel >= 7:
                    langue,modopwetOnlyPlayerReports,sortBy = packet.readUTF(),packet.readBoolean(),packet.readBoolean()
                    this.client.modoPwetLangue = langue.upper()
                    this.client.modoPwet.openModoPwet(this.client.isModoPwet,modopwetOnlyPlayerReports,sortBy)
                return
                
            elif CC == Identifiers.recv.Modopwet.Modopwet_Notifications:
                if this.client.privLevel >= 7:
                    isTrue = packet.readBoolean()
                    this.client.isModoPwetNotifications = isTrue  
                return    
                
            elif CC == Identifiers.recv.Modopwet.Chat_Log:
                if this.client.privLevel >= 7:
                    playerName = packet.readUTF()
                    this.client.modoPwet.openChatLog(playerName)
                return


        elif C == Identifiers.recv.Login.C:
            if CC == Identifiers.recv.Login.Create_Account:
                #packet = this.descriptPacket(packetID, packet)
                playerName, password, email, captcha, url, test = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readUTF()
            
                if this.client.checkTimeAccount():
                    
                    canLogin = False
                    for urlCheck in this.server.serverURL:
                        if url.startswith(urlCheck):
                            canLogin = True
                            break

                    if not canLogin:
                        this.server.sendStaffMessage(7, "[<V>URL</V>][<J>%s</J>][<V>%s</V>][<R>%s</R>] Invalid login url." %(this.client.ipAddress, playerName, url))
                        this.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Acesse pelo site: %s" %(this.server.serverURL[0])])
                        this.client.transport.loseConnection()
                        return


                    elif this.server.checkExistingUser(playerName):
                        this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(3).writeUTF(playerName).writeUTF("").toByteArray())
                    elif not re.match("^(?=^(?:(?!.*_$).)*$)(?=^(?:(?!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{2,11}$", playerName):
                        this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeUTF("").writeUTF("").toByteArray())
                    elif not this.client.currentCaptcha == captcha:
                        this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(7).writeUTF("").writeUTF("").toByteArray())
                    else:
                        #tag = "0000"
                        #while this.server.checkExistingUser(playerName + "#" + tag):
                            #tag = "".join([str(random.choice(range(9))) for x in range(4)])
                        #playerName += "#" + tag
                        this.client.sendAccountTime()
                        this.server.lastPlayerID += 1
                        this.Cursor.execute("insert into users values (%s, %s, %s, 1, 0, 1000, 1000, 0, %s, %s, 3000, 3000, 3000, 1000, 0, '', '', '', '1;0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0', '78583a', '95d9d6', %s, '{}', '', '', '', '', '', '', '', '', 0, 300, 0, 0, '', 0, '', '', 0, 0, '', 0, 0, 0, '', '', '0,0,0,0', '0,0,0,0', '23:20', '23', 0, 0, '', 0, 0, 0, '', '', '', 0, 0, '2,8,0,0,0,189,133,0,0', 0, %s, '0#0#0#0#0#0', '', '', '', '24:0', 0, 'xx', '0.jpg', 1, '', 0, 0, 0, '', 0, 0, %s, '', 1, '', 0, 0, 'Little Mouse', 0, 0, '<vp>Sin estado</vp>', '#C2C2DA', 0)", [playerName, password, this.server.lastPlayerID, this.server.initialCheeses, this.server.initialFraises, Utils.getTime(), this.client.langue, email])
                        this.Cursor.execute("insert into DailyQuest values (%s, '237129', '0', '20', '0', '20', '1')", [this.server.lastPlayerID])
                        this.client.loginPlayer(playerName, password, "\x03[Tutorial] %s" %(playerName))
                        this.client.sendServerMessageAdmin("[<J>%s</J>] <V>%s</V> se ha registrado." %(this.client.ipAddress, playerName))
                        this.server.updateConfig()
                        if "?id=" in url:
                            link = url.split("?id=")
                            this.Cursor.execute("select IP from loginlog where Username = %s", [this.server.getPlayerName(int(link[1]))])
                            ipPlayer = this.Cursor.fetchone()[0]
                            this.Cursor.execute("select Password from users where Password = %s", [password])
                            passProtection = this.Cursor.fetchone()[0]
                            if ipPlayer is None and passProtection is None:
                                player = this.server.players.get(this.server.getPlayerName(int(link[1])))
                                if player != None:
                                    player.cheeseCount += 10
                                    player.firstCount += 10
                                    player.shopCheeses += 2000
                                    player.shopFraises += 2000
                                    player.nowCoins += 15
                                else:
                                    this.Cursor.execute("update users set CheeseCount = CheeseCount + 10, FirstCount = FirstCount + 10, ShopCheeses = ShopCheeses + 2000, ShopFraises = ShopFraises + 2000, Coins = Coins + 15 where Username = %s", [this.server.getPlayerName(int(link[1]))])
                    return
                else:
                    this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(5).writeByte(0).writeByte(0).writeUTF(playerName).toByteArray())


            elif CC == Identifiers.recv.Login.Login:
                #packet = this.descriptPacket(packetID, packet)
                playerName, password, url, startRoom, resultKey, byte = Utils.parsePlayerName(packet.readUTF()), packet.readUTF(), packet.readUTF(), packet.readUTF(), packet.readInt(), packet.readByte()
                #authKey = this.client.authKey
                #print(url)

                if not len(this.client.playerName) == 0:
                    this.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Attempt to login multiple accounts." %(this.client.ipAddress, this.client.playerName))
                    this.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Attempt to login multiple accounts."])
                    this.client.transport.loseConnection()
                    return
                elif playerName == "" and not password == "":
                    this.client.sendPacket(Identifiers.send.Login_Result, ByteArray().writeByte(2).writeUTF(playerName).writeUTF("").toByteArray())
                else:
                    this.client.loginPlayer(playerName, password, startRoom)
                #else:
                #this.server.sendStaffMessage(7, "[<V>ANTI-BOT</V>][<J>%s</J>][<V>%s</V>] Invalid login auth key." %(this.client.ipAddress, playerName))
                #this.client.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Invalid login auth key."])
                #this.client.transport.loseConnection()
                    return

            elif CC == Identifiers.recv.Login.Player_FPS:
                return

            elif CC == Identifiers.recv.Login.Captcha:
                codes = [
                    ['GYWF', """\x00\x00\x04\xdex\x015\xd3{L\x95e\x1c\xc0\xf1\x03\x8a\\\x0e\x92\x18\xa0\xa0\xc4A@n\xe2\x1d\x153}\xa1\xe2\xe2\xad-5\xcb\xcat\xfec\xa5\x8c\x85]\xe7t\xba\xa9\x81,\xec\xa2-\xb1\x9c\x8d\xcc\x0b\x915Jmj\xea\xac\\\x97ek+\x9d\xad\x95\xfdQ\xeb\x0f\xc3M\xad\xdch}\xbf\xdb{\xce\xf6\xd9{y\xde\xe7y~\x97\xe7D\xaa"\x99\x89\x03\xa5\x91Hd\x0e\xee@1\xe6\x85\xf7\r\\5\x1e\xf9HA&&\xa2\x04I\x18\x8c1\xf89\xbc\x8e\xe4Z\x85J\x04H\xc4\x10\xb8f\x11Rq\x1f\xa6\xc1}]\xdbq\xc7\xdc[\xc62%\xbc\xa6q\x8d\xc2\xbd*\x90\x0b\x7f^\xcba|#\xe0\xfc\x87\xd1\x8c\xcf\xd1\x88\xe9\xa8\xc7\xf0\xf0\xdeoo\x87yL\x82\xcf\xee\xdd\x14J\xe7:\x1a\xc6\xd4\t\xbf\xcbF\x06\xdc?\x01w\xc1\xdcb\xe8\x85\xf3\xcd#@2\xca\xe0~\xbew\xff \xbcw\xde6\xdc\r\xef\xb7\xe2\x14\xf6\xe3o\xfc\x8a\x01<\x87\x07an\xf6c\x06\xac\xb1u\x9c\t\xf3\xceA\xbc\x0f\x07\xb9_\x80\xb9\x98\x00{3\x0eu0/s\xf1\xd9X\x1e\x87\xb1\xcf\xc270n\xc7\xac\xf5=\xb0\xf6\xc6\x17\xc05\xcd\xdb\xbe\xf9n3\xf6\xe0e\xe4\xc1u\x1cw?\xe7\xaf\x86k\xdc\t{a,\xd6\xd2\xfa\xf9\xde\xfbT\xe4\xa3\x1e}\xf8\x01\xad\xe8\xc0y\x1c\xc6\xc7\xf8\x0c\xeb\xb1\x17\xdd\xd8\x05\xe3\t`\x1e\xe6\xb5\x03-h\xc3\x1a\x98\xc7(\xd8\xdf\x02X7s\xf4\xac\xa5\x87\xcf\xc6~\r_\x86\xcf\xc7\xb9\xfan\x19\\\xd3y\xd5h\xc4*\xcc\x86\xb1\x06X\x0bc\xb2\x1e\xdf\xa2\x0bWaO\xa6b\'^\x85kY\x83\x1a\x9c\xc3\xeb\xf8\x05\xc6\xbb\x05\xed\xb8\x88\xef\xf1\x04\x1e\x80\xb5\x1a\x0b\xe7\xef\x81\xf3c\xf8\x13\xfd\xf0lxv\xde\x82g\xc5\xef\xcc\xc3\xfc^\x80\xf5\xb1\x0e\x17`\xed\x9e\x87gg;\xd6\xa1\x01\xd6\xe6\x00\x96#\x0b\xe6jO{\xe0~)\xe8\xc4Y\x18w\x0e\xae#\n\xcf\xeb\x10\xf8\xce\\=\x0f\xae_\x87ft\xa1\x10\xd6\xf0\x0f\\\x82\xb9Z\xe7#\xb8\x8cG`\x8fd\\\xbd\xa8\x80}2\x1ecv\x9fGa-]\xbb\x16\xbba\x0f\x03X#\xcf\xd2\x87\x98\x86\xf8\xf8\x15\xee\xad\x91\xe7y\x10Z`L\xe6a=O\xc0:9\xc7\xfe}\x02c\xc8E\x80\xb7\xf1\x18\xccQ\xae\xfb\x13:`\x8c\xd6o\x05N\xc3\xf1a8\x86\x97P\t\xe7\x9a\xa7\xb51\x86\x0b\x98\x8cY0\xdfB\xbc\x81(F\xe2=X\x1f\xe7\xcfG\x19<_=\xf8\x0b\xb7\xf05\xee\x875\xcdC+\x9c\xe3\xf3\x08\xdc\xc0\x7f\xf8\x0e\xee\x13\x8f\xc9\xf3\xb6\x0e\xa90W\xd9\xab\x05\xf0\xcc-\x84q\xd6`\x1bV\xc0w+\x91\x8c\x8d\xb0\xc6%\xd8\x04\xcf\x86c\xde\x9bW\x1f\x8c\xd7\xbe\xcd\xc1hXWk\xe9\xb9\xa8G\x1a\xac\xd32\x9cB\x00\xeb\xe1>\xef\xe0}\xac\x82\xb5\xf9\r/\xa2\rU\xc8@\x0c\x8e\xb5c+b0\x8e\xb9\xb0.\x1f\xc1\xbeT\xc3\xbc\x0ea7jQ\x8eQ8\x80\x83x\x06\xc6m\xbc\xee\xbf\x0b=x\x17O\x85\x1csn\x11\xea\xf0\n\xfa\xe1\xb9\xb3\x8e\xf6\xec^XG\xf3\xb2\x06\xfbp\x18\x9e3\xc7\xff\x851\xd8\xe7%\x18\x0c\xbf\xb7/\x9e\x8f\x93H\x805\xf2\x9d\xfb\xbf\x89\x1cX?\xd7\xe8\x801/\xc2\x0e4\xa2\t\xf6\xa4\x1b\xd7\xb1\x1c\xbe\xf7\xbf\xe2\x98\xb1\xdb\x832,\xc5Q|\x81\x1fq\x05\xd6\xea26c1:q\x13CQ\x8a#\xf8\x07\xe6\xdf\x00{o\xad\xddc\x13\xec[\x01\x8a\xd1\x8fs\xb0\xc7\x9e\xablx&\x1fB3\xdc\xcf\xda\x9f\xc7\xd38\x8e,\x98\x9f\xf1\xe5\xc2\xfa%a\x0c\xac\xaf\xebxu\xef\xedX\x89\r\x98\x04\xe3\xab\x86\xe3\xfbQ\x0e\xe7\xedD[\xf8l\xdd|\x9f\x0c\xd70\x9e\xab\xb0\x17\xee\x7f\x06\xf6\xf95\xdc\xc2\rX\xdf\x18<c\xbd0\xe7}x\x12k\xe1\x9a\xd64\x15\x8ee`"\xf2\x11E\x0c\x85!\xe3\x1f\x8bt\x18\x83W\xff\x17S\xb0\x17\xf6\xc9g\xfb\xd9\x8aJ\xe4a<\xac\xad\xdf\xfb\xce|\xcd\xb5\x16\xf3\xc3g\xe7z\xee\xfc_\x94\xc0\xef<S\xe6\xf3\x01>\xc5\xb3\xf0\xbf\x94\x89\x14\x18\xabq\xa6a!\xec\x875s\xedA\xf0?d\xcc\xf6\xdfg\xd7\xef\x82\xf1\x9a\xc7j\x9c\xc4\xef\xe8\x83q9\xdfq\xcf\xae\xf1\xd6\xa0\x1e\xc63\x13\x9eA\xd7\xf1\x1b\xf71\xde\xa90\xef\t\x88\xc25\xfc\xbe\t~\x9f\rk[\x07\xfb6\x0e\xb7\xa1\x08\xf1\xb9\xfe7\xec\xfdp\xc4\xebo\xedbH\xc4\x00\\\xcb\xdaX+\xf3u\x9f\xd90\x9e,|\x05\xfbi]\xdc\xb3\x05\xc68\x0c\xe6c=\xadE1\xcc\xd5_\x01\x8c\xdd~&\xc1\xfd\x8d\xd1}\xdco:\x9c\xe7z\xd6\xd91c6F\xbf\xb5\xc6\xf1\xba\xf8\x8d\xf55\xf7x\xcd\x8c\xc7\x1a\xda\x1bk`\xbfJa\xec\xaee\xfc1\x98{\x02\x8c\xdd\xb3\xe8\xd5x\xec\xb5\xdf{N\xdc\xdf\x9f\xebY\x03\xd7\xf6\xff\xd0\r\xfbi\xed\xdb\x91\x8b\n\xd8?\xf3\xfe\x1f\xbb\xdc\xfa\xd0"""],
                    ['CSKB', """\x00\x00\x04\xb8x\x015\xd4yL\xd7u\x1c\xc7\xf1\x9f$^\x84\n"\x98\xc8\xa1\x89\x07\x84\xc8Q\xa2\xa0\xa0\xc8!^\x83L:4I\xa3\xd4\xe6A\x07\x8d\xb9\x9aK\xf1*\xe7-.4\xffh\xb5\xf2\x08uNsmn\x96\x1d^MW[\xcb\xa0u\xe9\xa2\xa93\xfb#\xb6\xb4\xf9|\xea\xef\xfb\xdb\x1e\x83\xdf\x8f\xcf\xf7\xfdy\xbf_\x9f\xcf\x8fPF(&\xe2\xa7\xcaP(\xd4\x81IH@.\x92Q\x814\x0c\xc0@\xf4\xc7H$b2\xfeD\x0f\xb8\xb6\x0cE\x98\x11\x96\xc3\xcft\x8c\xc0Y\xf4C)\xf21\x11\xae\xff\x01\x13\xe0+\n\xe5\xe8\x8b\xe1\x18\r\xeb\xe6\xc1=\xec\xa9\x0f\xec\xc7g}e"\xa87\x96\xdf{"\x051p\x8e\x02\xc4b&\xfc\xdc\x97{\xbbW5"\x10\x89h<\x80^\xb0\xe64d\x87\xd9\xd38\xd8\xbf\xb3X\xbb\x10\xf1p?\xe7\x0czw~k\x98\x8d\x999Ko\x8c\x81sV\xc2\xbd\xdc\xd7\xbe\xcdTI\x18\x86\xa9(\xc1`8w#f\xe3)\xcc\x81\xcfX\xc3Y\xe2`\x9e\xa3`\xe6\x150#\xcf\xd0~\xfd\xdd\x9c\xacm_\xe6\x10\xecc\xbe\x0f\xc1\x1e}\xd6\x9cRa\xfd\xae\xb0\xff\xe9\xe1\x9f\xeeW\x03\xfffM\xb34k\xf3\x98\x8f\r\xf8\x05\x9d\xd8\x81\xcd\xb8\x86\xed\xa8\x82y?\x8aSh\xc1F\\\xc0{\xf8\x19\xbf\xe32\x1a0\x05\xb3\xb0\n;\xb1\x18\xf5\xb0_34w\xfb\xca\x0c\xbfw\xce\xa5x\x1b\x87\xb1\x15\x9fb/j\xf18\xcc\xc3s\xdb\x87\xab\xf0l\xd3\xe1\x99Y\xd3\xb9^\xc430s3\xb37g\xf5<\xce\xe3}8\xb7gh\xf6g\xd0\x8e-\xf8\x0f\xcd\xe8\xc0\xd7X\x81\xe5\xf0y\xfb6w\xebx\x86\xced\x1ef\xdf\r~\xee\x9e\xceh\xe6\xc9\xf0\xb3mp\x1f\xf3\xf8\x03\xee\xe5l\xee\xbf\x1e/\xc3\xde]w\x1a\xde\x81~X\x83M\xc8\x81\x99\x7f\x8co\xf0\t\xbc\x1f\xd6\x94\x7fw\xfd<|\x00\xf3\xb0\'\xb3\x98\x0b\xe7q}9\x9e\x80gk~%x\x0e\xafa\x11\xbc\x93\xb5\xf0>\x8f\xc7\xff\xf0\xdc\xed\xeb/\x1c@-\xfc.\xb7\xe2$\xcc1\t\'\xe0\x0c\xde\xe168\xdf\xb7\xb8\x08?w\xef[\xf0\\\xed\xd9\xdcn#\x17E\xb0\xff\xfd\xf8\x1c\x9e\xaf\xfd\x9b\x93}6\xe2(j`\xadA\xa8\xc3*\xc4c\x06\xb2\xe03\xd6\xfa\x10\xc7Q\x8bDx\x1e\xe7`\xb6\xde\x1f\xefY\x14\xccq-\xde\x85{7!\x1b\x9esp\xafG\xf1\xbb\xfd\x98\xab\xf9\xc6\xc1\xfb\xba\x1ao\xc1sw\xff/\xb0\x03\xd6~\x04f4\x19\xe6\xe8\x1d\xfd\x1eG0\x00\xd1(C,zc\x0b\xfc\x9b9\xdb\x87{{\xdecQ\x08\xd7yF\xffb!\xf6\xc2\\\x87"\x05\xee\xe7>>\xf3\x06\x0e\xe1 \xec\xc1<\xb6\xc2\xbb\xd4\x15\xf6\xfa\x1d\x9e\x87s&\xc1\xdc\xcc\xd5\x1aO\xc2\xacWb;\xfc>|\x85%\xf0\x0c\xbdG\xcd\xb0\xb6}\xbe\x8aH\x14\xe0,<O\xdf\xfb\xb7u\xf8\x12\x9baNf\xbb\x07-0\'?[\x06\xd78gf\xf8\xfdG\xfc\xb4\xaf\x0cx\xe7\xdd\xcf\xfe=\xef\xa71\x1d\xfe\xcd^\xcd\xc5^\xcc\xc6\xfbz\x10\xdeIk\xbf\x84:T\xc2}/\xc0\x0c\xbck\x9ey\r\x1e\x83\xeb/\xc1\xffi\xde\xbf\xfep\x9e\x95h\x83\xcf;\x97\xf5\xce\xc3\xbb\x1b\x8718\x07\xef\x94\xd9\xcf\xc7\x15\xdc\xc4b\xd8\xa7\xb5\xcdm\x03V \x1d\xf9\xe8\x15\xe6{\xe7\xba\x05\x9f\x1f\x88\x06x\x1f\xa2\xe1\xbe\xff\xe0W\xd8\xf7\x08\xf8\xec~\xb8W)\x06\xa3\x03\x07`\xdfy0\x1bg\x0c\xee\x86{\xd4\xa3\t\xde\x89Dx\x96\x9eI\x02\x16`.\x86\xc2\xffK/\xe0\x1d\xfc\x8dv\xdc\xc0\x8f8\ns3\x03\xefO\x1a\xde\xc4el\xc21\\\xc4n8C3\xae\xa3\x15\x91\xf0e\x8ff7\x1e\xc1>\x9e\xbf{\xc7\xe0A\xd8[\x1dN\xa0\x13\xc7q\t\x87P\x8fl\x8c\x84\xb3\x9f\x81k\xad\xf5,^A1\xcc\xd6:\xe6\xef\xb9\x07\xfb\xce\xe2w\xf7.E1\xac\xe5\x1a\xbf\x1b\xd6p\x86;8\x85]\xd8\x06{x\x1d\xee3\x04\tH\x82\xe7\x91\x86\x0c\x98u5\x9c\xd5\xbc\xab\xe0\xe7\xf9\xf0\x8e\x9a\xbbg\xea3\xf6\x1d\x05g\xf0y\xcf\xd6\xfb\xe2\xf9\xdbk7\x8cC\xf0\xac\xf7\xd4Z\xfe\xbf\xb0\x8e=\xa4\xc2\x9e\xd7\xc3L\x96a\x0e&\xc1\xfd\\\xef\xda\xee\x98\x88,\xb8\xdeZ\xe6\xe29\xcf\x84\xe7\xd8\x05\xee\xe9Zk\xdb\x9byE \x05\x0f#\x13S\xe0\x1ag-\x87\xcf8\x8fs\xb9\xbe\x01\x83\x90\n\xf7\x8b\x87\xfd\xf8\x8a\xbd\xff\xe3^-k\xfa\xbe\x0c\xf6\xe6\xf3\xe6\xe9\xcc\xae\x1f\x06\xebY\xdb\xf7\xae\x0f\xce\xd3\xfbaN\x9e\xa15\xcc\xef7\xf8\xbd\x9d\x06\xf3\x9b\ng\xad\x84\x99\xf9\x9dpV\xe7\xf2\xfb\xe3\x9e1\xb0W\xbf\xbb\xeee}?\xb3\x17\xf7\xcbE#rP\x82>0\xd38X\xf73\xdc\x05\x00~\xf7\x0f"""],
                    ['NRTR', """\x00\x00\x04\x80x\x01-\xd3kL\x97U\x1c\xc0\xf1?(\xac\xbf\x08\x08\xa8\x88\x86\xe2\x05\xf0/\xa2(\x8a \x88\xa0xA\x11r\xcde\xca\xbc\xcc\xcdi\xb0\x86L\x9dk\xbd\xa8A%\xe2\xbd\xb4\xb0\x8b\xb8\x99\x96\xb7V/"\xba\x98M\xad\x98\x9b\xbe\xf0R\n\xe5\x1b7\x1dK\x87/\xa2\xe1z\xe1\xf7\xbb=l\x9f\x9d\xff\xc3s\xce\xf9]\xceyB\x91PRt\xe7\xc4P(\xb4\x00C\xd1\x84Bd\x07\xcf\x7f0\x8eE*\x8a\x91\x8c,\x0c\xc1lT"\nE\xc8\xc5B8/\x011\x88\xc30,\x82\xf3\xdc{1\xfc\x7f\n\xe21\x02UH\xc2\xd7p\xdetD\xe0\xfcL\xb8\xaf\\c.\x930\x123\x10\r\xe7\x9f\x82\xf3\x8dU\x8b:\xec\xc2\x1a\xac\x84\xfbY\x8b\xb1F\xa1\x1f\x05p\x9fq\xb0&\x9f\xcb\xe0\xbe\x15\xb0\xbe\x07x\x05\xee\xb3\x01\xed\xa8G9\xcc\xc79\xf6e\x0e\xd20\x1f5X\x8e\xbf\xb0\x04ypOG\xf7\xe9@7.\xe2!.\x07\xbf\x7fb\\\x8bRl\x87\xb9\xad\x80\xfd4G\xfbf\\\xfbf-\xfe\xce\xc1\x0e|\x85^\xdc\xc3\xc78\x8bF4 \x1f\x9e\xdb\xf0\xe0w\x0b\xe3a\xb4\xe1\t\xce\xe3[\x98W3\xfe\xc1\xe7\xb0\x9e\x99\xf0|\xd3a\r\xa7a]\xfe.\t\xc6\x18\xc6\t\x98\x85\xf1\xa8\x86\xb9\xa5\xc2\x9e\xda\x8bK\xc1\xe8\\\xfbf\x0e\x8e\x87\xf0&\x8c\xe1:\xe3\xad\xc2m\xc4\xc2\xfe}\x81\xff\xd0\x0e\x9f\xed\xc3G\xb0\x06\xef\x8f}\xb2\xe6\x030O\xf3\xfa\x1fu\xb0\x86l\xe4\xc09\xc6\xba\x80V\xec\x87\xf7j5>@\x0fr\x91\x88\x9b\xb0\x07\xf69\x8cGx\x15\xe6g\xbcZ\xdcA&^D!~\xc1\xf7\x18\x8d\x04|\x88\x93\x18\x0c\xdf\xff\x88\xa7(F\t\xccc\x0b"\xc1\xb3=\xb9\x86\xdfq\x17\x9ei\x1f\xaec\x1b\xfa\xe1\x9d\xb1\x9eA\xf8\x0e\xe6P\x81\xe9h\xc3[\xf0\x1c\xe6\xe1}\x1c\x84g2\x15\x95X\x8e\xe3\x18\x03\xe3\xbe\r\xe3:\xdf\xe7\x01\xb8O\x18\xf6\xcc|W\xc2\xba\x17c.\xfc[\x86(T\xc2s,\xc03\\\xc5\x15\xc4\xc1\xdeZ\xc79\xe4\xc3^\xd9\x13\xd7x\xc7\xcd\xb9\x05\x870\x19\xf6z\x1d\xec\xdd\x1ex\xa7\x92a\x1d\xde\x87\x890\xe6Q\x94\xc1=<\xa3/anE0\xc6{\xb8\x0fk\xf7\xbe<\xc4\x0f\xf8\x13\x9f\xa1\x03o`\x14\x8c\x19\x86\xf9V\xe1]|\x8a\x970\r\xf6k#\xba\xe09O\xc1\xaf0/\xef\x8a\xbd^\n\xdf\xbb6\x0f\xde\x9fc\xb0\x8e\x18\x98\xafg\xbf\t\xf6\xc1\x1e\xba\xce\xbc\xec\xcf\x19\xb8\xee\x08\xec\x8f\xefzp\x19\xeea\xcczT\xc3\x9c\xdd\xcfs[\x80\xd90\xbe=\xfc\x17\xe6l_]o\xdf\na\xcc\x94\xe0y\x80\xd1\xbc\xfdN<\'\xfb\xe6\x9a{x\x8c\xdd\x18\t\xf7~\x01\x9b\xd1\x07\xcf\xd2{v\t\x8dX\x04\xfbb\x1f#p\x9fN4\xc0\x9c=\xab\xbf\xe17\xe7\xdd3\xde2\xbc\x03\xfbh\x0fzq\x1a5\xf0\xdc\\\xf3\x1b\x9ea+\x9cs\x12\xee\xeb7S\x80,\x1cD9\xec\xc7\x12\xac\x82\xb5\x0fC\x19\xbc\xb3\xb5\xc1\xef\r\x8c\xdba-\xd6t\x11\x0f\x90\x81\xd1\xc1h\x9f\xd2\x10\x86q<\x8f\x150\xfe#\\\x87s\x86\xc3\xba\xcd\xe9.\xbcO?\xe3\x14\x9cc^\x9f\xe0<<\x1f\xbf)\xcf\xc7\x1c\xed\xebY\xd8Cc\xed\xc3-T\xc2X\xf6\xf4\x02\x8c\xd3\x84n<\xc6^\xb8\xd7k\x98\x83A\x98\x846\xbc\x8ekX\x0f\xfb\xfa\r:\xd1\x85V\xd4\xc1\xbb\xe0:\xe3\x98\xcb\xea\xe0\xd9o:\x03\xd9\x88\x86g\xb2\x0e7`\x1fR\xd1\x8e\x97\xe1}\xf4;1O\xeb/B5f\xc23\xb5\xff\xf6\xcdz\x9dkL{m\xdd%\xf0\xdcf \x0f\xce\xf1\xae\x94\xc2\xbcF \x05\t\xf0\xfc\xe5\x9c\xa5\xc1X\xc6\xe8\xdc$\xb8W>\xee \x03\xd64\x80r\xb8>\x13Q0\x17\xef\xf0P\x98\xaf1\\7\x1f\x9e\xa9\xa3\xbd\x88\xc05\xb1X\x08\xffo\xdd\xf6\xd7u\xde\x0f\xeb\xf6\xbd\xb5\x9a\x87}\x1a\x838\x98\xbf\xbd\xb0\x87\xe6\xe7\xd9X\xa7\xf9\xefD\x07\xba\xd0\x8c\\\xb8\xd6Z\xfd&\xe3a\x8f\\g\xbct\x98\xb71\xfd.|o}\xc6vO{:\x18\xd65\rS`\xee>\xbb\xa7\xb5T\xc0\xfe\xbb\xd6x\xbe\xf7l\xed\x8d\xef\xfd\xed\xe8\xff\xed\x99\xf9[\x93y\xe4\xc0\xde\x98\x83\xf3\x9dk\xcd1\xf0\xbc\xcc\xa1\x06\xc6\xce\x80\xeb\xfd\x7f\x15&\xc0\xbd|\xefwf\x0c\xff\xef{\xcf\xdcs\xf3\xf7d8G\xe6\xe0\xde\xae5\xb6\xb5%\x06\x8c\x95\x05\xcf,\x0c\xcf\xc6=\xec\x9f5\x9e\x80\xe7\xe7Z\xfb\x90\x06\xff?\x04\xf6"\x19\xae\xf5\xbd\xf9>\x07\xb2\xd7\xe9\xf1"""],
                    ['FKGG', """\x00\x00\x04hx\x015\xd3kl\x8eg\x18\xc0\xf1W\x1d\xab\xaa\x0e\xa5\xbaV\xcf\xad\x17m\r=8\xb4\x0e\xad\xa2\x0e\xa5>\x10\t\x1f\xac\xc9\xe2\xb8 >\x90\x98u=m\x04q(\x1b2[6\x93J\xb1Nb\xb6L|\x10\xa78\x9f\x97M\xb6\x91"\xfd\xe0\x10A\x84\x98\xf8\xff\x93gM~y\xde>\xcf\xfd\\\xd7}]\xd7\xfd\x84\xc2\xa1\x9e\x11M\xa9\xa1P(\n\x830>\xf8\xdd\x87kG\x84\xd1\x19\x15\x18\x88L\xc4!\x06\xb1\xc8FOL\xc30\xe4\xa0\x07\xc6 \x1a\xa5\x18\x8aI(F\x06\x92\xe13\xef\x99/\x12S\xf1\x0c\xe6\x9c\x81"t\x80\xeb}f\xccN\xb8\n\x9f\xbb\x1f\xdfu\xdd\x08\xb8\xa67|\'\x1e\xd3Q\x00k3\x86k\x8c\xed;\xae\xb5\x96<\x8c\x82\xefX\xef\x03\x98\xc7\xd8\xee;\x01\xd6g\x8e$L\x84\xcf\x8c\x9b\x0f\xefy\xb5\x96\x0fP\x8eYh\xc4\\4\xa0\x12\xeee\x08\xec\xaf1.\xc1\x9a\xd3a\x1e\xe3\xdbOc\xbb\x1f\xfb\xd3\x0e\xde\xb3\xa7\xbeS\x82D8\x8b^\xe8\x0f\xeb\xf5\xaf\x0b\x9c\x89{\xe8\x87)\x98\x0c\xfb\xe0\x1e}\xcf\x19\xac\xc2\x01\xfc\x8eZ\xdc\xc3\x15\x1c\xc2\'\x98\x8depv\xce\xf3\xff\xbd\x99\xdf\xdf\xf6.7\xb8\xfa|\x05\xd6\xa0\x0c\xcev4\\\xe7\xfb\xd6d^kr\xad\xb1w\xa0\n\xdeK\x87{\x1c\x0bg\x91\x83\x83\x18\x0ccy6&\xc0\xba\xaco!\xeec\x1fN\xe1\x08>\xc7q|\x8f\x7f\xb1\x13\xd6\xd7\x8c\xd3h\xc5Kx\xae~C=\xec\xa7\xf9\x9d\xbd\xef\x1e\xc6sl\xc1E<\xc6_X\x87r\xecB\x04\xac\xcd\xb37\x0e\xcee%\xf6\xe3<\xfe\xc4n\x98\xc3\xd8Y\xb8\x8b6X\x8f\xf3\xb2/_\xa0\t\xd6\x90\x86\xae\x18\x8e\xbe\x88\x85\xe7\xc6\xf731\x0f\xc7\xe0\xfa0\x9c\x9f}\xea\x0e\xcf\xc0\x97\xb0O\x03\x90\x8b\x19\xb0\xbf\xde\xf3\x0co\xc3^\xb8\xce|G\xb1\x15\xce\xd0|\x1b\xb1\t\xe6\xf5\x9c\xfb\xbb\x06\x0b\xe19*\xc1\x1e<\xc1\xdfp\xff\xb5\xc1\xf5c\xae\x17`m\x11(\x80=>\x0bs\xe6\xc3\xbdT\xa2=\xe2\xb1\x02oa\xbeTd\xc3\xf3;\x14\xd6[\x07\xe7\xea90\xf7-\x8c\x84ko\xc2z\xecu\x1f\x98\xf7$</\xe7\xb0\x1d\xf7\xe1\xfcG\xa1\x05\xaeM\x83ko\xe06\x9cq\x13\x9c\xb3\xfb\x99\t\xfb\x9f\x82\x05\xf0\xec8gk\xfa\x14\r\xf8\x06\xee\xc5<\x9e\r\xbf\xafB\x18+\x1a\xae3\xef;\xd8\xafnp\x16~WOq\x1dgp\x07G1\x1e\xab\xe1Y\xb1\x9f\xce\xee2|\xff\x04Z\xf1\x08\xf6q\x0e\xa6\xe3\x17,\xc6\x0b\x8c\x83\xe7\xc0\xfd\x1b\xfb\x08\xdc\x8355\xc3Y\x97\xc2>\xe6a\x1a^\xe1gT\xa3\x03|\xee\xfe\xd6\xa2=\xe2\xe0\x9e\x7f\xc5r\x98\xefk\x84Q\x8c\x9f\xb0\x04\xae\xcb\x80\xef\xfb\xedX\x8b\xfd0\x87\xb5\xfa\r\xfa=\x9b\xc3o\xcd\xfe\x95\xc1\xf9\xbb\xde\xff\xbbc\x10\x9c\xa9\xb1\x8c\xef\xda\x0b\xa8C!\xcckO^c#\\\x9f\x82\xcdX\x86Mp\x8f\xce\xb6+~@+\x1e\xa0?bq\x15~\x931p\x7f\xc6\xdc\x85Dx\xbe\xbf\xc2*x\xfe\xfa\xa2\n\xf6\xd2\xde:\xff\r\xf8\x08\x91\x88\xc2\xdb\x80\xeb\xac\xdb~\xfd\x07\xe7\xb8\x0e\xde;\x86\xf5\x98\x0f\x9f\x15\xc1\xef\xb3\x025\xf8\x0e\xee\xaf\x1a\xe6\xda\n\xf7\x95\x80l\xf8\xfd\xac\x851\xac\xcf\xb3\\\x0ck\xf0\x1c\xfc\x08\xd7\rC\x0b\xfe@*<\xb3\xe6?\x0e\xdf3\x865$\xc3\xf3\x9d\x84D\xb4\xc1\xb5\xf6\xcd=_B\t2\xe1\xfd\xc9\xc8\x82=u\x0f\x8b\x90\x0f\xe3\xf4\x80y\xad\xc5\xda]k\\\x7f\x17a\x0c\xf6\xe1\x1f\xd8\x13\xcf\xc2\x0e\xdc\xc1\xe9\xe0\xb7\xf3\xaf\xc5)|\x86f|\x8b\xe7\xb8\x8bF\x8c\xc4$\x98k6\x9c\xffC<\xc1\xb6\x80}\xde\x0b{W\n\xcf`\x17\xc4\xa1#\xdcK\x01\xd2`<\xf7g\x1d\x19\x18\x02\xfb\xea{\xb9\xc1\xffs\xb8\x16\xc25\xf6c f\xc1\xda\xecA=\x9c\xc3\xd8\xe0:\x95\xab1{\xc1\xde\xd9{\xfb\xb5\x14\xd5\x98\x87$$ \x0f\xe6\xb1\xa7S`\x8e\xdep\x8f\xf1pO\xc6\xb5\x06g\xecy\xf4|:#g}\r\x9d\x10\x05c\x99\xdbge\xc1\xff\xce\xc1\xbd\x9d\x87\xf1\xec]\x0c\\\x93\x03s:\xd3D\xb8\x07\xd9+{\xf3\x06\xbe_\x0e\xdf\xfd\x10\xed`\xcf\xbc\xef\x99H\x86\xf7\xed\xad\xb1\x8c\xef\x99\x9a\x800|\x16\x8dH\x18\xdb\xdc\xd6\x13\x8b\x14X\x83\xfb\xb6\xe6\xce\xb0\xcf\x8f\x82\xff=K\xf6\xc6\xb5\xc6JE:\xec\xa7\xf9\xad\xdb>\xbf\x07GO\xf5+"""],
                    ['ACMK', """\x00\x00\x04\xb0x\x015\xd4kl\x8dw\x1c\xc0\xf1\xa3\xd5P\xb4(J\xb58M\xa9R-m\xb5\xb4\xa6\xceZ\xbd(%\xeel\x92\r\x11\xcb\x10\x97\x17B\x88\xa22\x14\xa5\xb3\xb8$\xb6\xd55H\xb0d\xd2f\x19\x1b^\xc82\tb!\xcbd\x93,\xb3\x10q\xe9\x16\x04!\xbe\xdf\xe49\x92O\x9es\x9e\xfe/\xbf\xdb\x11\xca\x0eu\x8f\xb9;&\x14\nU\xa0\x1a\xa5\x88\xa0\x06\xe9\x18\x8d\x16\xa4\xa1\x12\xf1\xd8\x86"\xe4"\x0b\xf7\x90\x87X\x84\xd1\x171\x18\x15<\xc7\xf1\x9c\x10|v\xafg%\xa2\x16c\x03\t<]W\x8c\xf1pM9:\xa0\x1b"(\x08\x9e\x93x\xc6a\x10\xba\xe0&\xdc;\x02\xed\xd1\x07\x1d\xe1\x1d{\xe1=\xc6:\x04%0\xae\x0cx\x9e\xfb\xcd\xbf\x07\x86c$\x16\xc2xS\x91\x83|\xb8g"\xa6`6&\xa3:\xf8\xee{c\x8e\xc0\xba\xb8\xcfZyn/tB;\x14"\x19\xae\xf7\x99\x82L\xb8\xd68\x06 \x1a\xe7&>G\xcf\xb1\xb6a\x0c\x84\xf50\x8f\x06\x98\xdbv4\xa3\t\xe7q\x1b\xff\xe2,\xde\xe0\x11N\xe2>n\xa1\x0e\x7f\xc25\x17a\x9ee\xc13\x9e\xa75\xb4\'\xdei\x9c=a\x0e\xd9\xb0\xb6\xfe\xdd\x19\xe9\x0ckR\x01\xf3\xb4F\xf6n\x07\x96a\x1e\x9c\xa1\x99h\x81\xb5\xb2\x06Cq\x08\x8f\xb0\x12\x9e\xdf\rwa.\xd6\xc1\x9a\xff\x04s\xb2\xafYp\xa6\xd6\xa2\n\xce\x85\xf1\xd9\xbfDXCc\x9e\x05\xfb\xe7zk\xea\xd3\xd8\xedy\x18\xbe\x9b\x8f_P\x0fk\xf47\xdeb\x1d\xbeG#\x9c\x1f{\x16\x07\xeb\xf95<\xd7\xfd\x9e\xd7\x06\xd7:W/\xf0\x07\xbe\x821\xd8\xc3\x870ws\xfd\x04\xbe+B!\xcc\xf9\x1f\xd8\x8f\xff\xf1\x05>\x80u\xf0\xb7\xe6\xbd\xc3\xf0\x11vaA\xf0\xdd>\xed\x813\xea\xbd\xcd\xf0^{\xe2\x1cY\x13{c}\x9c\x13s\xef\x87\xd7\xd8\x0c\xe37\x9eVX\xb3t\\\xc7\x01\xd8\xffi\x98\x1c|v\xedR\\\x81g\'\xc1~\xbf\xc2Td\xa3\x07\xec\xbb\xb1\xbc\x83g\xe7\xc2\xdf\x8e\xfb.\xc3\xb5~?\x88\x93(\x813c=c\xe1\xb9~6\xe6\xde\xb0.G\xe0\x99\xd6\xde\xf7\xd6\xc3\xb9\xd8\x8f\xa70\xaf\x0e0f\xcf(\x863w\x18\xc6\xef\x1d\x05h\x803\xe5\xef5\x06\x99\x98\x8b_\xe1\xdf#p\xc6\x1a\xe1:\xe3\\\x0c\xe7\xf2%\xfa\xc3~\xec\x83u\x1d\x0c\xd7;\x1b\t\xb0\xef\x17`\xad*`L\xd5\xf8\x18\xb7\xe0>\xfb\x1aF\x1e"\xb0\x1em\xb0\xbf\xe6a-J\xe1\x8c\xd7a>\x8e\xa0/\x8e\xe3(\xac\xb3\xbd\xf9\x01\xab\x90\x01k\xe5<|\x8em\xf0_>6\xc1\xfc\xfe\xc3}\x98C\x18\xbfa#\xcc\xc1\xbd\xde\xe13\x11\xc7\xf0\x00s`\xbc\xe7`\x1f\xeaq\x18\xe6\xe7\xcc\x9dF{\xd4\xc0\x9e\x9d\x80qj\x0b\x9cMc\xb0ww\xb0\x1b\xce\x87\xfb\'\xe2\x1b\\\x81\xb5\xf0\xbb=\xfd\x19kq\x11)\xf0\xfd3\xb8n\x08\x92p\x06\xcbP\x0e\xfb\xfb\x17f!\x0c\xe3\xf2}+Z\xe0o\xd3\xf3\x7f\x87=\xf3\xfe\xe50?\xd7Va\r\xf6\xc2}S\xd0\x80\x87\xf0\xdd\x028\xf7\xee\xb1\xfe\xf1\x98\x84\xef0\x1b\xfe\xfe\xad]\x0c\xaa\xf1\x18\xeew\x9d}\xb2\x06M\x18\x8d\x04\x0c\xc5~\x98\xd7(\xac\x83k\xec\xbfu\x89\xae\xc9\xe2\xb3{\xac\xdfi|\n\xf3_\x04\xff\xff)B2\xac\xc3N\xdc\x80\xf3\xe2<\xaf\xc7)\xfc\x88\xabh\x86}L\xc3J\xb4\xe1\x12\xec\x91g]\xc6\x13x\x86w}\x8b\x970\xaf\xd5\xb0.\xe6\xd6\x8a\x03\x18\x08\xebn\xcf\xdf\xc1\xf3\xec\x95\xf1\xedC#zc\x00\x96\xe0\x05\xa6\xa2\x13\xcc/\x13\xd6\xcb\xb3\xeb1\x07\xee\xb5698\x03k\xec\x9de\xb0\'\x11L\x87y\xf8\xbd\x18\xd6p\x1ajQ\x03\xf7\x1b\x9b\xdf\x8d\xa3\x02\x89X\x05s1\xdekX\x01\xf7\xe7a\x1e\xecS)|\xe7\xba\xd78\x84\xad\xb0\x8eM\xf8\x0c\x13P\x80"X\x13?\xc7\xc1{\x93a?\x9d\xafv0\xc7\x0c\xc4\xa2+\\3\x1c\xd6m,:"\x8c>0\xa7\r8\x87{0o\xf3\xb1\xd7\x07\xf1\x1c\xe71\x0e\xe6\xe7~\xef\xb2\xc6\x11\xcc\x80k\xad\xa5\x7fs\xa6\xd3\xd0\x1d\xd6\xd3\xb8\x13\xe0\xfb\xce\xd8\x88\xcd\xf8\x12\xce\x98k\xad\xe5\x08\x18s\x04\xd6\xdf\xb8\xb2\xe1^\xf3\xf1i\x9f\xac[%\x8c\xd3\x1a$\xa1\x1f<\xcb\xdaxN!\\\xef\x0c\xf8\xf7r\x18\xaf=\xc9\x87g\x94\xc0u\xfe\x7f\xe1\xbd\xd6\xb0\'\xbc\xf7\r\xc2\xb0>\xb9\x18\x04\xd7x\xaf\xb1\xa4\xc0\x1a\xe6 =\xf8\xee~c\xf0>\xeb\x13\x8d\xcf:\x8c\xc7`x\x8e\xe7\xd7\xc2X?\x849\x18\xbf\xbd\xf3\x9d\xe7\xd9\xaf8x\xbf}\xcbB\xb4F\xf1|6\x16\xef\xf1~{\xe5\x99\xe6e\xff\xd2`\xee\xe6\xda\x1f\xc6\xe2\xdf\xedM/\xa4\xc2\xbaz\xbe1\xbf\x07Y\xfe\xf6,"""],
                    ['UXUC', """\x00\x00\x04\x9dx\x015\xd3{L\xd5e\x18\xc0qJEg\x04\x02r\xf1\x02\x1c P\xd0DQ\x11A\xe4\x80\xa8\x88\\jNW\xd9\xdcD\x9bw[\x97\x99\xf5G\xcb\x00\x1d\x14\xd1\xd4i\xe4\xe6\x8d\xd4\x8c\xb5\xca[9\xad\xe9\xd06\xd1\xf22s\xc5\xbaH9\xca\xe9\xdc\xb2en\xd5\xd6\xf7\xbb\xcea\xfb\xecw\xf8\x9d\xf7}\xde\xe7}\x9e\xe7D\xe4F\xc4>\xd8=*\xe2\xff\xbf\x1a\x1eUx\x18\x130\x0c\xd5(C\x14\\\xd7\x8b\x01\x88\xc5T\x14\x85\x9e\xd9<\xd31\x12\x91\x08\xa02\xf4\xac\xe59\x1b3q!\xf4\xf9\x1f\x9eC0\x06\xa3\xe1\xde\x1dx\x08\xc5\xf0}\x0c\\\xe3;\x9fsQ\x1a\x92\xc2s\x1f\xc6a2\xc6c\x16\xea`^\xae\xf3.\xee\x89F!<\x7f\x12\xfa\xc1w\xc64\x7f\xefe\xce~g\x9c2\xa4b \xbc\xc3 X\x87/\xe1\xb9\xc6\x99\x03c\xf8\xbf{\xcd#\x1e\xe6l\xeec\xe1\xde\x19\xf0\x0c\xd7\x05Q\x81ZL\x83\xe7\x9a\xaf\xb1\xcc\xbd?\xcc\xc9\xfc\xadw\t\xfc\x8bC\x16\xfc>\x1bCQ\x0e\xdf'\xc2\xbby\x861<'\x13I0\x8f%X\x8a\xf9x\x1a\xd6\xc4>O\xc1D\xb8\xb6\x01\xcd8\x86\xf71\x1d\xcf\xe2:v\xe20r1\x02\x9f\xa3\x1e\xe6\xe6\x99\xce\x89w0\xfe\xe3\xf0\x9dO\xeb\xe1zs\x0c\xc0u\xf3P\x00\xeb\x1b\x84upo#Zq\x14\xdbq\x0e\x9d\xa8\x805\xf2\xbe\xeeqf\x1eE::\xd0\x8e>\xcc\x80\xf9\xecE\x0b\xcc\xff+l\xc5\xcf\xb8\x8cC\xf8\t\xce\x98{}\xff;\xae\xe0e\xac\xc5j4\xe1{\xbc\x886|\x81m\xd8\x8cW\xe0<\rG\x0c\xccc!\xbc{\x02\xf2\xb1\x18\xff\xc2\xfe[\xdf\x1eX\xbf30O\xf7y\xdf\xe7\xb0\x1c\xae\xb3\xdf\x83\xf1-~\x80\xf3\xe5{\xcf\xbf\x8748#\xef\xc1\xbcN\xc2;\x8e\xc6%\x18\xcf=7\xe1\xfc>\x80\xd7\xd0\x8d}\xb0\xdf+\xf0\x14\x92\xe1Y\xf6\xe2\x1b\x18\xbb\x02\xf6\xfdc\x1cG%\xec\xcdg\xf8\x05\xde\xfb*\xdc\x9b\x0b{Y\x8f\x14d\xe0\x04\x8e\xc0\xfb;s[\xd0\x0b\xeb\x10\x89Dta\x1d>\xc2Ex\xa6\xbd\xf4\xbc\x1bhG+\xcck2Ra?\xac\xe7]\xfc\x8d\x91\xd8\x85\xefp\x1fY(\xc5\x078\x8fE\xf8\x03\xab\xe0\xef(\x07\xd5\xb0Nk\xe0\xd9\xf6\xd1\xfb\xf9g,\xefm\x8f\x8dc\x7f\xac\xd7[0f\x07\na\xae\xd6\xc6\xfc\xfc]\x05\xe0\x1c\x94\xa0\x00\xce\xc3\xab0\xcfG`\x8dvc'\x8e!\x88N\x18\xf7\x1d8\xd3\x9bp\x0f\xf63|\x865?\n\xf3\xbc\x06\xebc\xec\xad8\x83\xbd\xb0\xdei\xb8\x02\xf3\xfb\x11{\x10\x03\xeb\xe6{c\xff\tg\xa1\n\xf6k:\xbc\xc7J\x1c\x84\xb9\x9b\xc7Y8\xef\xcd\xf0<\xff.\xc3>\xc4a-\xbe\xc6\xa7x\x03\xc6\xf4;\xff\xb7\x8f\xde/\x19\xbe\xdf\x8f\xd3\xb8\x83\x89p\x86\xed\xc5F\x18\x7f=\x82(\xc2)\xd8+\xf7{F=\xe6 1\xc4\xcf\xbf\xa2\x00\xf9h\xc2},\xc3LL\xc2%,\x85\xbd\xfb\x10\xd7`\x0f\xd3\x91\x80\x1c8W]x\x17\xf6&\x0f\xce\xaau\xbe\x05c\x1b\xef \x1a\xb0\x18\xde\xff1\xd4\xe1\tl\x83\xfb\x9f\xc7l,\x81\xf7s\xb6\x8d\xe7\x1cmF\r\xec\xbd1\xa7 \x1e\x1b\xd0\x02\xd79#\xe7\xe0L\xda\x0f\xbf{\t\xa9\xf0\xfbO\xe0\xd9+\x10\x8bgp\x16/\xc0\x99\x8dCo\xe8\xb3\xbf\x05s}\x1b\xe69\x0c\xe3P\x8e\xbf\xd0\x06\xebb\xfd\x9c\xff\xa9\x98\x06\xf7\x1c\x87\xb5=\x80\x1el\x82\xef\xcd\xc9\xf5ep\x96\x9c\x07\xf9;\xf67>\x06\xde\xdb3\xf6\xe0.\x8c\x1b\xc0`x/{\xeb\xec\xbd\x89 \na\xcd\xac\xd1Ul@#\x9aq\x1b\xf6\xcf\xba\r\x85g\x1a{\x04\xecc-\x96\xc1\xbe,\xc7\x02\xd8C\xd7d`\x11V\xc3\xb9x\x1d\xf6\xf4\x06\xfa\xd0\tk{\x08\xeb\xe1\xbb\xdf\xd0\x0eks\x11\xf6\xc5\xbb\x06\x10\x05\xfb\xe0,L\xc0\x1al\xc4:,\xc4X\x84\x7f3Y|\xb6.\xde\xd5\x1a{\xc7\xb9\xb0\xce\xb2N\xfeo\xadbP\x8c\x1cT#\x08\xf7y\x86\xf7\xb56\xeeq\x9e=\xc3\xfa\xbb\xb7\x15u\x08\xc2}\xceT9\x86\xc39\xf0\\g$\x13\tp\xaf\xdfy\x87\x0c\x18\xe7\x14\xaa\xe0\xfbQ0\xcfd\xb8\xdewyp\xbfsS\tc:\xb7\xee\r\xc2\xf5\xce\x84\xe7z\xf7HX\x1f{\xe3\xfd\x07`\x10\xec\x89\xbf\x7f\xd7\xf7\x83\xf9z\x1f\xe7\xcdZ8\x1b)0\x17\xefZ\x03\xcf3\x9e\xf1\xb3C\xff\x1b\xdb\xfc\x8c\xf7$\\o-\x9c\xf5p\x9d=#\t\xf6\xd6\xb8\xde\xdb3\xfdl=\xac\xa9\xb5\x0e\xe7k\x0c\xe7\xc8\x1exV4\x06b\x08\xc2\xf52'\xd7\xe5\xc2\xbb;\xd3\x15hB\x7f\xb8\xde\x9c\xff\x036n\xff\x0c"""],
                    ['AWRG', """\x00\x00\x05\x1dx\x015\xd4{L\x95e\x1c\xc0\xf1\x03(\xa2\x10\x88\x9a\xe2\r\x0e\xa8\x84\\\xc4\xbb"$\x1co\x89 \xd4&ce\x7f\xb9e\x19\x99VV\xde\x9aF\x85\xe4DfI\x89N\x9dT\x14)\xa1\xb5\xac?\xd2rf:u\xa6\x95\x9a\x97.\xea\xe6\xe6\x1fNm\xba\xb1V\xce\xefw{a\xfb\xec}\xcf{\x9e\xf7\xf9\xdd\x9eC(?\x94\x1c\x93V\x14\n\x85\xc2x\x0c\xe5\xc8\xc1l\x0c\x82\xdf%\xa17\xd2\xf1(\xa6"\x06\x17\x91\x8cx\x14\xa0\x0fz\xc1g\xe3\x10\x8bY(\xc6$\xa4\xc1w]\x1b\x85,d#\x1fs1\x01\xa9\x81\x1e\xc1\xb3\x11\\]?\x1c\xc6\xf1\xbd\xf1\x98\x821\x88\xc60\x94\xc0g\xeeg\x1d5\xb8\x15|\x9e\xc9\xd5\x9c\n\x91\x07?[\x93\xcf\xack2\xba\xc1\xba\xfd\xb3v\x9f%\xc0\xfc\xed\x83\xfbZ\x8f\xeb#p/{\x93\x11|\xb6\xee\xa10o\xd7ZO%\xea\xf1<\xaa\xe1\xfa9x\x08\xe6>2\xb8\xda\x9b\x12|\x85=8\x85\xcd\xf8\x14e0F.\x06\xc2\xda\xed\x9b}\xb4W\xf6\xc3\xe7)\x88\x83=\xf0\xcf<\xfb\xc19\x98\xcb64c1\xe6\xc3g\xce%\x0c\xfbj\xae\xc6\xa8\xc2\xf7h\xc5i\xdc\xc75\x98[\x13\xec\x8d\xf1]o\x0ea\xac\xc6.8#g1\x03G\xb1\x01\xf6o,\x12a\xcf\x9d\x8d\xf9Z\xd3t\x98o&.\xe3\x1d\xf4\x85{D\xb0\x1e?\xe0\x00\xcc\xc95\xc7q\x06\xc6\xb7\xdf\xd61\x11\xefb?\x1a`]\xf6\xbaK\x98\xfb\xb7a\xacM\xf0]{\x93\x86_\xb1\x11\xd3\xe0s\xebk\x84\xb1<\xeb\xe5\xb0N\xe3\x18\xcf3\xea\xbds\xf4\x1dg\xa8\xfc\x80\xb5\xbc\x8av\xf8\xbe3\x1a\x00\xf7\xa8\xc0J\x1c\x83}\x91\xfd\xf8\x07\xee\xe5\xb9t\xcd\x1d\xb4\xe0\n\x86\x04\xf7\xf3\xb8z>KQ\x80\xa7`\x8e\xe6\xecY\xb4gq8\x85}p\xde\x1d\xa8\xc5\x0e\x1c\xc12\xdcD\'~G\x1b\xea\xf0\x1b\xd6\xc0\x1e\xbf\x8e\xed\xb0\x1ek1\x97\xbb\xb0\xc7\xc6\xfe\x0b/\xe1 \x9eC\r\x9cw2\x8c\xb5\x05\xf6\xf3\x7f\x9c\x801\xac\xad\x0c\xf10\xcf\xe5\xb8\x07g=\x02\xf6\xca:\xa3a\x0e\x1f\xc2\xb3j\x9f\x17c7\xdc\xc73a\x1c\xf3\xbd\x1f|.\xe6j\xdf\x0e\xe1;\xb4b\x1c<c\x9b\xe1\xde\xe9H\xc4\n\xd8/\xffO\x99\xbfy\x0c\xc6\xe3\xf8\x03\xbf\xc0Y\xbc\x0f\xcf\xae\xbf?\xcfC\x02\x9c\xa5}\xdf\x07go\xbe\xd9p\x9d{\xda\xab7\xf1\x13n\xc3\xba<;\xd6c\x1e\x7f\xc3<\x17a\x13\xeco\t\x16\xe2\x1c\\s\x12\xbd\x90\x03{\xf81\xc6\xc3|\x8f\xa2\x1aypv\xeec\x9d\xb3\xd0u\x0e\xac\xc5\xcf\xe6\xe9\x1c\xab0\n\xe6\xe9}\x1d\\\x93\x04\xf7\xf5\xde\xd9\xb9\x9f=:\x8b\x9b\xc8@,\xb6`\x0fF\xc3\x9cr\xf1/\x8aP\x88\x1bhB+\x9c\x99\xb9\xd9\x17\xbf\x9f\x80\x12\xec\xc5-\x98S\x02\xd6\xe3#\x98\xbbk\xea\xf1\'\xec\xbf\xeffa\x03\x9e\x859y\xee\x9c\x7f#\xdc7\x05\xef\xa1\x01\xe7a\xcc\xbe0\xbe\xb99\xaf\x9e\xf8\x1a\xa5\x98\x83\x08\xfa\xc3\xd9\xd9\x9f\xebp\xd6\xce\xfd3\xac\x82\xe7\xc3XmH\x85\xefZ\xff1x\xc6*1\x17]\xe7n*\xf7\x93\xb1\x13\xb5(\x83\xf5|\x8b\x85p\x8e\x03\xb1\x04\xeek\xed\xc6;\x8dv\x9c\x81\xef8\x9f*\xac\xc3\x0b\x88B\x0b\\\xff"\xd6\xc0>\xacE\x12\x8c\xd5\x8c\'\xd1\x84\x1d\xf0\xf9#x\x0b\xcb`\x1e\x03\xf0\x1f\x96\xc2\x9a\xdd\xc3\xbe\xef\x82{\xf8\xfd4x\xae\xed\xa9yt\xe2\tT\xc0\x9ck\xf0\x06\x1a\xf12^\x81=x\x1a\xc6\xd9\x86\xc3\xf82\x90\xc9\xb5\x12\xce\xc9\xb3{\x00\xc9\x98\x02\xeb2\x97\xcfa?\xed\x85g\xfa2\xc2\xb8\x81\x0b\xf0wc_{\xc2\xffq\xe5\xb8\x02\xcf\xebZ\xd8_{r\x04\x17a\xec/\xd0\x00\xcfN4\xf2\xe0z\xf7\xf1|\x1bo$\x86\xc1\xb9zF\xa6\xc3:\xf7\xa2\x0e\xc6\xf3\xdd\x1c\x98\xd7Ux\xae\x86\xc3Y\x7f\x00c\x0c\x81g\xbf#\xf8|\x89\xeb\t\x9cC-6\xe2\x1b\xcc\x873q6\xddp\x10\xf6\xc1\x9a\xd6\xe1g,B5\x9c\x81\xf3\x18\x84T\xa4a(\x9c\xa3\xef\xf4\xc0`X\xcb\xc3\x18\x0b\xcf\x8e\xf5Y\xfb$\xf8{\xf2\xfd\xad\x01\xbf\x8b\xc03X\x0f\xf3\xe9\x8eD\xd8\x8b\\\xec\xc6hX\xa3\xbf\x93\x05p\xb6\xe9\xf0\xb99xv\xec\x8b\xf9\xd9\xa3\xde\xb0\x9e8\x18s\x0c\x9cy!\xdc\xc3^\xf9\xbe\xbdvM\n\xdc\xc3x\xe6nO}f^\xc6kF;:\xf1\x1a\xda`\xffw\xe2$\x96\xc0\xb3\x18\x05\xfb2\n\xce\xc0\xfa\xdc\xc7g~\xde\x8f\x16Xc\x16\\o\xbe\x9e\x05g\x10\x1b\xf0\\\x18\xdb\xdc\xed\xa1\xdf\xcd\x84\x7f\xeee\xee\xd6\xf8#>A\x7f\xc4\xc0^t\xc0\xdf\xb53qf^\xfd\xbd\x18#\x12\\\xddw6\xe6!\x13\xf6\xdb\xf9\xb9g1\xec\x833v\xbfg`\xee\xf9\xb07Epm9\xfa\xc0\xbd\x9c\xadu\xfa\x8e1\xcc\xc5~x\xef3c\x18_\x19(\r\xee\x8d\xeb\x9c\xac\xd7g\tp>\xc65?\xe7\xe4_\x01\xfa\xc1\xfe8c\xfbk_\xfc\xde>\xcd\x805g\xc3^9\xbf\x8a@<W\xf7\xb7\x0f\xd6\xe7o\xca\xfe[\x8b\xb9\x1b\xd3<\x8d\xef\xf9\xf0={m\x0e\xd6\xe0\xfe\x0f\x00\x89l\x0b\xdc"""]
 
                ]
                captcha = random.choice(codes)
                this.client.currentCaptcha = captcha[0]
                this.client.sendPacket(Identifiers.send.Captcha, ByteArray().writeBytes(captcha[1]).toByteArray())
                return

            elif CC == Identifiers.recv.Login.Dummy:
                if this.client.awakeTimer.getTime() - _time.time() < 110.0:
                    this.client.awakeTimer.reset(120)
                return

            elif CC == Identifiers.recv.Login.Player_Info:
                return
            elif CC == Identifiers.recv.Login.Player_Info2:
                return

            elif CC == Identifiers.recv.Login.Temps_Client:
                return

            elif CC == Identifiers.recv.Login.Rooms_List:
                mode = packet.readByte()
                this.client.lastGameMode = mode
                this.client.sendGameMode(mode)
                return

            elif CC == Identifiers.recv.Login.Undefined:
                return

        elif C == Identifiers.recv.Transformation.C:
            if CC == Identifiers.recv.Transformation.Transformation_Object:
                objectID = packet.readShort()
                if not this.client.isDead and this.client.room.currentMap in range(200, 211):
                    this.client.room.sendAll(Identifiers.send.Transformation, ByteArray().writeInt(this.client.playerCode).writeShort(objectID).toByteArray())
                return

        elif C == Identifiers.recv.Informations.C:
            if CC == Identifiers.recv.Informations.Game_Log:
                errorC, errorCC, oldC, oldCC, error = packet.readByte(), packet.readByte(), packet.readUnsignedByte(), packet.readUnsignedByte(), packet.readUTF()
                if this.server.isDebug:
                    if errorC == 1 and errorCC == 1:
                        print "[%s] [%s][OLD] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), this.client.playerName, oldC, oldCC, error)
                    elif errorC == 60 and errorCC == 1:
                        if oldC == Identifiers.tribulle.send.ET_SignaleDepartMembre or oldC == Identifiers.tribulle.send.ET_SignaleExclusion: return
                        print "[%s] [%s][TRIBULLE] GameLog Error - Code: %s error: %s" %(_time.strftime("%H:%M:%S"), this.client.playerName, oldC, error)
                    else:
                        print "[%s] [%s] GameLog Error - C: %s CC: %s error: %s" %(_time.strftime("%H:%M:%S"), this.client.playerName, errorC, errorCC, error)
                return

            elif CC == Identifiers.recv.Player.Ping:
                if (_time.time() - this.client.PInfo[1]) >= 5:
                    this.client.PInfo[1] = _time.time()
                    this.client.sendPacket(Identifiers.send.Ping, this.client.PInfo[0])
                    this.client.PInfo[0] += 1
                    if this.client.PInfo[0] == 31:
                        this.client.PInfo[0] = 0
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Type:
                type = packet.readByte()
                this.client.shamanType = type
                this.client.sendShamanType(type, (this.client.shamanSaves >= 100 and this.client.hardModeSaves >= 150))
                return

            elif CC == Identifiers.recv.Informations.Letter:
                playerName = Utils.parsePlayerName(packet.readUTF())[:-5]
                type = packet.readByte()
                letter = packet.readUTFBytes(packet.getLength())
                idler = {0:29,1:30,2:2241,3:2330,4:2351}
                
                if this.server.checkExistingUser(playerName):
                    id = idler[type]
                    count = this.client.playerConsumables[id]
                    if count > 0:
                        count -= 1
                        this.client.playerConsumables[id] -= 1
                        if count == 0:
                            del this.client.playerConsumables[id]
                            if this.client.equipedConsumables:
                                for id in this.client.equipedConsumables:
                                    if not id:
                                        this.client.equipedConsumables.remove(id)
                                None
                                if id in this.client.equipedConsumables:
                                    this.client.equipedConsumables.remove(id)

                    this.client.updateInventoryConsumable(id, count)
                    this.client.useInventoryConsumable(id)
                    
                    player = this.server.players.get(playerName)
                    if (player != None): 
                        p = ByteArray()
                        p.writeUTF(this.client.playerName)
                        p.writeUTF(this.client.playerLook)
                        p.writeByte(type)
                        p.writeBytes(letter)
                        player.sendPacket(Identifiers.send.Letter, p.toByteArray())
                        this.client.sendLangueMessage("", "$MessageEnvoye")
                    else:
                        this.client.sendLangueMessage("", "$Joueur_Existe_Pas")
                else: 
                    this.client.sendLangueMessage("", "$Joueur_Existe_Pas")
                
                return

            elif CC == Identifiers.recv.Informations.Letter:
                return

            elif CC == Identifiers.recv.Informations.Send_self:
                this.client.sendPacket(Identifiers.send.Send_self, 1)
                return

            elif CC == Identifiers.recv.Informations.Computer_Info:
                return

            elif CC == Identifiers.recv.Informations.Change_Shaman_Color:
                color = packet.readInt()
                this.client.shamanColor = "%06X" %(0xFFFFFF & color)
                return

            elif CC == Identifiers.recv.Informations.Request_Info:
                this.client.sendPacket(Identifiers.send.Request_Info, ByteArray().writeUTF("http://195.154.124.74/outils/info.php").toByteArray())
                return

        elif C == Identifiers.recv.Lua.C:
            if CC == Identifiers.recv.Lua.Lua_Script:
                this.client.sendMessage("<r>Forbidden</r>")
                return

            elif CC == Identifiers.recv.Lua.Key_Board:
                key, down, posX, posY = packet.readShort(), packet.readBoolean(), packet.readShort(), packet.readShort()


                if this.client.isFlyMod and key == 32:
                    this.room.bindKeyBoard(this.playerName, 32, False, this.room.isFly)
                
                if this.client.isFFA and key == 40:
                    if this.client.canSpawnCN == True:
                        if this.client.isMovingRight == True and this.client.isMovingLeft == False:
                            reactor.callLater(0.2, this.client.Utility.spawnObj, 17, posX - 10, posY +15, 90)
                        if this.client.isMovingRight == False and this.client.isMovingLeft == True:
                            reactor.callLater(0.2, this.client.Utility.spawnObj, 17, posX + 10, posY +25, 270)
                        reactor.callLater(2.5, this.client.Utility.removeObj)
                        this.client.canSpawnCN = False
                        reactor.callLater(1.3, this.client.enableSpawnCN)

                elif this.client.room.mapCode == 20001:
					if this.client.posX >= 789 and this.client.posX <= 911 and this.client.posY >= 354 and this.client.posY <= 356:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
					elif this.client.posX >= 962 and this.client.posX <= 1049 and this.client.posY >= 274 and this.client.posY <= 276:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
					elif this.client.posX >= 1615 and this.client.posX <= 1705 and this.client.posY >= 246 and this.client.posY <= 247:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
					elif this.client.posX >= 277 and this.client.posX <= 347 and this.client.posY == 193:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
					elif this.client.posX >= 1752 and this.client.posX <= 2060 and this.client.posY >= 355 and this.client.posY <= 363:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(8, this.client.sendFishingCount)

		elif this.client.room.mapCode == 20002:
                    if this.client.posX >= 638 and this.client.posX <= 721 and this.client.posY >= 43 and this.client.posY <= 53:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
                    elif this.client.posX >= 647 and this.client.posX <= 734 and this.client.posY >= 336 and this.client.posY <= 338:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
                    elif this.client.posX >= 300 and this.client.posX <= 738 and this.client.posY >= 293 and this.client.posY <= 335:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
                    elif this.client.posX >= 200 and this.client.posX <= 256 and this.client.posY >= 182 and this.client.posY <= 186:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(5, this.client.sendFishingCount)
                    elif this.client.posX >= 41 and this.client.posX <= 129 and this.client.posY >= 331 and this.client.posY <= 353:
						if this.client.isEvent and key == 32:
							this.client.sendPlayerEmote(11, "", False, False)
							reactor.callLater(8, this.client.sendFishingCount)
                        
                if this.client.isSpeed and key == 32:
                    this.client.room.movePlayer(this.client.playerName, 0, 0, True, 50 if this.client.isMovingRight else -50, 0, True)
                if this.client.room.isFlyMod and key == 32:
                    this.client.room.movePlayer(this.client.playerName, 0, 0, True, 0, -50, True)
                if this.client.isFly and key == 32:
                    this.client.room.movePlayer(this.client.playerName, 0, 0, True, 0, -50, True)

                if this.client.room.isDeathmatch and key == 3:
                    if this.client.room.canCannon:
                        if not this.client.canCN:
                            this.client.room.objectID += 1
                            idCannon = {15: "149aeaa271c.png", 16: "149af112d8f.png", 17: "149af12c2d6.png", 18: "149af130a30.png", 19: "149af0fdbf7.png", 20: "149af0ef041.png", 21: "149af13e210.png", 22: "149af129a4c.png", 23: "149aeaa06d1.png"}
                            #idCannon = "149aeaa271c.png" if this.client.deathStats[4] == 15 else "149af112d8f.png" if this.client.deathStats[4] == 16 else "149af12c2d6.png"
                            if this.client.isMovingRight:
                                x = int(this.client.posX+this.client.deathStats[0]) if this.client.deathStats[0] < 0 else int(this.client.posX+this.client.deathStats[0])
                                y = int(this.client.posY+this.client.deathStats[1]) if this.client.deathStats[1] < 0 else int(this.client.posY+this.client.deathStats[1])
                                this.client.sendPlaceObject(this.client.room.objectID, 17, x, y, 90, 0, 0, True, True)
                                if this.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                    if not this.client.deathStats[3] == 1:
                                        this.client.room.sendAll([29, 19], ByteArray().writeInt(this.client.playerCode).writeUTF(idCannon[this.client.deathStats[4]]).writeByte(1).writeInt(this.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                            else:
                                x = int(this.client.posX-this.client.deathStats[0]) if this.client.deathStats[0] < 0 else int(this.client.posX-this.client.deathStats[0])
                                y = int(this.client.posY+this.client.deathStats[1]) if this.client.deathStats[1] < 0 else int(this.client.posY+this.client.deathStats[1])
                                this.client.sendPlaceObject(this.client.room.objectID, 17, x, y, -90, 0, 0, True, True)
                                if this.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                    if not this.client.deathStats[3] == 1:
                                        this.client.room.sendAll([29, 19], ByteArray().writeInt(this.client.playerCode).writeUTF(idCannon[this.client.deathStats[4]]).writeByte(1).writeInt(this.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                            this.client.canCN = True       
                            this.canCCN = reactor.callLater(0.8, this.client.cnTrueOrFalse)        
                if this.client.room.isDeathmatch and key == 79:
                    this.client.sendDeathInventory()
                if this.client.room.isDeathmatch and key == 80:
                    this.client.sendDeathProfile()
                    
                if this.client.room.isFFARace and key == 3:
                    if this.client.canCannon:
                        itemID = random.randint(100, 999)
                        if this.client.isMovingRight:
                            reactor.callLater(0.2, lambda: this.client.room.sendAll(Identifiers.send.Spawn_Object, ByteArray().writeInt(itemID).writeShort(17).writeShort(posX + -5).writeShort(posY + 15).writeShort(90).writeShort(0).writeByte(1).writeByte(0).toByteArray()))
                        else:
                            reactor.callLater(0.2, lambda: this.client.room.sendAll(Identifiers.send.Spawn_Object, ByteArray().writeInt(itemID).writeShort(17).writeShort(posX - -5).writeShort(posY + 15).writeShort(-90).writeShort(0).writeByte(1).writeByte(0).toByteArray()))
                        reactor.callLater(2.5, lambda: this.client.sendPacket(Identifiers.send.Remove_Object, ByteArray().writeInt(itemID).writeBoolean(True).toByteArray()))
                        this.client.canCannon = False
                        reactor.callLater(1.3, setattr, this.client, "canCannon", True)
                return
            
            elif CC == Identifiers.recv.Lua.Mouse_Click:
                posX, posY = packet.readShort(), packet.readShort()
                if this.client.isTeleport:
                    this.client.room.movePlayer(this.client.playerName, posX, posY, False, 0, 0, False)

                elif this.client.isExplosion:
                    this.client.Utility.explosionPlayer(posX, posY)
                return

            elif CC == Identifiers.recv.Lua.Popup_Answer:
                popupID, answer = packet.readInt(), packet.readUTF()
                return

            elif CC == Identifiers.recv.Lua.Text_Area_Callback:
                textAreaID, event = packet.readInt(), packet.readUTF()
                ## Menself Menu System ##
                if event in ["lbileri","lbgeri","lbkapat"]:
                    this.client.lbSayfaDegis(event=="lbileri",event=="lbkapat")
                    return 
                if event == "closed":
                    this.client.sendPacket([29, 22], struct.pack("!l", 7999))
                    this.client.sendPacket([29, 22], struct.pack("!l", 8249))
                    
                    
                if event == "fechar":
                    this.client.sendPacket([29, 22], struct.pack("!l", 10050))
                    this.client.sendPacket([29, 22], struct.pack("!l", 10051))
                    this.client.sendPacket([29, 22], struct.pack("!l", 10052))
                    this.client.sendPacket([29, 22], struct.pack("!l", 10053))


                elif event == "fecharPop":
                    this.client.sendPacket([29, 22], struct.pack("!l", 10056))
                    this.client.sendPacket([29, 22], struct.pack("!l", 10057))
                    this.client.sendPacket([29, 22], struct.pack("!l", 10058))

                        

                
                ## End Duxo Menu System ##
                    
                if event.startswith("fechadin"):
                    for x in range(0, 100):									
                        this.client.sendPacket([29, 22], ByteArray().writeInt(x).toByteArray())
                        
                if textAreaID in [8983, 8984, 8985]:
                    if event.startswith("inventory"):
                        event = event.split("#")
                        if event[1] == "use":
                            this.client.deathStats[4] = int(event[2])
                        else:
                            this.client.deathStats[4] = 0
                        this.client.sendDeathInventory(this.client.page)

                if textAreaID == 123480 or textAreaID == 123479:
                    if event == "next":
                        if not this.client.page >= 3:
                            this.client.page += 1
                            this.client.sendDeathInventory(this.client.page)
                    else:
                        if not this.client.page <= 1:
                            this.client.page -= 1
                            this.client.sendDeathInventory(this.client.page)

                if textAreaID == 9012:
                    if event == "close":
                        ids = 131458, 123479, 130449, 131459, 123480, 6992, 8002, 23, 9012, 9013, 9893, 8983, 9014, 9894, 8984, 9015, 9895, 8985, 504, 505, 506, 507
                        for id in ids:
                            if id <= 507 and not id == 23:
                                this.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                this.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 9009:
                    if event == "close":
                        ids = 39, 40, 41, 7999, 20, 9009, 7239, 8249, 270
                        for id in ids:
                            if id <= 41 and not id == 20:
                                this.client.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
                            else:
                                this.client.sendPacket([29, 22], ByteArray().writeInt(id).toByteArray())

                if textAreaID == 20:
                    if event.startswith("offset"):
                        event = event.split("#")
                        if event[1] == "offsetX":
                            if event[2] == "1":
                                if not this.client.deathStats[0] >= 25:
                                    this.client.deathStats[5] += 1
                                    this.client.deathStats[0] += 1
                            else:
                                if not this.client.deathStats[0] <= -25:
                                    this.client.deathStats[5] -= 1
                                    this.client.deathStats[0] -= 1
                        else:
                            if event[2] == "1":
                                if not this.client.deathStats[1] >= 25:
                                    this.client.deathStats[6] += 1
                                    this.client.deathStats[1] += 1
                            else:
                                if not this.client.deathStats[1] <= -25:
                                    this.client.deathStats[6] -= 1
                                    this.client.deathStats[1] -= 1
                    elif event == "show":
                        if this.client.deathStats[3] == 1:
                            this.client.deathStats[3] = 0
                        else:
                            this.client.deathStats[3] = 1
                    this.client.sendDeathProfile()

                    
                if event == "closeRanking":
                        i = 30000
                        while i <= 30010:
                            this.client.room.removeTextArea(i, this.client.playerName)
                            i += 1
                return

            elif CC == Identifiers.recv.Lua.Color_Picked:
                colorPickerId, color = packet.readInt(), packet.readInt()
                try:
                    if colorPickerId == 10000:
                        if color != -1:
                            this.client.nameColor = "%06X" %(0xFFFFFF & color)
                            this.client.room.setNameColor(this.client.playerName, color)
                            this.client.sendMessage("<font color='"+color+"'>" + "İsminizin rengi başarıyla değiştirildi." if this.client.langue.lower() == "tr" else "You've changed color of your nickname successfully." + "</font>")
                    elif colorPickerId == 10001:
                        if color != -1:
                            this.client.mouseColor = "%06X" %(0xFFFFFF & color)
                            this.client.playerLook = "1;%s" %(this.client.playerLook.split(";")[1])
                            this.client.sendMessage("<font color='"+color+"'>" + "Farenizin rengini başarıyla değiştirdiniz. Yeni renk için sonraki turu bekleyin." if this.client.langue.lower() == "tr" else "You've changed color of your mouse successfully.\nWait next round for your new mouse color." + "</font>")
                    elif colorPickerId == 10002:
                        if color != -1:
                            this.client.nickColor = "%06X" %(0xFFFFFF & color)
                            this.client.sendMessage("<font color='"+color+"'>" + "İsminizin rengini başarıyla değiştirdiniz. Yeni renk için sonraki turu bekleyin." if this.client.langue.lower() == "tr" else "You've changed color of your nickname successfully.\nWait next round for your new nickname color." + "</font>")
                except: this.client.sendMessage("<ROSE>" + "Renginizi Başarıyla Değiştiniz." if this.client.langue.lower() == "tr" else "Incorrect color, select other one.")
                return
            
        elif C == Identifiers.recv.Cafe.C:
            if CC == Identifiers.recv.Cafe.Mulodrome_Close:
                this.client.room.sendAll(Identifiers.send.Mulodrome_End)
                return

            elif CC == Identifiers.recv.Cafe.Mulodrome_Join:
                team, position = packet.readByte(), packet.readByte()

                if len(this.client.mulodromePos) != 0:
                    this.client.room.sendAll(Identifiers.send.Mulodrome_Leave, chr(this.client.mulodromePos[0]) + chr(this.client.mulodromePos[1]))

                this.client.mulodromePos = [team, position]
                this.client.room.sendAll(Identifiers.send.Mulodrome_Join, ByteArray().writeByte(team).writeByte(position).writeInt(this.client.playerID).writeUTF(this.client.playerName).writeUTF(this.client.tribeName).toByteArray())
                if this.client.playerName in this.client.room.redTeam: this.client.room.redTeam.remove(this.client.playerName)
                if this.client.playerName in this.client.room.blueTeam: this.client.room.blueTeam.remove(this.client.playerName)
                if team == 1:
                    this.client.room.redTeam.append(this.client.playerName)
                else:
                    this.client.room.blueTeam.append(this.client.playerName)
                return

            elif CC == Identifiers.recv.Cafe.Mulodrome_Leave:
                team, position = packet.readByte(), packet.readByte()
                this.client.room.sendAll(Identifiers.send.Mulodrome_Leave, ByteArray().writeByte(team).writeByte(position).toByteArray())
                if team == 1:
                    for playerName in this.client.room.redTeam:
                        if this.client.room.clients[playerName].mulodromePos[1] == position:
                            this.client.room.redTeam.remove(playerName)
                            break
                else:
                    for playerName in this.client.room.blueTeam:
                        if this.client.room.clients[playerName].mulodromePos[1] == position:
                            this.client.room.blueTeam.remove(playerName)
                            break
                return

            elif CC == Identifiers.recv.Cafe.Mulodrome_Play:
                if not len(this.client.room.redTeam) == 0 or not len(this.client.room.blueTeam) == 0:
                    this.client.room.isMulodrome = True
                    this.client.room.isRacing = True
                    this.client.room.noShaman = True
                    this.client.room.mulodromeRoundCount = 0
                    this.client.room.never20secTimer = True
                    this.client.room.sendAll(Identifiers.send.Mulodrome_End)
                    this.client.room.mapChange()
                return

            elif CC == Identifiers.recv.Cafe.Reload_Cafe:
                if not this.client.isReloadCafe:
                    this.client.cafe.loadCafeMode()
                    this.client.isReloadCafe = True
                    reactor.callLater(3, setattr, this.client, "isReloadCafe", False)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe_Topic:
                topicID = packet.readInt()
                this.client.cafe.openCafeTopic(topicID)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Topic:
                if this.client.privLevel >= 1:
                    message, title = packet.readUTF(), packet.readUTF()
                    this.client.cafe.createNewCafeTopic(message, title)
                return

            elif CC == Identifiers.recv.Cafe.Create_New_Cafe_Post:
                if this.client.privLevel >= 1:
                    topicID, message = packet.readInt(), packet.readUTF()
                    this.client.cafe.createNewCafePost(topicID, message)
                return

            elif CC == Identifiers.recv.Cafe.Open_Cafe:
                this.client.isCafe = packet.readBoolean()
                return

            elif CC == Identifiers.recv.Cafe.Vote_Cafe_Post:
                if this.client.privLevel >= 1:
                    topicID, postID, mode = packet.readInt(), packet.readInt(), packet.readBoolean()
                    this.client.cafe.voteCafePost(topicID, postID, mode)
                return

            elif CC == Identifiers.recv.Cafe.Delete_Cafe_Message:
                if this.client.privLevel >= 7:
                    topicID, postID = packet.readInt(), packet.readInt()
                    try: this.client.cafe.deleteCafePost(topicID, postID)
                    except: pass
                else:
                    this.client.sendMessage("Bunu yapmak için izniniz yok.")
                return

            elif CC == Identifiers.recv.Cafe.Delete_All_Cafe_Message:
                if this.client.privLevel >= 7:
                # if 7 in this.client.privLevel:
                    topicID, playerName = packet.readInt(), packet.readUTF()
                    try: this.client.cafe.deleteAllCafePost(topicID, playerName)
                    except: pass
                else:
                    this.client.sendMessage("Bunu yapmak için izniniz yok.")
                return

        elif C == Identifiers.recv.Inventory.C:
            if CC == Identifiers.recv.Inventory.Open_Inventory:
                this.client.sendInventoryConsumables()
                return

            elif CC == Identifiers.recv.Inventory.Use_Consumable:
                id = packet.readShort()
                if this.client.playerConsumables.has_key(id) and not this.client.isDead and not this.client.room.isRacing and not this.client.room.isBootcamp and not this.client.room.isDefilante and not this.client.room.isSpeedRace and not this.client.room.isMeepRace:
                    # if not id in [31, 34, 2240, 2247, 2262, 2332, 2340] or this.client.pet == 0:
                    count = this.client.playerConsumables[id]
                    if count > 0:
                        count -= 1
                        this.client.playerConsumables[id] -= 1
                        if count == 0:
                            del this.client.playerConsumables[id]
                            if this.client.equipedConsumables:
                                for id in this.client.equipedConsumables:
                                    if not id:
                                        this.client.equipedConsumables.remove(id)
                                None
                                if id in this.client.equipedConsumables:
                                    this.client.equipedConsumables.remove(id)

                        if id in [1, 5, 6, 8, 11, 20, 24, 25, 26, 2250]:
                            if id == 11:
                                this.client.room.objectID += 2
                            ids={1:65, 5:6, 6:34, 8:89, 11:90, 20:33, 24:63, 25:80, 26:95, 2250:97}   
                            this.client.sendPlaceObject(this.client.room.objectID if id == 11 else 0, ids[id], this.client.posX + 28 if this.client.isMovingRight else this.client.posX - 28, this.client.posY, 0, 0 if id == 11 or id == 24 else 10 if this.client.isMovingRight else -10, -3, True, True)
                            
##                        if id == 1 or id == 5 or id == 6 or id == 8 or id == 11 or id == 20 or id == 24 or id == 25 or id == 26 or id == 2250:
##                                if id == 11:
##                                    this.client.room.objectID += 2
##                                this.client.sendPlaceObject(this.client.room.objectID if id == 11 else 0, 65 if id == 1 else 6 if id == 5 else 34 if id == 6 else 89 if id == 8 else 90 if id == 11 else 33 if id == 20 else 63 if id == 24 else 80 if id == 25 else 95 if id == 26 else 114 if id == 2250 else 0, this.client.posX + 28 if this.client.isMovingRight else this.client.posX - 28, this.client.posY, 0, 0 if id == 11 or id == 24 else 10 if this.client.isMovingRight else -10, -3, True, True)
                        if id == 10:
                            x = 0
                            for player in this.client.room.clients.values():
                                if x < 5 and player != this.client:
                                    if player.posX >= this.client.posX - 400 and player.posX <= this.client.posX + 400:
                                        if player.posY >= this.client.posY - 300 and player.posY <= this.client.posY + 300:
                                            player.sendPlayerEmote(3, "", False, False)
                                            x += 1

                        if id == 11:
                            this.client.room.newConsumableTimer(this.client.room.objectID)
                            this.client.isDead = True
                            if not this.client.room.noAutoScore: this.client.playerScore += 1
                            this.client.sendPlayerDied()
                            this.client.room.checkChangeMap()
                    
                        if id == 28:
                            this.client.Skills.sendBonfireSkill(this.client.posX, this.client.posY, 15)

                        if id in [31, 34, 2240, 2247, 2262, 2332, 2340,2437]:
                            this.client.pet = {31:2, 34:3, 2240:4, 2247:5, 2262:6, 2332:7, 2340:8,2437:9}[id]
                            this.client.petEnd = Utils.getTime() + (1200 if this.client.pet == 8 else 3600)
                            this.client.room.sendAll(Identifiers.send.Pet, ByteArray().writeInt(this.client.playerCode).writeUnsignedByte(this.client.pet).toByteArray())

                        if id == 33:
                            this.client.sendPlayerEmote(16, "", False, False)
                        
                        if id == 21:
                            this.client.sendPlayerEmote(12, "", False, False)        

                        if id == 35:
                            if len(this.client.shopBadges) > 0:
                                this.client.room.sendAll(Identifiers.send.Balloon_Badge, ByteArray().writeInt(this.client.playerCode).writeShort(random.choice(this.client.shopBadges.keys())).toByteArray())

                        if id == 800:
                            this.client.shopCheeses += 5
                            this.client.sendAnimZelda(2, 0)
                            this.client.sendGiveCurrency(0, 5)

                        if id == 801:
                            this.client.shopFraises += 5
                            this.client.sendAnimZelda(2, 2)

                        if id == 2234:
                            x = 0
                            this.client.sendPlayerEmote(20, "", False, False)
                            for player in this.client.room.clients.values():
                                if x < 5 and player != this.client:
                                    if player.posX >= this.client.posX - 400 and player.posX <= this.client.posX + 400:
                                        if player.posY >= this.client.posY - 300 and player.posY <= this.client.posY + 300:
                                            player.sendPlayerEmote(6, "", False, False)
                                            x += 1

                        if id == 2239:
                            this.client.room.sendAll(Identifiers.send.Crazzy_Packet, ByteArray().writeByte(4).writeInt(this.client.playerCode).writeInt(this.client.shopCheeses).toByteArray())
                        
                        if id in [2252,2256,2349,2379]:
                            renkler = {2252:"56C93E",2256:"C93E4A",2349:"52BBFB",2379:"FF8400"}
                            renk = int(renkler[id],16)
                            this.client.drawingColor = renk
                            this.client.sendPacket(Identifiers.send.Crazzy_Packet, ByteArray().writeUnsignedByte(1).writeUnsignedShort(650).writeInt(renk).toByteArray())

                        if id in [9,12,13,17,18,19,22,27,407,2251,2258,2308,2439]: # kurkler
                            ids={9:"10",12:"33",13:"35",17:"37",18:"16",19:"42",22:"45",27:"51",407:"7",2251:"61",2258:"66",2308:"75",2439:"118"}[id]
                            look = this.client.playerLook
                            index = look.index(";")
                            this.client.fur = ids + look[index:]
                            
                        if id == 2246:
                            this.client.sendPlayerEmote(24, "", False, False)

                        if id == 2100:
                            idlist = ["1", "5", "6", "8", "11", "20", "24", "25", "26", "31", "34", "2240", "2247", "2262", "2332", "2340", "33", "35", "800", "801", "2234", "2239", "2255", "10", "28"]
                            ids = int(random.choice(idlist))
                            if not ids in this.client.playerConsumables:
                                this.client.playerConsumables[ids] = 1
                            else:
                               counts = this.client.playerConsumables[ids] + 1
                               this.client.playerConsumables[ids] = counts
                            this.client.sendAnimZeldaInventory(4, ids, 1)

                        if id == 2255:
                            this.client.sendAnimZelda2(7, case="$De6", id=random.randint(0, 6))
                            
                        if id == 2259:
                            this.client.room.sendAll(Identifiers.send.Crazzy_Packet, this.client.getCrazzyPacket(5, [this.client.playerCode, (this.client.playerTime / 86400),(this.client.playerTime / 3600) % 24]));
                                
                        this.client.updateInventoryConsumable(id, count)
                        this.client.useInventoryConsumable(id)
                return

            elif CC == Identifiers.recv.Inventory.Equip_Consumable:
                id, equip = packet.readShort(), packet.readBoolean()
                try:
                    if equip:
                        this.client.equipedConsumables.append(id)
                    else:
                        this.client.equipedConsumables.remove(str(id))
                except: pass
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Invite:
                playerName = packet.readUTF()
                this.client.tradeInvite(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Cancel_Trade:
                playerName = packet.readUTF()
                this.client.cancelTrade(playerName)
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Add_Consusmable:
                id, isAdd = packet.readShort(), packet.readBoolean()
                try:
                    this.client.tradeAddConsumable(id, isAdd)
                except: pass
                return
                
            elif CC == Identifiers.recv.Inventory.Trade_Result:
                isAccept = packet.readBoolean()
                this.client.tradeResult(isAccept)
                return

        elif C == Identifiers.recv.Tribulle.C:
            if CC == Identifiers.recv.Tribulle.Tribulle:
                if not this.client.isGuest:
                    code = packet.readShort()
                    this.client.tribulle.parseTribulleCode(code, packet)
                return

        elif C == Identifiers.recv.Sly.C:
            if CC == Identifiers.recv.Sly.Invocation:
                objectCode, posX, posY, rotation, position, invocation = packet.readShort(), packet.readShort(), packet.readShort(), packet.readShort(), packet.readUTF(), packet.readBoolean()
                if this.client.isShaman:
                    showInvocation = True
                    if this.client.room.isSurvivor:
                        showInvocation = invocation
                    pass
                    if showInvocation:
                        this.client.room.sendAllOthers(this.client, Identifiers.send.Invocation, ByteArray().writeInt(this.client.playerCode).writeShort(objectCode).writeShort(posX).writeShort(posY).writeShort(rotation).writeUTF(position).writeBoolean(invocation).toByteArray())
                return

            elif CC == Identifiers.recv.Sly.Remove_Invocation:
                if this.client.isShaman:
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Remove_Invocation, ByteArray().writeInt(this.client.playerCode).toByteArray())
                return

            elif CC == Identifiers.recv.Sly.Change_Shaman_Badge:
                badge = packet.readByte()
                if str(badge) or badge == 0 in this.client.shamanBadges:
                    this.client.equipedShamanBadge = str(badge)
                    this.client.sendProfile(this.client.playerName)
                return
                
            elif CC == Identifiers.recv.Sly.Crazzy_Packet:
                type = packet.readByte()
                if type == 2:
                    posX = int(packet.readShort())
                    posY = int(packet.readShort())
                    lineX = int(packet.readShort())
                    lineY = int(packet.readShort())
                    this.client.room.sendAllOthers(this.client, Identifiers.send.Crazzy_Packet, this.client.getCrazzyPacket(2,[this.client.playerCode, this.client.drawingColor, posX, posY, lineX, lineY]))
                       

            elif CC == Identifiers.recv.Sly.NPC_Functions:
                id = packet.readByte()
                if id == 4:
                    this.client.openNpcShop(packet.readUTF())
                else:
                    this.client.buyNPCItem(packet.readByte())
                return

            
            elif CC == Identifiers.recv.Sly.Full_Look:
                p = ByteArray(packet.toByteArray())
                visuID = p.readShort()

                shopItems = [] if this.client.shopItems == "" else this.client.shopItems.split(",")
                look = this.server.newVisuList[visuID].split(";")
                look[0] = int(look[0])
                lengthCloth = len(this.client.clothes)
                buyCloth = 5 if (lengthCloth == 0) else (50 if lengthCloth == 1 else 100)

                this.client.visuItems = {-1: {"ID": -1, "Buy": buyCloth, "Bonus": True, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}, 22: {"ID": this.client.getFullItemID(22, look[0]), "Buy": this.client.getItemInfo(22, look[0])[6], "Bonus": False, "Customizable": False, "HasCustom": False, "CustomBuy": 0, "Custom": "", "CustomBonus": False}}

                count = 0
                for visual in look[1].split(","):
                    if not visual == "0":
                        item, customID = visual.split("_", 1) if "_" in visual else [visual, ""]
                        item = int(item)
                        itemID = this.client.getFullItemID(count, item)
                        itemInfo = this.client.getItemInfo(count, item)
                        this.client.visuItems[count] = {"ID": itemID, "Buy": itemInfo[6], "Bonus": False, "Customizable": bool(itemInfo[2]), "HasCustom": customID != "", "CustomBuy": itemInfo[7], "Custom": customID, "CustomBonus": False}
                        if this.client.Shop.checkInShop(this.client.visuItems[count]["ID"]):
                            this.client.visuItems[count]["Buy"] -= itemInfo[6]
                        if len(this.client.custom) == 1:
                            if itemID in this.client.custom:
                                this.client.visuItems[count]["HasCustom"] = True
                            else:
                                this.client.visuItems[count]["HasCustom"] = False
                        else:
                            if str(itemID) in this.client.custom:
                                this.client.visuItems[count]["HasCustom"] = True
                            else:
                                this.client.visuItems[count]["HasCustom"] = False
                    count += 1
                hasVisu = map(lambda y: 0 if y in shopItems else 1, map(lambda x: x["ID"], this.client.visuItems.values()))
                visuLength = reduce(lambda x, y: x + y, hasVisu)
                allPriceBefore = 0
                allPriceAfter = 0
                promotion = 70.0 / 100

                p.writeUnsignedShort(visuID)
                p.writeUnsignedByte(20)
                p.writeUTF(this.server.newVisuList[visuID])
                p.writeUnsignedByte(visuLength)

                for category in this.client.visuItems.keys():
                    if len(this.client.visuItems.keys()) == category:
                        category = 22
                    itemID = this.client.getSimpleItemID(category, this.client.visuItems[category]["ID"])

                    buy = [this.client.visuItems[category]["Buy"], int(this.client.visuItems[category]["Buy"] * promotion)]
                    customBuy = [this.client.visuItems[category]["CustomBuy"], int(this.client.visuItems[category]["CustomBuy"] * promotion)]

                    p.writeShort(this.client.visuItems[category]["ID"])
                    p.writeUnsignedByte(2 if this.client.visuItems[category]["Bonus"] else (1 if not this.client.Shop.checkInShop(this.client.visuItems[category]["ID"]) else 0))
                    p.writeUnsignedShort(buy[0])
                    p.writeUnsignedShort(buy[1])
                    p.writeUnsignedByte(3 if not this.client.visuItems[category]["Customizable"] else (2 if this.client.visuItems[category]["CustomBonus"] else (1 if this.client.visuItems[category]["HasCustom"] == False else 0)))
                    p.writeUnsignedShort(customBuy[0])
                    p.writeUnsignedShort(customBuy[1])
                    
                    allPriceBefore += buy[0] + customBuy[0]
                    allPriceAfter += (0 if (this.client.visuItems[category]["Bonus"]) else (0 if this.client.Shop.checkInShop(itemID) else buy[1])) + (0 if (not this.client.visuItems[category]["Customizable"]) else (0 if this.client.visuItems[category]["CustomBonus"] else (0 if this.client.visuItems[category]["HasCustom"] else (customBuy[1]))))
                    
                p.writeShort(allPriceBefore)
                p.writeShort(allPriceAfter)
                this.client.priceDoneVisu = allPriceAfter

                this.client.sendPacket(Identifiers.send.Buy_Full_Look, p.toByteArray())

            elif CC == Identifiers.recv.Sly.Map_Info:
                this.client.room.cheesesList = []
                cheesesCount = packet.readByte()
                i = 0
                while i < cheesesCount / 2:
                    cheeseX, cheeseY = packet.readShort(), packet.readShort()
                    this.client.room.cheesesList.append([cheeseX, cheeseY])
                    i += 1
                
                this.client.room.holesList = []
                holesCount = packet.readByte()
                i = 0
                while i < holesCount / 3:
                    holeType, holeX, holeY = packet.readShort(), packet.readShort(), packet.readShort()
                    this.client.room.holesList.append([holeType, holeX, holeY])
                    i += 1
                return

        if this.server.isDebug:
            print "[%s] Packet not implemented - C: %s - CC: %s - packet: %s" %(this.client.playerName, C, CC, repr(packet.toByteArray()))

    def parsePacketUTF(this, packet):
        values = packet.split(chr(1))
        C = ord(values[0][0])
        CC = ord(values[0][1])
        values = values[1:]

        if C == Identifiers.old.recv.Player.C:
            if CC == Identifiers.old.recv.Player.Conjure_Start:
                this.client.room.sendAll(Identifiers.old.send.Conjure_Start, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjure_End:
                this.client.room.sendAll(Identifiers.old.send.Conjure_End, values)
                return

            elif CC == Identifiers.old.recv.Player.Conjuration:
                reactor.callLater(10, this.client.sendConjurationDestroy, int(values[0]), int(values[1]))
                this.client.room.sendAll(Identifiers.old.send.Add_Conjuration, values)
                return

            elif CC == Identifiers.old.recv.Player.Snow_Ball:
                this.client.sendPlaceObject(0, 34, int(values[0]), int(values[1]), 0, 0, 0, False, True)
                return

            elif CC == Identifiers.old.recv.Player.Bomb_Explode:
                this.client.room.sendAll(Identifiers.old.send.Bomb_Explode, values)
                return

        elif C == Identifiers.old.recv.Room.C:
            if CC == Identifiers.old.recv.Room.Anchors:
                this.client.room.sendAll(Identifiers.old.send.Anchors, values)
                this.client.room.anchors.extend(values)
                return

            elif CC == Identifiers.old.recv.Room.Begin_Spawn:
                if not this.client.isDead:
                    this.client.room.sendAll(Identifiers.old.send.Begin_Spawn, [this.client.playerCode] + values)
                return

            elif CC == Identifiers.old.recv.Room.Spawn_Cancel:
                this.client.room.sendAll(Identifiers.old.send.Spawn_Cancel, [this.client.playerCode])
                return

            elif CC == Identifiers.old.recv.Room.Totem_Anchors:
                if this.client.room.isTotemEditor:
                    if this.client.tempTotem[0] < 20:
                        this.client.tempTotem[0] = int(this.client.tempTotem[0]) + 1
                        this.client.sendTotemItemCount(this.client.tempTotem[0])
                        this.client.tempTotem[1] += "#3#" + chr(1).join(map(str, [values[0], values[1], values[2]]))
                return

            elif CC == Identifiers.old.recv.Room.Move_Cheese:
                this.client.room.sendAll(Identifiers.old.send.Move_Cheese, values)
                return

            elif CC == Identifiers.old.recv.Room.Bombs:
                this.client.room.sendAll(Identifiers.old.send.Bombs, values)
                return

        elif C == Identifiers.old.recv.Balloons.C:
            if CC == Identifiers.old.recv.Balloons.Place_Balloon:
                this.client.room.sendAll(Identifiers.old.send.Balloon, values)
                return

            elif CC == Identifiers.old.recv.Balloons.Remove_Balloon:
                this.client.room.sendAllOthers(this.client, Identifiers.old.send.Balloon, [this.client.playerCode, "0"])
                return

        elif C == Identifiers.old.recv.Map.C:
            if CC == Identifiers.old.recv.Map.Vote_Map:
                if len(values) == 0:
                    this.client.room.receivedNo += 1
                else:
                    this.client.room.receivedYes += 1
                return

            elif CC == Identifiers.old.recv.Map.Load_Map:
                values[0] = values[0].replace("@", "")
                if values[0].isdigit():
                    code = int(values[0])
                    this.client.room.CursorMaps.execute("select * from Maps where Code = ?", [code])
                    rs = this.client.room.CursorMaps.fetchone()
                    if rs:
                        if this.client.playerName == rs["Name"] or this.client.privLevel >= 6:
                            this.client.sendPacket(Identifiers.old.send.Load_Map, [rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]])
                            this.client.room.EMapXML = rs["XML"]
                            this.client.room.EMapLoaded = code
                            this.client.room.EMapValidated = False
                        else:
                            this.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                    else:
                        this.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                else:
                    this.client.sendPacket(Identifiers.old.send.Load_Map_Result, [])
                return

            elif CC == Identifiers.old.recv.Map.Validate_Map:
                mapXML = values[0]
                if this.client.room.isEditor:
                    this.client.sendPacket(Identifiers.old.send.Map_Editor, [""])
                    this.client.room.EMapValidated = False
                    this.client.room.EMapCode = 1
                    this.client.room.EMapXML = mapXML
                    this.client.room.mapChange()
                return

            elif CC == Identifiers.old.recv.Map.Map_Xml:
                this.client.room.EMapXML = values[0]
                return

            elif CC == Identifiers.old.recv.Map.Return_To_Editor:
                this.client.room.EMapCode = 0
                this.client.sendPacket(Identifiers.old.send.Map_Editor, ["", ""])
                return

            elif CC == Identifiers.old.recv.Map.Export_Map:
                isTribeHouse = len(values) != 0
                if this.client.cheeseCount < 40 and this.client.privLevel < 6 and not isTribeHouse:
                    this.client.sendMessage("<ROSE>Haritayı Aktarabilmek İçin 40 Peynire İhtiyacınız Var.", False)
                elif this.client.shopCheeses < (5 if isTribeHouse else 40) and this.client.privLevel < 6:
                    this.client.sendPacket(Identifiers.old.send.Editor_Message, ["", ""])
                elif this.client.room.EMapValidated or isTribeHouse:
                    if this.client.privLevel < 6:
                        this.client.shopCheeses -= 5 if isTribeHouse else 40

                    code = 0
                    if this.client.room.EMapLoaded != 0:
                        code = this.client.room.EMapLoaded
                        this.client.room.CursorMaps.execute("update Maps set XML = ?, Updated = ? where Code = ?", [this.client.room.EMapXML, Utils.getTime(), code])
                    else:
                        this.server.lastMapEditeurCode += 1
                        this.server.configs("game.lastMapCodeId", str(this.server.lastMapEditeurCode))
                        this.server.updateConfig()
                        code = this.server.lastMapEditeurCode
                        
                    this.client.room.CursorMaps.execute("insert into Maps (Code, Name, XML, YesVotes, NoVotes, Perma, Del) values (?, ?, ?, ?, ?, ?, ?)", [code, this.client.playerName, this.client.room.EMapXML, 0, 0, 22 if isTribeHouse else 0, 0])
                    this.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                    this.client.enterRoom(this.server.recommendRoom(this.client.langue))
                    this.client.sendPacket(Identifiers.old.send.Map_Exported, [code])
                return

            elif CC == Identifiers.old.recv.Map.Reset_Map:
                this.client.room.EMapLoaded = 0
                return

            elif CC == Identifiers.old.recv.Map.Exit_Editor:
                this.client.sendPacket(Identifiers.old.send.Map_Editor, ["0"])
                this.client.enterRoom(this.server.recommendRoom(this.client.langue))
                return

            elif C == Identifiers.old.recv.Draw.C:
                if CC == Identifiers.old.recv.Draw.Drawing:
                    if this.client.privLevel >= 10:
                        this.client.room.sendAllOthers(this.client, Identifiers.old.send.Drawing, values)
                    return

            elif CC == Identifiers.old.recv.Draw.Point:
                if this.client.privLevel >= 10:
                    this.client.room.sendAllOthers(this.client, Identifiers.old.send.Drawing_Point, values)
                return

            elif CC == Identifiers.old.recv.Draw.Clear:
                if this.client.privLevel >= 10:
                    this.client.room.sendAll(Identifiers.old.send.Drawing_Clear, values)
                return


        if this.server.isDebug:
            print "[%s][OLD] Packet not implemented - C: %s - CC: %s - values: %s" %(this.client.playerName, C, CC, repr(values))

    def descriptPacket(this, packetID, packet):
        data = ByteArray()
        while packet.bytesAvailable():
            packetID = (packetID + 1) % len(this.server.packetKeys)
            data.writeByte(packet.readByte() ^ this.server.packetKeys[packetID])
        return data
