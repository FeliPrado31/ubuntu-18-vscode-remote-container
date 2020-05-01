#coding: utf-8
import struct, random, time as _time
from twisted.internet import reactor
from utils import Utils

class fullMenu:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        currentPage = 1
        
    def sendMenu(this):
        bg = ""
        text = "<a href='event:fullMenu:open'><font size='15'><N>MENU</N></font></a>"
        this.client.sendAddPopupText(11000, 745, 24, 50, 20, '183236', '183236', 100, str(bg))
        this.client.sendAddPopupText(11001, 745, 24, 50, 20, '000000', '000000', 100, str(text))
    
    def open(this):
        if _time.time() - this.client.CMDTime > 0.5:
            this.client.CMDTime = _time.time()
            this.client.close()
            this.client.room.addTextArea(10002, "<img src='https://i.hizliresim.com/V3NqYP.png'>", this.client.playerName, 10, 25, 765, 380, 0, 0, 0, False)
            this.client.room.addTextArea(10003, this.client.getText("fullMenu.title", this.client.playerName), this.client.playerName, 170, 40, 495, 380, 0, 0, 0, False)
            this.client.room.addTextArea(10004, this.client.getText("fullMenu.main", this.client.playerName), this.client.playerName, 145, 105, 415, 270, 0, 0, 100, False)
            this.client.room.addTextArea(10066, "<font size='13'><N>Şu anda <ROSE>"+str(this.client.getConnectedPlayerCount())+"<N> kullanıcı çevrimiçi!</font>", this.client.playerName, 145, 270, 495, 380, 0, 0, 100, False)
            this.client.room.addTextArea(10067, "<img src='https://i.hizliresim.com/lbpnEg.png'></img>", this.client.playerName, 140, 286, 495, 380, 0, 0, 100, False)
            this.client.room.addTextArea(10070, "<font color='#FFD991' size='13'>TR: <CH>" + str(this.client.getConnectedPlayerCount()) + '</font>', this.client.playerName, 175, 292, 239, 380, 0, 0, 100, False)
            this.client.room.addTextArea(10075, "<img src='https://i.hizliresim.com/NONMGk.jpg'>", this.client.playerName, 560, 82, 495, 0, 0, 0, 100, False)
            this.client.room.addTextArea(10074, "<font face='Arial' size='20'><N><a href='event:profileMenu'>" + this.client.playerName + '</a></N></font>', this.client.playerName, 625, 100, 150, 25, 0, 0, 0, False)
            this.client.room.addTextArea(10076, "<img src='http://www.transforvida.com.br/newmenu/user-avatar.png' width='46' height='52'></img>", this.client.playerName, 560, 80, 60, 65, 0, 0, 100, False)
            this.client.room.addTextArea(10073, this.client.getText('shop.items.vip.1' if this.client.privLevel == 1 else 'shop.items.fichas.1' if this.client.privLevel == 7 else 'shop.items.fichas.2' if this.client.privLevel == 8 else 'shop.items.fichas.3' if this.client.privLevel == 9 else 'shop.items.fichas.4' if this.client.privLevel == 10 else 'shop.items.fichas.5', this.client.nowCoins, len(this.client.shopBadges), this.client.firstCount, this.client.cheeseCount, this.client.shamanSaves, this.client.hardModeSaves, this.client.divineModeSaves), this.client.playerName, 590, 220, 170, 155, 0, 0, 0, False)
            this.client.room.addTextArea(10091, "<img src='https://i.hizliresim.com/JONo2j.jpg' width='91' height='22'>", this.client.playerName, 23, 59, 100, 50, 0, 0, 0, False)
            this.client.getFull()

class roleta:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        currentPage = 1
    
    def open(this):
        if _time.time() - this.client.CMDTime > 0.5:
            this.client.CMDTime = _time.time()
            this.client.close()
            this.client.room.addTextArea(10002, "<img src='https://i.hizliresim.com/V3NqYP.png'>", this.client.playerName, 10, 25, 765, 380, 0, 0, 0, False)
            this.client.room.addTextArea(10003, this.client.getText("roleta.title", this.client.playerName), this.client.playerName, 170, 40, 495, 380, 0, 0, 0, False)
            this.client.room.addTextArea(10004, this.client.getText("roleta.main", this.client.playerName), this.client.playerName, 145, 105, 415, 270, 0, 0, 100, False)
            this.client.room.addTextArea(10091, "<img src='https://i.hizliresim.com/JONo2j.jpg' width='91' height='22'>", this.client.playerName, 23, 189, 100, 50, 0, 0, 0, False)
            this.client.getFull()

