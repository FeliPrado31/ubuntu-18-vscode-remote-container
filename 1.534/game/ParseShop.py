#coding: utf-8
import binascii

from ByteArray import ByteArray
from Identifiers import Identifiers

class Shop:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

    def getShopLength(this):
        return 0 if this.client.shopItems == "" else len(this.client.shopItems.split(","))

    def checkUnlockShopTitle(this):
        if this.server.shopTitleList.has_key(this.getShopLength()):
            title = this.server.shopTitleList[this.getShopLength()]
            this.client.checkAndRebuildTitleList("shop")
            this.client.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
            this.client.sendCompleteTitleList()
            this.client.sendTitleList()

    def checkAndRebuildBadges(this):
        rebuild = False
        for badge in this.server.shopBadges.items():
            if not this.client.shopBadges.has_key(badge[0]) and this.checkInShop(badge[0]):
                this.client.shopBadges[str(badge[1])] = 0
                rebuild = True

        if rebuild:
            badges = this.client.shopBadges
            this.client.shopBadges = {}
            for badge, count in badges.items():
                if not this.client.shopBadges.has_key(badge):
                    this.client.shopBadges[badge] = count

##    def checkAndRebuildBadges(this):
##        rebuild = False
##        for badge in this.server.shopBadges.items():
##            if not badge[1] in this.client.shopBadges and this.checkInShop(badge[0]):
##                this.client.shopBadges.append(str(badge[1]))
##                rebuild = True
##
##        if rebuild:
##            tempBadges = []
##            tempBadges.extend(this.client.shopBadges)
##            this.client.shopBadges = []
##            this.client.shopBadgesCounts = {}
##            for badge in tempBadges:
##                if not badge in this.client.shopBadges:
##                    this.client.shopBadges.append(badge)
##
    def checkUnlockShopBadge(this, itemID):
        if not this.client.isGuest:
            if this.server.shopBadges.has_key(itemID):
                unlockedBadge = this.server.shopBadges[itemID]
                this.sendUnlockedBadge(unlockedBadge)
                this.checkAndRebuildBadges()

    def checkInShop(this, checkItem):
        if not this.client.shopItems == "":
            for shopItem in this.client.shopItems.split(","):
                if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                    return True
        else:
            return False

    def checkInShamanShop(this, checkItem):
        if not this.client.shamanItems == "":
            for shamanItems in this.client.shamanItems.split(","):
                if checkItem == int(shamanItems.split("_")[0] if "_" in shamanItems else shamanItems):
                    return True
        else:
            return False

    def checkInPlayerShop(this, type, playerName, checkItem):
        this.Cursor.execute("select %s from Users where Username = %s" %(type), [playerName])
        for rs in this.Cursor.fetchall():
            items = rs[type]
            if not items == "":
                for shopItem in items.split(","):
                    if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                        return True
            else:
                return False

    def getItemCustomization(this, checkItem, isShamanShop):
        items = this.client.shamanItems if isShamanShop else this.client.shopItems
        if not items == "":
            for shopItem in items.split(","):
                itemSplited = shopItem.split("_")
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                if int(itemSplited[0]) == checkItem:
                    return "" if custom == "" else ("_" + custom)
        else:
            return ""

    def getShamanItemCustom(this, code):
        item = this.client.shamanItems.split(",")
        if "_" in item:
            itemSplited = item.split("_")
            custom = (itemSplited[1] if len(itemSplited) >= 2 else "").split("+")
            if int(itemSplited[0]) == code:
                packet = ByteArray().writeByte(len(custom))
                x = 0
                while x < len(custom):
                    packet.writeInt(int(custom[x], 16))
                    x += 1
                return packet.toByteArray()
        return chr(0)

    def getShopItemPrice(this, fullItem):
        itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        return this.getItemPromotion(itemCat, item, this.server.shopListCheck[str(itemCat) + "|" + str(item)][1])
                
    def getShamanShopItemPrice(this, fullItem):
        return this.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(this, itemCat, item, price):
        for promotion in this.server.shopPromotions:
            if promotion[0] == itemCat and promotion[1] == item:
                return int(promotion[2] / 100.0 * price)
        return price

    def sendShopList(this):
        this.sendShopList(True)

    def sendShopList(this, sendItems=True):
        shopItems = [] if this.client.shopItems == "" else this.client.shopItems.split(",")

        packet = ByteArray().writeInt(this.client.shopCheeses).writeInt(this.client.shopFraises).writeUTF(this.client.playerLook).writeInt(len(shopItems))
        for item in shopItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeByte(len(realCustom)+1).writeInt(int(realItem))

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeByte(0).writeInt(int(item))

        shop = this.server.shopList if sendItems else []
        packet.writeInt(len(shop))

        for item in shop:
            value = item.split(",")
            packet.writeShort(int(value[0])).writeShort(int(value[1])).writeByte(int(value[2])).writeByte(int(value[3])).writeByte(int(value[4])).writeInt(int(value[5])).writeInt(int(value[6])).writeShort(0)
                
        visuais = this.server.newVisuList
        packet.writeByte(len(visuais))
        i = len(visuais)
        for visual in visuais.items():
            packet.writeShort(visual[0])
            a = visual[1]
            packet.writeUTF("".join(a))
            packet.writeByte(visual[2])
            i -= 1

        packet.writeShort(len(this.client.clothes))

        for clothe in this.client.clothes:
            clotheSplited = clothe.split("/")
            packet.writeUTF(clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])    

        shamanItems = [] if this.client.shamanItems == "" else this.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))

        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")

                packet.writeShort(int(realItem))

                packet.writeBoolean(item in this.client.shamanLook.split(",")).writeByte(len(realCustom)+1)

                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in this.client.shamanLook.split(",")).writeByte(0)

        shamanShop = this.server.shamanShopList if sendItems else []
        packet.writeShort(len(shamanShop))

        for item in shamanShop:
            value = item.split(",")
            packet.writeInt(int(value[0])).writeByte(int(value[1])).writeByte(int(value[2])).writeByte(int(value[3])).writeInt(int(value[4])).writeShort(int(value[5]))

        this.client.sendPacket(Identifiers.send.Shop_List, packet.toByteArray())
             
    def sendShamanItems(this):
        shamanItems = [] if this.client.shamanItems == "" else this.client.shamanItems.split(",")

        packet = ByteArray().writeShort(len(shamanItems))
        for item in shamanItems:
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeShort(int(item.split("_")[0])).writeBoolean(item in this.client.shamanLook.split(",")).writeByte(len(realCustom) + 1)
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in this.client.shamanLook.split(",")).writeByte(0)
        this.client.sendPacket(Identifiers.send.Shaman_Items, packet.toByteArray())

    def sendLookChange(this):
        try:
            p = ByteArray()
            look = this.client.playerLook.split(";")
            p.writeByte(int(look[0]))

            for item in look[1].split(","):
                if "_" in item:
                    itemSplited = item.split("_")
                    realItem = itemSplited[0]
                    custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                    realCustom = [] if custom == "" else custom.split("+")
                    p.writeInt(int(realItem)).writeByte(len(realCustom))
                    x = 0
                    while x < len(realCustom):
                        p.writeInt(int(realCustom[x], 16))
                        x += 1
                else:
                    p.writeInt(int(item)).writeByte(0)

            p.writeInt(int(this.client.mouseColor, 16))
            this.client.sendPacket(Identifiers.send.Look_Change, p.toByteArray())
        except: pass

    def sendShamanLook(this):
        items = ByteArray()

        count = 0        
        for item in this.client.shamanLook.split(","):
            realItem = int(item.split("_")[0]) if "_" in item else int(item)
            if realItem != 0:
                items.writeShort(realItem)
                count += 1
        this.client.sendPacket(Identifiers.send.Shaman_Look, ByteArray().writeShort(count).writeBytes(items.toByteArray()).toByteArray())

    def sendItemBuy(this, fullItem):
        this.client.sendPacket(Identifiers.send.Item_Buy, ByteArray().writeInt(fullItem).writeByte(1).toByteArray())

    def sendUnlockedBadge(this, badge):
        this.client.room.sendAll(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(this.client.playerCode).writeShort(badge).toByteArray())

    def sendthisResult(this, type, playerName):
        this.client.sendPacket(Identifiers.send.this_Result, ByteArray().writeByte(type).writeUTF(playerName).writeByte(0).writeShort(0).toByteArray())

    def equipClothe(this, packet):
        clotheID = packet.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                this.client.playerLook = values[1]
                this.client.mouseColor = values[2]
                this.client.shamanColor = values[3]
                break
                
        this.sendLookChange()
        this.sendShopList(False)

    def saveClothe(this, packet):
        clotheID = packet.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                values[1] = this.client.playerLook
                values[2] = this.client.mouseColor
                values[3] = this.client.shamanColor
                this.client.clothes[this.client.clothes.index(clothe)] = "/".join(values)
                break

        this.sendShopList(False)

    def sendShopInfo(this):            
        this.client.sendPacket(Identifiers.send.Shop_Info, ByteArray().writeInt(this.client.shopCheeses).writeInt(this.client.shopFraises).toByteArray())

    def equipItem(this, packet):
        if this.client.isBlockAttack:
            fullItem = packet.readInt()
            itemStr = str(fullItem)
            itemCat = (0 if fullItem / 10000 == 1 else fullItem /10000) if len(itemStr) > 4 else fullItem / 100
            item = int(itemStr[2 if len(itemStr) > 3 else 1:]) if len(itemStr) >= 3 else fullItem
            itemStr = str(item)

            equip = str(item) + this.getItemCustomization(fullItem, False)

            lookList = this.client.playerLook.split(";")
            lookItems = lookList[1].split(",")
            lookCheckList = lookItems[:]
            idx = 0
            while idx < len(lookCheckList):
                lookCheckList[idx] = lookCheckList[idx].split("_")[0] if "_" in lookCheckList[idx] else lookCheckList[idx]
                idx += 1

            if itemCat <= 10:
                if lookCheckList[itemCat] == itemStr:
                    lookItems[itemCat] = "0"
                else:
                    lookItems[itemCat] = str(equip)

            elif itemCat == 21:
                lookList[0] = "1"
                color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
                this.client.mouseColor = "78583a" if this.client.mouseColor == color else color
            else:
                if lookList[0] == itemStr:
                    lookList[0] = "1"
                else:
                    lookList[0] = itemStr

            this.client.playerLook = lookList[0] + ";" + ",".join(map(str, lookItems))
            this.sendLookChange()
            this.client.isBlockAttack = False
            this.client.blockAttack()
		
    def buyItem(this, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()
        itemCat = ((fullItem - 10000) / 10000) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        this.client.shopItems += str(fullItem) if this.client.shopItems == "" else "," + str(fullItem)
        price = this.getItemPromotion(itemCat, item, this.server.shopListCheck[str(itemCat) + "|" + str(item)][1 if withFraises else 0])
        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        this.sendItemBuy(fullItem)
        this.sendShopList(False)
        this.client.sendAnimZelda(0, fullItem)
        this.checkUnlockShopTitle()
        this.checkUnlockShopBadge(fullItem)

    def customItemBuy(this, packet):
        fullItem, withFraises = packet.readInt(), packet.readBoolean()

        items = this.client.shopItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shopItems = ",".join(items)
        if withFraises:
            this.client.shopFraises -= 20
        else:
            this.client.shopCheeses -= 2000

        if len(this.client.custom) == 1:
            if not fullItem in this.client.custom:
                this.client.custom.append(fullItem)
        else:
            if not str(fullItem) in this.client.custom:
                this.client.custom.append(str(fullItem))
                
        this.sendShopList(False)

    def customItem(this, packet):
        fullItem, length = packet.readInt(), packet.readByte()
        custom = length
        customs = list()

        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = this.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                this.client.shopItems = ",".join(items)

                itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
                item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
                equip = str(item) + this.getItemCustomization(fullItem, False)
                lookList = this.client.playerLook.split(";")
                lookItems = lookList[1].split(",")

                if "_" in lookItems[itemCat]:
                    if lookItems[itemCat].split("_")[0] == str(item):
                        lookItems[itemCat] = equip
                                
                elif lookItems[itemCat] == str(item):
                    lookItems[itemCat] = equip
                this.client.playerLook = lookList[0] + ";" + ",".join(lookItems)
                this.sendShopList(False)
                this.sendLookChange()
                break

    def buyShamanItem(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()
        price = this.server.shamanShopListCheck[str(fullItem)][1 if withFraises else 0]
        this.client.shamanItems += str(fullItem) if this.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        this.sendShopList(False)
        this.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(this, packet):
        fullItem = packet.readInt()
        item = str(fullItem) + this.getItemCustomization(fullItem, True)
        itemStr = str(fullItem)
        itemCat = int(itemStr[:len(itemStr)-2])
        index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
        index -= 1
        lookItems = this.client.shamanLook.split(",")

        if "_" in lookItems[index]:
            if lookItems[index].split("_")[0] == itemStr:
                lookItems[index] = "0"
            else:
                lookItems[index] = item

        elif lookItems[index] == itemStr:
            lookItems[index] = "0"
        else:
            lookItems[index] = item

        this.client.shamanLook = ",".join(lookItems)
        this.sendShamanLook()

    def customShamanItemBuy(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shamanItems = ",".join(items)
        if withFraises:
            this.client.shopFraises -= 150
        else:
            this.client.shopCheeses -= 4000
                
        this.sendShopList(False)

    def customShamanItem(this, packet):
        fullItem, length = packet.readShort(), packet.readByte()
        customs = []
        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xFFFFFF & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                this.client.shamanItems = ",".join(items)

                item = str(fullItem) + this.getItemCustomization(fullItem, True)
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr)-2:])
                index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
                index -= 1
                lookItems = this.client.shamanLook.split(",")

                if "_" in lookItems[index]:
                    if lookItems[index].split("_")[0] == itemStr:
                        lookItems[index] = item
                                
                elif lookItems[index] == itemStr:
                    lookItems[index] = item

                this.client.shamanLook = ",".join(lookItems)
                this.sendShopList()
                this.sendShamanLook()
                break

    def buyClothe(this, packet):
        clotheID, withFraises = packet.readByte(), packet.readBoolean()
        this.client.clothes.append("%02d/%s/%s/%s" %(clotheID, "1;0,0,0,0,0,0,0,0,0,0,0", "78583a", "fade55" if this.client.shamanSaves >= 1000 else "95d9d6"))
        if withFraises:
            this.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            this.client.shopFraises -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        this.sendShopList(False)

    def sendself(this, packet):
        playerName, isShamanItem, fullItem, message = packet.readUTF(), packet.readBoolean(), packet.readShort(), packet.readUTF()
        if not this.server.checkExistingUser(playerName):
            this.sendselfResult(1, playerName)
        else:
            player = this.server.players.get(playerName)
            if player != None:
                if (player.Shop.checkInShamanShop(fullItem) if isShamanItem else player.Shop.checkInShop(fullItem)):
                    this.sendselfResult(2, playerName)
                else:
                    this.server.lastselfID += 1
                    player.sendPacket(Identifiers.send.Shop_self, ByteArray().writeInt(this.server.lastselfID).writeUTF(this.client.playerName).writeUTF(this.client.playerLook).writeBoolean(isShamanItem).writeShort(fullItem).writeUTF(message).writeBoolean(False).toByteArray())
                    this.sendselfResult(0, playerName)
                    this.server.shopselfs[this.server.lastselfID] = [this.client.playerName, isShamanItem, fullItem]
                    this.client.shopFraises -= this.getShamanShopItemPrice(fullItem) if isShamanItem else this.getShopItemPrice(fullItem)
                    this.sendShopList()
            else:
                selfs = ""
                if (this.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", playerName, fullItem)):
                    this.sendselfResult(2, playerName)
                else:
                    this.Cursor.execute("select selfs from Users where Username = %s", [playerName])
                    rs = this.Cursor.fetchone()
                    selfs = rs[0]

                selfs += ("" if selfs == "" else "/") + binascii.hexlify("|".join(map(str, [this.client.playerName, this.client.playerLook, isShamanItem, fullItem, message])))
                this.Cursor.execute("update Users set selfs = %s where Username = %s", [selfs, playerName])
                this.sendselfResult(0, playerName)

    def selfResult(this, packet):
        selfID, isOpen, message, isMessage = packet.readInt(), packet.readBoolean(), packet.readUTF(), packet.readBoolean()
        if isOpen:
            values = this.server.shopselfs[int(selfID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendLangueMessage("$DonItemRecu", this.client.playerName)

            isShamanItem = bool(values[1])
            fullItem = int(values[2])
            if isShamanItem:
                this.client.shamanItems += str(fullItem) if this.client.shamanItems == "" else ",%s" %(fullItem)
                this.sendShopList(False)
                this.client.sendAnimZelda(1, fullItem)
            else:
                this.client.shopItems += str(fullItem) if this.client.shopItems == "" else ",%s" %(fullItem)
                this.client.sendAnimZelda(0, fullItem)
                this.checkUnlockShopTitle()
                this.checkUnlockShopBadge(fullItem)

        elif not message == "":
            values = this.server.shopselfs[int(selfID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendPacket(Identifiers.send.Shop_self, ByteArray().writeInt(selfID).writeUTF(this.client.playerName).writeUTF(this.client.playerLook).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(message).writeBoolean(True).toByteArray())
            else:
                messages = ""
                this.Cursor.execute("select Messages from Users where Username = %s", [str(values[0])])
                rs = this.Cursor.fetchone()
                messages = rs[0]

                messages += ("" if messages == "" else "/") + binascii.hexlify("|".join(map(str, [this.client.playerName, this.client.playerLook, values[1], values[2], message])))
                this.Cursor.execute("update Users set Messages = %s where Username = %s", [messages, str(values[0])])

    def checkselfsAndMessages(this, lastReceivedselfs, lastReceivedMessages):
        needUpdate = False
        selfs = lastReceivedselfs.split("/")
        for this in selfs:
            if not this == "":
                values = binascii.unhexlify(this).split("|", 4)
                this.server.lastselfID += 1
                this.client.sendPacket(Identifiers.send.Shop_self, ByteArray().writeInt(this.server.lastselfID).writeUTF(values[0]).writeUTF(values[1]).writeBoolean(bool(values[2])).writeShort(int(values[3])).writeUTF(values[4] if len(values) > 4 else "").writeBoolean(False).toByteArray())
                this.server.shopselfs[this.server.lastselfID] = [values[0], bool(values[2]), int(values[3])]
                needUpdate = True

        messages = lastReceivedMessages.split("/")
        for message in messages:
            if not message == "":
                values = binascii.unhexlify(message).split("|", 4)
                this.client.sendPacket(Identifiers.send.Shop_self_Message, ByteArray().writeShort(0).writeShort(0).writeUTF(values[0]).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(values[4]).writeUTF(values[3]).writeBoolean(True).toByteArray())
                needUpdate = True

        if needUpdate:
            this.Cursor.execute("update Users set selfs = '', Messages = '' where Username = %s", [this.client.playerName])
