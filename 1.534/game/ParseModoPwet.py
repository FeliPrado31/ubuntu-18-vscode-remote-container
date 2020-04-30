from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
import math

class ModoPwet:

    def __init__(this, player, server):
        this.client = player
        this.server = player.server

    def checkReport(this, array, playerName):
        return playerName in array

    def makeReport(this, playerName, type, comments):
        playerName = Utils.parsePlayerName(playerName)
        repatan = this.client.playerName
        this.client.sendServerMessageAdmin('[REPORTE] <V>%s</V> <N>ha reportado a</N> <V>%s</V>' % (repatan,playerName))          
        #this.server.sendStaffMessage(8, '[REPORT] [<V>%s</V>] by <V>[%s]</V> reported and reason: <J>%s</J> -> <V>%s</V>' % (repatan,playerName,{0: 'Hack',1: 'Spam / Flood',2: 'Insultos',3: 'Phishing',4: 'Others'}[type],'-' if comments == '' else comments))

        if this.server.players.get(playerName):
            if this.server.reports.has_key(playerName):
                if this.server.reports[playerName]['reporters'].has_key(repatan):
                    r = this.server.reports[playerName]['reporters'][repatan]
                    if r[0] != type:
                        this.server.reports[playerName]['reporters'][repatan]=[type,comments,Utils.getTime()]
                        
                else:
                    this.server.reports[playerName]['reporters'][repatan]=[type,comments,Utils.getTime()]
                this.server.reports[playerName]['durum'] = 'online' if this.server.checkConnectedAccount(playerName) else 'disconnected'
            else:
                this.server.reports[playerName] = {}
                this.server.reports[playerName]['reporters'] = {repatan:[type,comments,Utils.getTime()]}
                this.server.reports[playerName]['durum'] = 'online' if this.server.checkConnectedAccount(playerName) else 'disconnected'
                this.server.reports[playerName]['dil'] = this.getModopwetLangue(playerName)
                this.server.reports[playerName]['isMuted'] = False
            this.updateModoPwet()
            this.client.sendBanConsideration()

    def getModopwetLangue(this, playerName):
        player = this.server.players.get(playerName)
        if player != None:
            return player.langue
        else:
            return 'EN'

    def updateModoPwet(this):
        for player in this.server.players.values():
            if player.isModoPwet and player.privLevel >= 5:
                player.modoPwet.openModoPwet(True)

    def getPlayerRoomName(this, playerName):
        player = this.server.players.get(playerName)
        if player != None:
            return player.roomName
        else:
            return '0'
            
    def getRoomMods(this,room):
        s = []
        i = ""
        for player in this.server.players.values():
            if player.roomName == room and player.privLevel >= 5:
                s.append(player.playerName)
                
        if len(s) == 1:
            return s[0]
        else:
            for isim in s:
                i = i+isim+", "
        return i
        
    def getPlayerKarma(this, playerName):
        player = this.server.players.get(playerName)
        if player:
            return player.playerKarma
        else:
            return 0
    
    def banHack(this, playerName,iban):
        if this.server.banPlayer(playerName, 360, "Hack (last warning before account deletion)", this.client.playerName, iban):
            this.server.sendStaffMessage(5, "<V>%s<BL> baniu <V>%s<BL> por <V>360 <BL>horas. Motivo: <V>Hack (last warning before account deletion)<BL>." %(this.client.playerName, playerName))
        this.updateModoPwet()
        
    def deleteReport(this,playerName,handled):
        if handled == 0:
            this.server.reports[playerName]["durum"] = "deleted"
            this.server.reports[playerName]["deletedby"] = this.client.playerName
        else:
            if this.server.reports.has_key(playerName):
                del this.server.reports[playerName]
                
        this.updateModoPwet()
        
    def sirala(this,verilen):
        for i in verilen[1]["reporters"]:
            return verilen[1]["reporters"][i][2]
            
    def sortReports(this,reports,sort):  
        if sort:
            return sorted(reports.items(), key=this.sirala,reverse=True)
        else:
            return sorted(reports.items(), key=lambda (x): len(x[1]["reporters"]),reverse=True)
    
    def openModoPwet(this,isOpen=False,modopwetOnlyPlayerReports=False,sortBy=False):
        if isOpen:
            if len(this.server.reports) <= 0:
                this.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
            else:
                this.client.sendPacket(Identifiers.send.Modopwet_Open, 0)
                reports,bannedList,deletedList,disconnectList = this.sortReports(this.server.reports,sortBy),{},{},[]
                sayi = 0
                p = ByteArray()  
                for i in reports:
                    isim = i[0]
                    v = this.server.reports[isim]
                    if this.client.modoPwetLangue == 'ALL' or v["dil"] == this.client.modoPwetLangue:
                        oyuncu = this.server.players.get(isim)
                        saat = math.floor(oyuncu.playerTime/3600) if oyuncu else 0
                        odaisim = oyuncu.roomName if oyuncu else "0"
                        sayi += 1
                        this.client.lastReportID += 1
                        if sayi >= 255:
                            break  
                        p.writeByte(sayi)
                        p.writeShort(this.client.lastReportID)
                        p.writeUTF(v["dil"])
                        p.writeUTF(isim)
                        p.writeUTF(odaisim)
                        p.writeByte(1) # alttaki modname uzunlugu ile alakali
                        p.writeUTF(this.getRoomMods(odaisim))
                        p.writeInt(saat) #idk
                        p.writeByte(int(len(v["reporters"])))
                        for name in v["reporters"]:
                            r = v["reporters"][name]
                            p.writeUTF(name)
                            p.writeShort(this.getPlayerKarma(name)) #karma
                            p.writeUTF(r[1])
                            p.writeByte(r[0])
                            p.writeShort(int(Utils.getSecondsDiff(r[2])/60)) #05m felan rep suresi
                                
                        mute = v["isMuted"]
                        p.writeBoolean(mute) #isMute
                        if mute:
                            p.writeUTF(v["mutedBy"])
                            p.writeShort(v["muteHours"])
                            p.writeUTF(v["muteReason"])
                            
                        if v['durum'] == 'banned':
                            x = {}
                            x['banhours'] = v['banhours']
                            x['banreason'] = v['banreason']
                            x['bannedby'] = v['bannedby']
                            bannedList[isim] = x
                        if v['durum'] == 'deleted':
                            x = {}
                            x['deletedby'] = v['deletedby']
                            deletedList[isim] = x
                        if v['durum'] == 'disconnected':
                            disconnectList.append(isim)

                this.client.sendPacket(Identifiers.send.Modopwet_Open, ByteArray().writeByte(int(len(reports))).writeBytes(p.toByteArray()).toByteArray())
                for user in disconnectList:
                    this.changeReportStatusDisconnect(user)

                for user in deletedList.keys():
                    this.changeReportStatusDeleted(user, deletedList[user]['deletedby'])

                for user in bannedList.keys():
                    this.changeReportStatusBanned(user, bannedList[user]['banhours'], bannedList[user]['banreason'], bannedList[user]['bannedby'])

    def changeReportStatusDisconnect(this, playerName):
        this.client.sendPacket(Identifiers.send.Modopwet_Disconnected, ByteArray().writeUTF(playerName).toByteArray())

    def changeReportStatusDeleted(this, playerName, deletedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Deleted, ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray())

    def changeReportStatusBanned(this, playerName, banhours, banreason, bannedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Banned, ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray())

    def openChatLog(this, playerName):
        if this.server.chatMessages.has_key(playerName):
            packet = ByteArray().writeUTF(playerName).writeByte(len(this.server.chatMessages[playerName]))
            for message in this.server.chatMessages[playerName]:
                packet.writeUTF(message[1]).writeUTF(message[0])
            this.client.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