class equipe:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        currentPage = 1
    
    def open(this):
        this.client.close()
        this.client.room.addTextArea(10002, "<img src='https://i.hizliresim.com/V3NqYP.png'>", this.client.playerName, 10, 25, 765, 380, 0, 0, 0, False)
        this.client.room.addTextArea(10003, this.client.getText("equipe.title", this.client.playerName), this.client.playerName, 170, 40, 495, 380, 0, 0, 0, False)
        this.client.room.addTextArea(10004, this.client.getText("equipe.main", this.client.playerName), this.client.playerName, 150, 100, 220, 265, 1250067, 1118481, 40, False)
        this.client.room.addTextArea(10091, "<img src='https://i.hizliresim.com/JONo2j.jpg' width='91' height='22'>", this.client.playerName, 23, 159, 100, 50, 0, 0, 0, False)
        this.client.getFull()
        
    def sendStaff(this, type):
        if _time.time() - this.client.CMDTime > 0.5:
            this.client.CMDTime = _time.time()
            lists = ["<p align='left'>", "<p align='left'>", "<p align='left'>", "<p align='left'>", "<p align='left'>", "<p align='left'>", "<p align='left'>"]
            if type == 1:
                this.Cursor.execute("select Users, PrivLevel from Username where PrivLevel = 11 Order by PlayerID")
            if type == 2:
                this.client.Cursor.execute("select Users, PrivLevel from Username where PrivLevel = 10 Order by PlayerID LIMIT 7")
            if type == 3:
                this.client.Cursor.execute("select Users, PrivLevel from Username where PrivLevel = 9 Order by PlayerID LIMIT 7")
            if type == 4:
                this.client.Cursor.execute("select Users, PrivLevel from Username where PrivLevel = 8 Order by PlayerID LIMIT 7")
            if type == 5:
                this.client.Cursor.execute("select Users, PrivLevel from Username where PrivLevel = 7 Order by PlayerID LIMIT 7")
            if type == 6:
                this.client.Cursor.execute("select Users, PrivLevel from Username where PrivLevel = 6 Order by PlayerID LIMIT 7")
            r = this.Cursor.fetchall()
            for rs in r:
                playerName = rs["Username"]
                privLevel = int(rs["PrivLevel"])
                lists[{11:0, 10:1, 9:2, 8:3, 7:4, 6:5, 5:6}[privLevel]] += "\n" + " <V> " +playerName+ "<N> - <V>" + {11:"<font color='#FE8446'>Kurucu</font>", 10: "<ROSE>Admin", 9:"<VI>Koordinatör", 8:"<J>Süper Moderatör", 7:"<CE>Moderatör", 6:"<CEP>MapCrew"}[privLevel] + "<V><N> - " + ("<N>[<VP>Çevrimiçi<N>] \n <N> " if this.server.checkConnectedAccount(playerName) else "<N>[<R>Çevrimdışı<N>] \n")
            if type == 1:
                this.open()
                this.client.room.addTextArea(10014, "<p align = \"left\"><font size = \"13\">  Kurucular\n" + "".join(lists) + "</p>""<br><br></p>", this.client.playerName, 400, 96, 470, 215, 0, 0, 0, False)
            if type == 2:
                this.client.room.addTextArea(10014, "<p align = \"left\"><font size = \"13\">  Adminler\n" + "".join(lists) + "</p>""<br><br></p>", this.client.playerName, 400, 96, 470, 215, 0, 0, 0, False)
            if type == 3:
                this.client.room.addTextArea(10014, "<p align = \"left\"><font size = \"13\">  Koordinatörler\n" + "".join(lists) + "</p>""<br><br></p>", this.client.playerName, 400, 96, 470, 215, 0, 0, 0, False)
            if type == 4:
                this.client.room.addTextArea(10014, "<p align = \"left\"><font size = \"13\">  Süper Moderatörler\n" + "".join(lists) + "</p>""<br><br></p>", this.client.playerName, 400, 96, 470, 215, 0, 0, 0, False)
            if type == 5:
                this.client.room.addTextArea(10014, "<p align = \"left\"><font size = \"13\">  Moderatörler\n" + "".join(lists) + "</p>""<br><br></p>", this.client.playerName, 400, 96, 470, 215, 0, 0, 0, False)
            if type == 6:
                this.client.room.addTextArea(10014, "<p align = \"left\"><font size = \"13\">  MapCrewler\n" + "".join(lists) + "</p>""<br><br></p>", this.client.playerName, 400, 96, 470, 215, 0, 0, 0, False)

