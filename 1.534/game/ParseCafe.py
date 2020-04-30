#coding: utf-8
# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers
class Cafe:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        # this.CursorCafe = player.server.CursorCafe
    
    def loadCafeMode(this):
        can = not this.client.isGuest
        
        if not can:
            this.client.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")
            
        this.client.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(can).toByteArray())

        packet = ByteArray()
        konular = this.server.cafeTopics
        if len(konular) > 0:
            # for i,v in this.server.cafeTopics.items():
            for i,v in sorted(konular.items(), key=lambda x: x[1]["Tarih"],reverse=True):
                if v["Dil"] == this.client.langue:
                    konuid,baslik,sahip,yorumlar,sonyazan,tarih = v["KonuID"],v["Baslik"],v["Sahip"],v["Yorumlar"],v["SonYazan"],v["Tarih"]
                    packet.writeInt(konuid).writeUTF(baslik).writeInt(this.server.getPlayerID(sahip)).writeInt(yorumlar).writeUTF(sonyazan).writeInt(Utils.getSecondsDiff(tarih))
        
        this.client.sendPacket(Identifiers.send.Cafe_Topics_List, packet.toByteArray())
            

    def openCafeTopic(this, topicID):
        if this.server.cafeTopics.has_key(topicID):
            packet = ByteArray().writeBoolean(True).writeInt(topicID)
            for id,v in this.server.cafePosts[topicID].items():
                yorumid,yorumyazan,yorumtarih,mesaj,puan,verenler = v["YorumID"],v["YorumYazan"],v["YorumTarih"],v["YorumMesaj"],v["Puan"],v["OyVerenler"]
                packet.writeInt(yorumid).writeInt(this.server.getPlayerID(yorumyazan)).writeInt(Utils.getSecondsDiff(yorumtarih)).writeUTF(yorumyazan).writeUTF(mesaj).writeBoolean(str(this.client.playerID) not in verenler).writeShort(puan)
            this.client.sendPacket(Identifiers.send.Open_Cafe_Topic, packet.toByteArray())
        
    def createNewCafeTopic(this, title, message):
        id = len(this.server.cafeTopics)+1
        this.server.cafeTopics[id] = {}
        this.server.cafeTopics[id]["KonuID"] = id
        this.server.cafeTopics[id]["Baslik"] = "CENSORED" if this.server.checkMessage(title) else title
        this.server.cafeTopics[id]["Sahip"] = this.client.playerName
        this.server.cafeTopics[id]["Yorumlar"] = 0
        this.server.cafeTopics[id]["SonYazan"] = this.client.playerName
        this.server.cafeTopics[id]["Tarih"] = Utils.getTime()
        this.server.cafeTopics[id]["Dil"] = this.client.langue
        this.createNewCafePost(id, "CENSORED" if this.server.checkMessage(this.client, message) else message)
        this.loadCafeMode()

    def createNewCafePost(this, topicID, message):
        commentsCount = 0
        if not this.server.cafeTopics.has_key(topicID): return
        
        if not this.server.cafePosts.has_key(topicID):
            this.server.cafePosts[topicID] = {}
            
        id = len(this.server.cafePosts[topicID])+1 #yorum id
        this.server.cafePosts[topicID][id] = {}
        this.server.cafePosts[topicID][id]["KonuID"] = topicID
        this.server.cafePosts[topicID][id]["YorumID"] = id
        this.server.cafePosts[topicID][id]["YorumYazan"] = this.client.playerName
        this.server.cafePosts[topicID][id]["YorumMesaj"] = "CENSORED" if this.server.checkMessage(this.client, message) else message
        this.server.cafePosts[topicID][id]["YorumTarih"] = Utils.getTime()
        this.server.cafePosts[topicID][id]["Puan"] = 0
        this.server.cafePosts[topicID][id]["OyVerenler"] = []
            
        this.server.cafeTopics[topicID]["Yorumlar"] += 1
        this.server.cafeTopics[topicID]["SonYazan"] = this.client.playerName
        this.server.cafeTopics[topicID]["Tarih"] = Utils.getTime()

        commentsCount = this.server.cafeTopics[topicID]["Yorumlar"]
        this.openCafeTopic(topicID)
        for player in this.server.players.values():
            if player.isCafe:
                player.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(this.client.playerName).writeInt(commentsCount).toByteArray())
       
    def voteCafePost(this, topicID, postID, mode):
        try:
            if not this.client.playerID in this.server.cafePosts[topicID][postID]["OyVerenler"]:
                puan = this.server.cafePosts[topicID][postID]["Puan"]
                playerid = str(this.client.playerID)

                this.server.cafePosts[topicID][postID]["OyVerenler"].append(playerid) 
                if mode:
                    this.server.cafePosts[topicID][postID]["Puan"] += 1
                else:
                    this.server.cafePosts[topicID][postID]["Puan"] -= 1

                this.openCafeTopic(topicID)
        except: pass

    def deleteCafePost(this, topicID, postID):   
        del this.server.cafePosts[topicID][postID]
        
        this.server.cafeTopics[topicID]["Yorumlar"] -= 1
        
        if len(this.server.cafePosts[topicID]) < 1:
            del this.server.cafeTopics[topicID]
            
        for player in this.server.players.values():
            if player.isCafe:
                player.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray().writeInt(topicID).writeInt(postID).toByteArray())
        
        this.openCafeTopic(topicID)

    def deleteAllCafePost(this, topicID, playerName):
        if this.server.cafeTopics[topicID]["Sahip"] == playerName:
            del this.server.cafePosts[topicID]
            del this.server.cafeTopics[topicID]
        else:
            for id,v in this.server.cafePosts[topicID].items():
                if v["YorumYazan"] == playerName:
                    del this.server.cafePosts[topicID][id]
                    
        this.loadCafeMode()
        this.openCafeTopic(topicID)
