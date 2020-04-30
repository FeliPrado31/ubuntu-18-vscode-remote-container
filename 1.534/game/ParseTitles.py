#coding: utf-8
import re, base64, hashlib, urllib2, random, struct

from ByteArray import ByteArray
from Identifiers import Identifiers

class parseTitles:
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

    def parseCommandCode(this, command):                
        values = command.split(" ")
        _command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        this.currentArgsCount = argsCount
        try:
            
            if command in ["yolo"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 463.1 if id == 1 else 463.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["dodger"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 464.1 if id == 1 else 464.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["survive"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 465.1 if id == 1 else 465.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["thelastmouse"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 466.1 if id == 1 else 466.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["mousegrylls"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 467.1 if id == 1 else 467.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["nottoday"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 468.1 if id == 1 else 468.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["survivalist"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 469.1 if id == 1 else 469.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["cannonsurfer"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 470.1 if id == 1 else 470.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["supermeatmouse"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 471.1 if id == 1 else 471.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["themousewholived"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 472.1 if id == 1 else 472.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            
            elif command in ["meeptitle"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 473.1 if id == 1 else 473.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["sugardadmy"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 474.1 if id == 1 else 474.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["themerciless"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 475.1 if id == 1 else 475.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["strike"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 475.1 if id == 1 else 475.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["wreckingball"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 477.1 if id == 1 else 477.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["pierogi"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 478.1 if id == 1 else 478.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["snowboarder"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 479.1 if id == 1 else 479.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["nicemice2019"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 480.1 if id == 1 else 480.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["mododiablo"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 481.1 if id == 1 else 481.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["starlight"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 482.1 if id == 1 else 482.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["trucho"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 483.1 if id == 1 else 483.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
                        
            elif command in ["kratos"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 488.1 if id == 1 else 488.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["bichote"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 489.1 if id == 1 else 489.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["black"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 490.1 if id == 1 else 490.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            elif command in ["rip"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 491.1 if id == 1 else 491.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["pain"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 492.1 if id == 1 else 492.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["rekq"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 493.1 if id == 1 else 493.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["thetrue1"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 494.1 if id == 1 else 494.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["myhappyended"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 495.1 if id == 1 else 495.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["anightmareonstreet"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 496.1 if id == 1 else 496.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["weachina1"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 497.1 if id == 1 else 497.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["fishforthecat"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 498.1 if id == 1 else 498.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["malandr"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 499.1 if id == 1 else 499.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["kqofdead"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 500.1 if id == 1 else 500.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["jelidance"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 501.1 if id == 1 else 501.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["fuckyou"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 502.1 if id == 1 else 502.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["vanidos"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 503.1 if id == 1 else 503.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["reyna"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 504.1 if id == 1 else 504.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["pikachu"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 12:
                        titleID = 505.1 if id == 1 else 505.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 12
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 12 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["skere"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 506.1 if id == 1 else 506.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["ohohoh"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 1062.1 if id == 1 else 1062.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["assasin"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 1034.1 if id == 1 else 1034.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["cowabunga"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 1033.1 if id == 1 else 1033.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["Game of Thrones"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 0:
                        titleID = 1024.1 if id == 1 else 1024.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 0
                        this.client.sendMessage("\n<font color='#FFFFFF'>Gracias por llevarte este título, recuerda a CentralCACA cada vez que vayas al baño y guarda comida para Ale.")
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 1 moneda. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["pmnoel"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 1063.1 if id == 1 else 1063.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
            
            elif command in ["snowballs"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 1064.1 if id == 1 else 1064.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")
                
            elif command in ["dulcenavidad"]:
                if this.client.privLevel >= 1:
                    if this.client.nowCoins >= 10:
                        titleID = 1065.1 if id == 1 else 1065.1
                        this.client.specialTitleList.append(titleID);
                        this.client.sendUnlockedTitle(str(int(titleID)), "")
                        this.client.sendCompleteTitleList()
                        this.client.sendTitleList()
                        this.client.nowCoins -= 10
                    else:
                        this.client.sendMessage("\n<font color='#FFFFFF'>Lo siento, este título cuesta 10 monedas. </font>\n\n<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")

        except Exception as ERROR:
            pass