class ranking:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        currentPage = 1
    
    def open(this):
        this.client.close()
        this.client.room.addTextArea(10002, "<img src='https://i.hizliresim.com/V3NqYP.png'>", this.client.playerName, 10, 25, 765, 380, 0, 0, 0, False)
        this.client.room.addTextArea(10003, this.client.getText("ranking.title", this.client.playerName), this.client.playerName, 170, 40, 495, 380, 0, 0, 0, False)
        this.client.room.addTextArea(10004, this.client.getText("ranking.main", this.client.playerName), this.client.playerName, 150, 100, 300, 260, 1250067, 1118481, 40, False)
        this.client.room.addTextArea(10091, "<img src='https://i.hizliresim.com/JONo2j.jpg' width='91' height='22'>", this.client.playerName, 23, 129, 100, 50, 0, 0, 0, False)
        this.client.getFull()

    def sendRanking(this, type):
        if _time.time() - this.client.CMDTime > 1:
            this.client.CMDTime = _time.time()
            if type == 1:
                this.open()
                names = "<font size='12'><ROSE>Kullanıcı</ROSE></font>\n"
                counts = "<font size='12'><ROSE>First</ROSE></font>\n"
                for user in this.server.rankingsList[0].items():
                    names += ("<font size='13'><J>%02d<V> - <N>%s</N>\n" if user[0] == 1 else ('<CH>%02d<V> - <N>%s</N>\n' if user[0] == 2 else ('<R>%02d<V> - <N>%s</N>\n' if user[0] == 3 else '<V>%02d - <N>%s</N>\n'))) % (user[0], user[1][0].lower().capitalize())
                    counts += "<font size='13'><J>%s\n" % user[1][1]
                    this.client.room.addTextArea(10022, names, this.client.playerName, 500, 105, 306, 270, 0, 0, 0, False)
                    this.client.room.addTextArea(10033, counts, this.client.playerName, 650, 105, 0, 0, 0, 0, 0, False)

            if type == 2:
                names = "<font size='12'><ROSE>Kullanıcı</ROSE></font>\n"
                counts = "<font size='12'><ROSE>Peynir</ROSE></font>\n"
                for user in this.server.rankingsList[1].items():
                    names += ("<font size='13'><J>%02d<V> - <N>%s</N>\n" if user[0] == 1 else ('<CH>%02d<V> - <N>%s</N>\n' if user[0] == 2 else ('<R>%02d<V> - <N>%s</N>\n' if user[0] == 3 else '<V>%02d - <N>%s</N>\n'))) % (user[0], user[1][0].lower().capitalize())
                    counts += "<font size='13'><J>%s\n" % user[1][1]
                    this.client.room.addTextArea(10022, names, this.client.playerName, 500, 105, 306, 270, 0, 0, 0, False)
                    this.client.room.addTextArea(10033, counts, this.client.playerName, 650, 105, 0, 0, 0, 0, 0, False)

            if type == 3:
                names = "<font size='12'><ROSE>Kullanıcı</ROSE></font>\n"
                counts = "<font size='12'><ROSE>Save</ROSE></font>\n"
                for user in this.server.rankingsList[2].items():
                    names += ("<font size='13'><J>%02d<V> - <N>%s</N>\n" if user[0] == 1 else ('<CH>%02d<V> - <N>%s</N>\n' if user[0] == 2 else ('<R>%02d<V> - <N>%s</N>\n' if user[0] == 3 else '<V>%02d - <N>%s</N>\n'))) % (user[0], user[1][0].lower().capitalize())
                    counts += "<font size='13'><J>%s\n" % user[1][1]
                    this.client.room.addTextArea(10022, names, this.client.playerName, 500, 105, 306, 270, 0, 0, 0, False)
                    this.client.room.addTextArea(10033, counts, this.client.playerName, 650, 105, 0, 0, 0, 0, 0, False)

            if type == 4:
                names = "<font size='12'><ROSE>Kullanıcı</ROSE></font>\n"
                counts = "<font size='12'><ROSE>Bootcamp</ROSE></font>\n"
                for user in this.server.rankingsList[3].items():
                    names += ("<font size='13'><J>%02d<V> - <N>%s</N>\n" if user[0] == 1 else ('<CH>%02d<V> - <N>%s</N>\n' if user[0] == 2 else ('<R>%02d<V> - <N>%s</N>\n' if user[0] == 3 else '<V>%02d - <N>%s</N>\n'))) % (user[0], user[1][0].lower().capitalize())
                    counts += "<font size='13'><J>%s\n" % user[1][1]
                    this.client.room.addTextArea(10022, names, this.client.playerName, 500, 105, 306, 270, 0, 0, 0, False)
                    this.client.room.addTextArea(10033, counts, this.client.playerName, 650, 105, 0, 0, 0, 0, 0, False)

            if type == 5:
                names = "<font size='12'><ROSE>Kullanıcı</ROSE></font>\n"
                counts = "<font size='12'><ROSE>Coins</ROSE></font>\n"
                for user in this.server.rankingsList[4].items():
                    names += ("<font size='13'><J>%02d<V> - <N>%s</N>\n" if user[0] == 1 else ('<CH>%02d<V> - <N>%s</N>\n' if user[0] == 2 else ('<R>%02d<V> - <N>%s</N>\n' if user[0] == 3 else '<V>%02d - <N>%s</N>\n'))) % (user[0], user[1][0].lower().capitalize())
                    counts += "<font size='13'><J>%s\n" % user[1][1]
                    this.client.room.addTextArea(10022, names, this.client.playerName, 500, 105, 306, 270, 0, 0, 0, False)
                    this.client.room.addTextArea(10033, counts, this.client.playerName, 650, 105, 0, 0, 0, 0, 0, False)

            if type == 6:
                names = "<font size='12'><ROSE>Kullanıcı</ROSE></font>\n"
                counts = "<font size='12'><ROSE>Puan</ROSE></font>\n"
                for user in this.server.rankingsList[5].items():
                    names += ("<font size='13'><J>%02d<V> - <N>%s</N>\n" if user[0] == 1 else ('<CH>%02d<V> - <N>%s</N>\n' if user[0] == 2 else ('<R>%02d<V> - <N>%s</N>\n' if user[0] == 3 else '<V>%02d - <N>%s</N>\n'))) % (user[0], user[1][0].lower().capitalize())
                    counts += "<font size='13'><J>%s\n" % user[1][1]
                    this.client.room.addTextArea(10022, names, this.client.playerName, 500, 105, 306, 270, 0, 0, 0, False)
                    this.client.room.addTextArea(10033, counts, this.client.playerName, 650, 105, 0, 0, 0, 0, 0, False)

            if type == 7:
                names = "<font size='12'><ROSE>Kabile</ROSE></font>\n"
                counts = "<font size='12'><ROSE>Puan</ROSE></font>\n"
                for user in this.server.rankingsList[6].items():
                    names += ("<font size='13'><J>%02d<V> - <N>%s</N>\n" if user[0] == 1 else "<CH>%02d<V> - <N>%s</N>\n" if user[0] == 2 else "<R>%02d<V> - <N>%s</N>\n" if user[0] == 3 else "<V>%02d - <N>%s</N>\n") %(user[0], user[1][0].lower().capitalize())
                    counts += "<font size='13'><J>%s\n" %(user[1][1])
                    this.client.sendPacket([29, 22], struct.pack("!l", 10004))
                    this.client.room.addTextArea(10022, names, this.client.playerName, 195, 95, 0, 0, 0, 0, 0, False)
                    this.client.room.addTextArea(10033, counts, this.client.playerName, 605, 95, 0, 0, 0, 0, 0, False)
                            
class shop:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        currentPage = 1
                
    def open(this):
        if _time.time() - this.client.CMDTime > 0.5:
            this.client.CMDTime = _time.time()
            this.client.close()
            this.client.room.addTextArea(10002, "<img src='https://i.hizliresim.com/V3NqYP.png'>", this.client.playerName, 10, 25, 765, 380, 0, 0, 0, False)
            this.client.room.addTextArea(10003, this.client.getText("shop.title", this.client.playerName), this.client.playerName, 170, 40, 495, 380, 0, 0, 0, False)
            this.client.room.addTextArea(10004, this.client.getText("shop.main", this.client.playerName, this.client.nowCoins), this.client.playerName, 200, 95, 495, 380, 0, 0, 0, False)
            this.client.room.addTextArea(10091, "<img src='https://i.hizliresim.com/JONo2j.jpg' width='91' height='22'>", this.client.playerName, 23, 99, 100, 50, 0, 0, 0, False)
            this.client.getFull()
        
    def changeTab(this, tab, page):
        if _time.time() - this.client.CMDTime > 0.5:
            this.client.CMDTime = _time.time()
            this.client.room.removeTextArea(10004, this.client.playerName)
            this.client.room.addTextArea(10014, this.client.getText("shop.main", this.client.playerName, this.client.nowCoins), this.client.playerName, 200, 95, 495, 380, 0, 0, 0, False)
            text = this.client.getText("shop.main" if tab == 1 else "shop.header", this.client.playerName, this.client.nowCoins)
            if tab == 2 or tab == 3 or tab == 4 or tab == 5 or tab == 6 or tab == 7 or tab == 8 or tab == 9:
                items = this.server.menu["texts"][this.client.langue if this.client.langue in this.server.menu["texts"] else "EN"]["shop"]["items"]["firsts" if tab == 2 else "bootcamps" if tab == 3 else "savesnormal" if tab == 4 else "savesdificil" if tab == 5 else "savesdivino" if tab == 6 else "vip" if tab == 7 else "fichas" if tab == 8 else "coletados"]
                coins = this.client.getText("shop.coins")
                i = 0
                while i < len(items):
                    text += "\n<J><a href='event:shop:buyItem-%s-%s'>[x]</a> <N> %s - %s %s" %(tab - 1, i + 1, items[str(i + 1)], this.server.menu["shop"]["firsts" if tab == 2 else "bootcamps" if tab == 3 else "savesnormal" if tab == 4 else "savesdificil" if tab == 5 else "savesdivino" if tab == 6 else "vip" if tab == 7 else "fichas" if tab == 8 else "coletados"][str(i + 1)], coins)
                    i += 1
            this.client.room.updateTextArea(10014, text, this.client.playerName)  
            this.currentPage = page

    def buyItem(this, type, id):
        if _time.time() - this.client.CMDTime > 0.5:
            this.client.CMDTime = _time.time()
            this.client.room.removeTextArea(10014, this.client.playerName)
            this.client.room.addTextArea(10004, this.client.getText("shop.main", this.client.playerName, this.client.nowCoins), this.client.playerName, 200, 95, 495, 380, 0, 0, 0, False)
            typeName = "firsts" if type == 1 else "bootcamps" if type == 2 else "savesnormal" if type == 3 else "savesdificil" if type == 4 else "savesdivino" if type == 5 else "vip" if type == 6 else "fichas" if type == 7 else "coletados"
            item = this.server.menu["shop"][typeName][str(id)][0] if type == 14 or type == 15 else this.client.getText("shop.items." + str(typeName) + "." + str(id))
            price = this.server.menu["shop"][typeName][str(id)][1] if type == 14 or type == 15 else this.server.menu["shop"][typeName][str(id)]
            this.client.room.updateTextArea(10004, this.client.getText("shop.confirmBuy", item, price, type, id, type + 1, this.currentPage), this.client.playerName)
                    
    def confirmBuyItem(this, type, id):
        if _time.time() - this.client.CMDTime > 0.5:
            this.client.CMDTime = _time.time()
            typeName = "firsts" if type == 1 else "bootcamps" if type == 2 else "savesnormal" if type == 3 else "savesdificil" if type == 4 else "savesdivino" if type == 5 else "vip" if type == 6 else "fichas" if type == 7 else "coletados"
            item = this.server.menu["shop"][typeName][str(id)][0] if type == 14 or type == 15 else this.client.getText("shop.items." + str(typeName) + "." + str(id))
            price = this.server.menu["shop"][typeName][str(id)][1] if type == 14 or type == 15 else this.server.menu["shop"][typeName][str(id)]
            canBuy = True

            if this.client.nowCoins < price:
                canBuy = False
                this.client.room.updateTextArea(10004, this.client.getText("shop.buyErrorNoCoins", type + 1, this.currentPage) if type == 9 or type == 10 else this.client.getText("shop.buyErrorNoCoins", item, type + 1, this.currentPage), this.client.playerName)

            if canBuy:
                this.client.room.updateTextArea(10004, this.client.getText("shop.buySucess", type + 1, this.currentPage) if type == 9 or type == 10 else this.client.getText("shop.buySucess", item, type + 1, this.currentPage), this.client.playerName)
                this.client.nowCoins -= price
                if type == 1:
                    if id == 1:
                        this.client.cheeseCount += 200
                        this.client.firstCount += 200
                    elif id == 2:
                        this.client.cheeseCount += 400
                        this.client.firstCount += 400
                    elif id == 3:
                        this.client.cheeseCount += 600
                        this.client.firstCount += 600
                    elif id == 4:
                        this.client.cheeseCount += 800
                        this.client.firstCount += 800
                    elif id == 5:
                        this.client.cheeseCount += 1000
                        this.client.firstCount += 1000

                elif type == 2:
                    if id == 1:
                        this.client.bootcampCount += 200
                    elif id == 2:
                        this.client.bootcampCount += 400
                    elif id == 3:
                        this.client.bootcampCount += 600
                    elif id == 4:
                        this.client.bootcampCount += 800
                    elif id == 5:
                        this.client.bootcampCount += 1000

                elif type == 3:
                    if id == 1:
                        this.client.shamanSaves += 200
                    elif id == 2:
                        this.client.shamanSaves += 400
                    elif id == 3:
                        this.client.shamanSaves += 600
                    elif id == 4:
                        this.client.shamanSaves += 800
                    elif id == 5:
                        this.client.shamanSaves += 1000

                elif type == 4:
                    if id == 1:
                        this.client.hardModeSaves += 200
                    elif id == 2:
                        this.client.hardModeSaves += 400
                    elif id == 3:
                        this.client.hardModeSaves += 600
                    elif id == 4:
                        this.client.hardModeSaves += 800
                    elif id == 5:
                        this.client.hardModeSaves += 1000

                elif type == 5:
                    if id == 1:
                        this.client.divineModeSaves += 200
                    elif id == 2:
                        this.client.divineModeSaves += 400
                    elif id == 3:
                        this.client.divineModeSaves += 600
                    elif id == 4:
                        this.client.divineModeSaves += 800
                    elif id == 5:
                        this.client.divineModeSaves += 1000
                        
                elif type == 6:
                    if id == 1:
                        if not this.client.privLevel >= 2:
                            this.Cursor.execute("update Users SET VipTime = ?, PrivLevel = 2 WHERE Users = ?", [Utils.getTime() + ((24 * 31) * 3600), this.client.playerName])
                            this.Cursor.fetchall()
                            this.client.privLevel = 2
                            this.client.shamanSaves += 500
                            this.client.hardModeSaves += 500
                            this.client.divineModeSaves += 500
                            this.client.bootcampCount += 500
                            this.client.cheeseCount += 500
                            this.client.firstCount += 500
                            this.client.shopCheeses += 500
                            this.client.shopFraises += 500
                            this.client.nowCoins += 500
                            bg = '<img src="http://www.transforvida.com.br/images/icones/bgroleta.png">'
                            txt = '<p align="center"><N>Parabéns! Você comprou <ROSE>VIP<N> no <ROSE>TransforXD <N>por <ROSE>30 dias<N> e ganhou também <ROSE>500<N> moedas e firsts.</p>'
                            txtOK = '<font size="12"><V><a href="event:fecharPop">OK</a></font>'
                            this.client.sendAddPopupText(10056, 300, 130, 299, 100, '000000', '000000', 100, bg)
                            this.client.sendAddPopupText(10057, 325, 150, 225, 60, '000000', '000000', 100, txt)
                            this.client.sendAddPopupText(10058, 420, 193, 30, 60, '000000', '000000', 100, txtOK)
                            this.client.sendMessage("<ROSE>Reentre no jogo para poder desfrutar do cargo de VIP.")
                            this.client.updateDatabase()
                        else:
                            this.client.nowCoins += 5000
                            this.client.sendMessage("<ROSE>Você já possui VIP ou um cargo privilegiado no servidor.")
                    elif id in [2, 3, 4, 5]:
                        bg = '<img src="http://www.transforvida.com.br/images/icones/bgroleta.png">'
                        txt = '<p align="center">Para adquirir o cargo na equipe, acesse: <u>www.transforxd.top/lojinha</u> e escolha o plano que queira comprar.</p>'
                        txtOK = '<font size="12"><V><a href="event:fecharPop">OK</a></font>'
                        this.client.sendAddPopupText(10056, 300, 130, 299, 100, '000000', '000000', 100, bg)
                        this.client.sendAddPopupText(10057, 325, 150, 225, 60, '000000', '000000', 100, txt)
                        this.client.sendAddPopupText(10058, 420, 190, 30, 60, '000000', '000000', 100, txtOK)
                        
                elif type == 7:
                    this.client.nowTokens += (10 if id == 1 else 20 if id == 2 else 30 if id == 3 else 40 if id == 4 else 50 if id == 5 else 0)

                elif type == 8:
                    if id == 1:
                        this.client.cheeseCount += 200
                    elif id == 2:
                        this.client.cheeseCount += 400
                    elif id == 3:
                        this.client.cheeseCount += 600
                    elif id == 4:
                        this.client.cheeseCount += 800
                    elif id == 5:
                        this.client.cheeseCount += 1000

class consumablesShop:

    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.itemsCache = {}
        this.cheesesCount = 0
        this.fraisesCount = 0
        this.currentPage = 0

    def open(this):
        if _time.time() - this.client.CMDTime > 1:
            this.client.CMDTime = _time.time()
            this.desbugCache()
            this.client.close()
            this.currentPage = 1
            consumables = this.server.menu['consumables']
            this.client.room.addTextArea(10002, "<img src='https://i.hizliresim.com/V3NqYP.png'>", this.client.playerName, 10, 25, 765, 380, 0, 0, 0, False)
            this.client.sendPacket([29, 20], "\x00\x00'Y\x00\x00\x00\x91\x00_\x02l\x01\x0e\x00\x1826\x00\x1826<\x00")
            this.client.room.addTextArea(10091, "<img src='https://i.hizliresim.com/JONo2j.jpg' width='91' height='22'>", this.client.playerName, 23, 219, 100, 50, 0, 0, 0, False)
            this.client.getFull()
            this.client.room.addTextArea(10003, this.client.getText('consumablesShop.title', this.client.playerName), this.client.playerName, 170, 40, 495, 380, 0, 0, 0, False)
            slot = 0
            while slot < 6:
                if slot >= len(consumables):
                    break
                consumable = consumables[str(slot)]
                this.client.room.addTextArea(10040 + slot, "<img src='http://www.transforvida.com.br/newmenu/consumablesShop/getItem.php?cheeses=%s&fraises=%s&id=%s' hspace='-2' vspace='0'>" % (consumable[1], consumable[2], consumable[0]), this.client.playerName, 200 + 140 * slot - 420 * (slot / 3), 120 + 110 * (slot / 3), 130, 105, 0, 0, 0, False)
                this.client.room.addTextArea(10046 + slot, "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-1-" + str(slot) + "'>" if this.itemsCache.has_key(consumable[0]) else '') + '-' + ('</a>' if this.itemsCache.has_key(consumable[0]) else '') + '    <CEP>' + (this.itemsCache[consumable[0]] if this.itemsCache.has_key(consumable[0]) else '0') + '   <CH2>' + ((("<a href='event:consumablesShop:addItem-1-" + str(slot) + "'>" if this.itemsCache[consumable[0]] < 80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0) else '') if this.itemsCache.has_key(consumable[0]) else "<a href='event:consumablesShop:addItem-1-" + str(slot) + "'>") if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else '') + '+' + ((('</a>' if this.itemsCache[consumable[0]] < 80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0) else '') if this.itemsCache.has_key(consumable[0]) else '</a>') if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else '') + '</p>', this.client.playerName, 210 + 140 * slot - 420 * (slot / 3), 195 + 110 * (slot / 3), 76, 20, 0, 0, 0, False)
                slot += 1

            this.itemsPage()

    def itemsPage(this):
        consumables = this.server.menu['consumables']
        this.client.room.addTextArea(10053, "<p align='center'><b>&lt;</b></p>", this.client.playerName, 635, 160, 18, 16, 3952740, 1118481, 100, False)
        this.client.room.addTextArea(10055, "<p align='center'>" + ("<N><a href='event:consumablesShop:changePage-2'>" if len(consumables) / 6 + 1 > 1 else '<BL>') + '<b>&gt;</b>' + ('</a>' if len(consumables) % 6 + 1 > 1 else '') + '</p>', this.client.playerName, 665, 160, 18, 16, 3952740, 1118481, 100, False)
        this.client.room.addTextArea(10056, this.client.getText('consumablesShop.endBuy'), this.client.playerName, 630, 127, 60, 16, 3952740, 1118481, 100, False)
        this.client.room.addTextArea(10057, "<img src='http://www.transforvida.com.br/newmenu/consumablesShop/price.png' hspace='0' vspace='0'>", this.client.playerName, 635, 187, 20, 45, 1, 1, 0, False)
        this.client.room.addTextArea(10058, "<b><font size='13'><J>%s</font>\n<font size='7'>\n</font><font size='13'><R>%s</font></b>" % (this.cheesesCount, this.fraisesCount), this.client.playerName, 663, 187, 120, 120, 0, 0, 100, False)

    def changePage(this, page):
        if _time.time() - this.client.CMDTime > 1:
            this.client.CMDTime = _time.time()
            isCancel = page == -1
            page = this.currentPage if isCancel else page
            this.currentPage = page
            i = 10040
            while i <= 10051:
                this.client.room.removeTextArea(i, this.client.playerName)
                i += 1

            i = 10060
            while i <= 10065:
                this.client.room.removeTextArea(i, this.client.playerName)
                i += 1

            consumables = this.server.menu['consumables']
            slot = (page - 1) * 6
            while slot < (page - 1) * 6 + 6:
                if slot >= len(consumables):
                    break
                consumable = consumables[str(slot)]
                this.client.room.addTextArea(10040 + slot % 6, "<img src='http://www.transforvida.com.br/newmenu/consumablesShop/getItem.php?cheeses=%s&fraises=%s&id=%s' hspace='-2' vspace='0'>" % (consumable[1], consumable[2], consumable[0]), this.client.playerName, 200 + 140 * (slot % 6) - 420 * (slot % 6 / 3), 120 + 110 * (slot % 6 / 3), 130, 105, 0, 0, 0, False)
                this.client.room.addTextArea(10046 + slot % 6, "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-" + str(page) + '-' + str(slot % 6) + "'>" if this.itemsCache.has_key(consumable[0]) else '') + '-' + ('</a>' if this.itemsCache.has_key(consumable[0]) else '') + '    <CEP>' + (str(this.itemsCache[consumable[0]]) if this.itemsCache.has_key(consumable[0]) else '0') + '   <CH2>' + ((("<a href='event:consumablesShop:addItem-" + str(page) + '-' + str(slot % 6) + "'>" if this.itemsCache[consumable[0]] < 80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0) else '') if this.itemsCache.has_key(consumable[0]) else "<a href='event:consumablesShop:addItem-" + str(page) + '-' + str(slot % 6) + "'>") if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else '') + '+' + ((('</a>' if this.itemsCache[consumable[0]] < 80 - (this.client.playerConsumables[consumable[0]] if this.client.playerConsumables.has_key(consumable[0]) else 0) else '') if this.itemsCache.has_key(consumable[0]) else '</a>') if (this.client.playerConsumables[consumable[0]] < 80 if this.client.playerConsumables.has_key(consumable[0]) else True) else '') + '</p>', this.client.playerName, 210 + 140 * (slot % 6) - 420 * (slot % 6 / 3), 195 + 110 * (slot % 6 / 3), 76, 20, 0, 0, 0, False)
                slot += 1

            if not isCancel:
                this.client.room.updateTextArea(10053, "<p align='center'>" + ("<N><a href='event:consumablesShop:changePage-" + str(page - 1) + "'>" if page > 1 else '<BL>') + '<b>&lt;</b>' + ('</a>' if page == 0 else '') + '</p>', this.client.playerName)
                this.client.room.updateTextArea(10055, "<p align='center'>" + ("<N><a href='event:consumablesShop:changePage-" + str(page + 1) + "'>" if page < len(consumables) / 6 + 1 else '<BL>') + '<b>&gt;</b>' + ('</a>' if page == 0 else '') + '</p>', this.client.playerName)
            else:
                this.itemsPage()

    def addItem(this, page, itemIndex):
        object = this.server.menu['consumables'][str((page - 1) * 6 + itemIndex)]
        id = object[0]
        if this.itemsCache.has_key(id):
            this.itemsCache[id] += 1
        else:
            this.itemsCache[id] = 1
        this.cheesesCount += object[1]
        this.fraisesCount += object[2]
        consumables = this.server.menu['consumables']
        currentItems = []
        index = (page - 1) * 6
        consumable = 0
        while consumable < len(consumables):
            info = consumables[str(consumable)]
            if consumable >= index and consumable < index + 6:
                currentItems.append([info[0], info[1], info[2]])
            consumable += 1

        this.client.room.updateTextArea(10046 + itemIndex, "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-" + str(page) + '-' + str(itemIndex) + "'>" if this.itemsCache.has_key(currentItems[itemIndex][0]) else '') + '-' + ('</a>' if this.itemsCache.has_key(currentItems[itemIndex][0]) else '') + '    <CEP>' + (str(this.itemsCache[currentItems[itemIndex][0]]) if this.itemsCache.has_key(currentItems[itemIndex][0]) else '0') + '   <CH2>' + ((("<a href='event:consumablesShop:addItem-" + str(page) + '-' + str(itemIndex) + "'>" if this.itemsCache[currentItems[itemIndex][0]] < 80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0) else '') if this.itemsCache.has_key(currentItems[itemIndex][0]) else "<a href='event:consumablesShop:addItem-" + str(page) + '-' + str(itemIndex) + "'>") if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else '') + '+' + ((('</a>' if this.itemsCache[currentItems[itemIndex][0]] < 80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0) else '') if this.itemsCache.has_key(currentItems[itemIndex][0]) else '</a>') if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else '') + '</p>', this.client.playerName)
        this.client.room.updateTextArea(10058, "<b><font size='13'><J>%s</font>\n<font size='7'>\n</font><font size='13'><R>%s</font></b>" % (this.cheesesCount, this.fraisesCount), this.client.playerName)

    def removeItem(this, page, itemIndex):
        object = this.server.menu['consumables'][str((page - 1) * 6 + itemIndex)]
        id = object[0]
        if this.itemsCache.has_key(id):
            count = this.itemsCache[id]
            if count == 1:
                del this.itemsCache[id]
            else:
                this.itemsCache[id] = count - 1
            this.cheesesCount -= object[1]
            this.fraisesCount -= object[2]
        consumables = this.server.menu['consumables']
        currentItems = []
        index = (page - 1) * 6
        consumable = 0
        while consumable < len(consumables):
            info = consumables[str(consumable)]
            if consumable >= index and consumable < index + 6:
                currentItems.append([info[0], info[1], info[2]])
            consumable += 1

        this.client.room.updateTextArea(10046 + itemIndex, "<p align='center'><CH2>" + ("<a href='event:consumablesShop:removeItem-" + str(page) + '-' + str(itemIndex) + "'>" if this.itemsCache.has_key(currentItems[itemIndex][0]) else '') + '-' + ('</a>' if this.itemsCache.has_key(currentItems[itemIndex][0]) else '') + '    <CEP>' + (str(this.itemsCache[currentItems[itemIndex][0]]) if this.itemsCache.has_key(currentItems[itemIndex][0]) else '0') + '   <CH2>' + ((("<a href='event:consumablesShop:addItem-" + str(page) + '-' + str(itemIndex) + "'>" if this.itemsCache[currentItems[itemIndex][0]] < 80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0) else '') if this.itemsCache.has_key(currentItems[itemIndex][0]) else "<a href='event:consumablesShop:addItem-" + str(page) + '-' + str(itemIndex) + "'>") if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else '') + '+' + ((('</a>' if this.itemsCache[currentItems[itemIndex][0]] < 80 - (this.client.playerConsumables[currentItems[itemIndex][0]] if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else 0) else '') if this.itemsCache.has_key(currentItems[itemIndex][0]) else '</a>') if (this.client.playerConsumables[currentItems[itemIndex][0]] < 80 if this.client.playerConsumables.has_key(currentItems[itemIndex][0]) else True) else '') + '</p>', this.client.playerName)
        this.client.room.updateTextArea(10058, "<b><font size='13'><J>%s</font>\n<font size='7'>\n</font><font size='13'><R>%s</font></b>" % (this.cheesesCount, this.fraisesCount), this.client.playerName)

    def endBuy(this):
        if _time.time() - this.client.CMDTime > 1:
            this.client.CMDTime = _time.time()
            consumablesCount = 0 if len(this.itemsCache) == 0 else sum(this.itemsCache.values())
            if consumablesCount > 0:
                i = 10040
                while i <= 10058:
                    this.client.room.removeTextArea(i, this.client.playerName)
                    i += 1

                this.client.room.addTextArea(10060, this.client.getText('consumablesShop.buyMessage', this.client.playerName, this.client.shopCheeses, this.client.shopFraises, consumablesCount), this.client.playerName, 200, 100, 480, 250, 0, 0, 0, False)
                this.client.room.addTextArea(10061, ("<a href='event:consumablesShop:confirmBuy-0'>" if this.client.shopCheeses >= this.cheesesCount else '') + "<img src='http://www.transforvida.com.br/newmenu/consumablesShop/getPrice.php?type=0&value=%s&can=%s' hspace='0' vspace='-2'>" % (this.cheesesCount, '1' if this.client.shopCheeses >= this.cheesesCount else '0') + ('</a>' if this.client.shopCheeses >= this.cheesesCount else ''), this.client.playerName, 280, 210, 120, 60, 0, 0, 0, False)
                this.client.room.addTextArea(10062, ("<a href='event:consumablesShop:confirmBuy-1'>" if this.client.shopFraises >= this.fraisesCount else '') + "<img src='http://www.transforvida.com.br/newmenu/consumablesShop/getPrice.php?type=1&value=%s&can=%s' hspace='0' vspace='-2'>" % (this.fraisesCount, '1' if this.client.shopFraises >= this.fraisesCount else '0') + ('</a>' if this.client.shopFraises >= this.fraisesCount else ''), this.client.playerName, 480, 210, 120, 60, 0, 0, 0, False)
                this.client.room.addTextArea(10064, this.client.getText('consumablesShop.cancelBuy'), this.client.playerName, 360, 290, 150, 20, 3294800, 3294800, 100, False)

    def confirmBuy(this, withFraises):
        if _time.time() - this.client.CMDTime > 1:
            this.client.CMDTime = _time.time()
            consumablesCount = 0 if len(this.itemsCache) == 0 else sum(this.itemsCache.values())
            if withFraises:
                this.client.shopFraises -= this.fraisesCount
            else:
                this.client.shopCheeses -= this.cheesesCount
            i = 10061
            while i <= 10063:
                this.client.room.removeTextArea(i, this.client.playerName)
                i += 1

            for consumable in this.itemsCache.items():
                this.client.sendAnimZelda(-3, consumable[0])
                this.client.sendNewConsumable(consumable[0], consumable[1])
                if this.client.playerConsumables.has_key(consumable[0]):
                    this.client.playerConsumables[consumable[0]] += consumable[1]
                else:
                    this.client.playerConsumables[consumable[0]] = consumable[1]

            this.client.room.updateTextArea(10060, this.client.getText('consumablesShop.buySucess', consumablesCount, '<R>' if withFraises else '<J>', this.fraisesCount if withFraises else this.cheesesCount, this.client.getText('consumablesShop.fraises') if withFraises else this.client.getText('consumablesShop.cheeses')), this.client.playerName)
            this.client.room.updateTextArea(10064, this.client.getText('consumablesShop.returnToHome'), this.client.playerName)
            this.cheesesCount = 0
            this.fraisesCount = 0
            this.itemsCache = {}

    def desbugCache(this):
        this.cheesesCount = 0
        this.fraisesCount = 0
        this.currentPage = 0
        this.itemsCache = {}
