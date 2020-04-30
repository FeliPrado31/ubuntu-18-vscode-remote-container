#coding: utf-8
import re, sys, base64, hashlib, time as _time, random as _random

# Modules
from time import gmtime, strftime
from langues import Langues
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from datetime import datetime

class Commands:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        this.currentArgsCount = 0

    def requireNoSouris(this, playerName):
        if not playerName.startswith("*"):
            return True

    def requireArgs(this, argsCount):
        if this.currentArgsCount < argsCount:
            this.client.sendMessage("Invalid arguments.")
            return False

        return True
    
    def requireTribe(this, canUse=False, tribePerm=8):
        if (not(not this.client.tribeName == "" and this.client.room.isTribeHouse and tribePerm != -1 and this.client.tribeRanks[this.client.tribeRank].split("|")[2].split(",") [tribePerm] == "1")) if (argsCount >= 1) else "":
            canUse = True

    def parseCommandProtect(this, event_raw, EVENTRAWSPLIT, EVENTCOUNT):
        EVENTRAWSPLIT = event_raw.split(' ')
        EVENTCOUNT = len(EVENTRAWSPLIT)
        if this.client.privLevel < 12:
            this.client.sendLuaMessageAdmin("<font color='#DFE283'>["+this.client.ipAddress+"]</font> - <font color='#DFE283'>["+this.client.playerName+"]</font><ROSE> escribió el comando: <CH>/"+str(event_raw)+"")

    def parseCommand(this, command):                
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        this.currentArgsCount = argsCount
        try:
            if command in ["profil", "perfil", "profile"]:
                if this.client.privLevel >= 1:
                    this.client.sendProfile(Utils.parsePlayerName(args[0]) if len(args) >= 1 else this.client.playerName)
			
	    elif command in ["editeur", "editor"]:
                if this.client.privLevel >= 1:
                    this.client.sendPacket(Identifiers.send.Room_Type, 1)
                    this.client.enterRoom("\x03[Editeur] %s" %(this.client.playerName))
                    this.client.sendPacket(Identifiers.old.send.Map_Editor, [])

            elif command in ["bot"]:
                if this.client.privLevel >= 10:
                    botName = this.client.playerName
                    botLook = this.client.playerLook
                    botTitle = this.client.titleNumber
                    otherPlayer = False

                    if len(args) >= 1:
                        botName = Utils.parsePlayerName(args[0])
                    if len(args) >= 2:
                        if ";" in args[1]:
                            botLook = args[1]
                        else:
                            otherPlayer = True if int(args[1]) == 1 or str(args[1]) == "1" else False
                    if len(args) == 3:
                        botTitle = int(args[2])

                    for client in this.client.room.clients.values():
                        if otherPlayer:
                            if botName == client.playerName:
                                if client.privLevel >= this.client.privLevel:
                                    this.client.sendMessage("")
                                else:
                                    client.room.sendAll([8, 30], ByteArray().writeInt(client.playerCode).writeUTF(client.playerName).writeShort(client.titleNumber).writeByte(0).writeUTF(client.playerLook).writeShort(client.posX).writeShort(client.posY).writeShort(11).writeByte(250).writeShort(0).toByteArray())
                        else:
                            client.sendPacket([8, 30], ByteArray().writeInt(-20).writeUTF(botName).writeShort(botTitle).writeBoolean(True).writeUTF(botLook).writeShort(this.client.posX).writeShort(this.client.posY).writeShort(1).writeByte(11).writeShort(0).toByteArray())
                            this.client.sendServerMessageAdmin("Bot name  => %s i, Bot Title => %s, Bot Look => %s" %(botName, botTitle, botLook)) 
            
            elif command in ["luaadmin"]:
                if this.client.playerName in ["Fabri", "Omar", "Baited", "Jeikob"]:
                    this.client.isLuaAdmin = not this.client.isLuaAdmin
                    this.client.sendMessage("You can run scripts as administrator." if this.client.isLuaAdmin else "You can not run scripts as administrator anymore.")
    
            elif command in ["time", "temps"]:
                if this.client.privLevel >= 1:
                    this.client.playerTime += abs(Utils.getSecondsDiff(this.client.loginTime))
                    this.client.loginTime = Utils.getTime()
                    this.client.sendLangueMessage("", "$TempsDeJeu", this.client.playerTime / 86400, this.client.playerTime / 3600 % 24, this.client.playerTime / 60 % 60, this.client.playerTime % 60)

            elif command in ["totem"]:
                if this.client.privLevel >= 1:
                    if this.client.privLevel != 100 and this.client.shamanSaves >= 100:
                        this.client.enterRoom("\x03[Totem] %s" %(this.client.playerName))

            elif command in ["sauvertotem", "guardartotem"]:
                if this.client.room.isTotemEditor:
                    this.client.totem[0] = this.client.tempTotem[0]
                    this.client.totem[1] = this.client.tempTotem[1]
                    this.client.sendPlayerDied()
                    this.client.enterRoom(this.server.recommendRoom(this.client.langue))
                    


            elif command in ["comanditos", "cmdstaff"]:
                if this.client.privLevel >= 4:
                    message = "<p align = \"center\"><font size = \"15\"><J>Lista de comandos</font></p><p align=\"left\"><font size = \"13\">"
                    message += "<font color='#0EE5FA'>Helpers</font><br>"
                    message += "<N>/ls = <vp> Muestra la lista de jugadores y en que sala se encuentran<br>"
                    message += "<N>/mute [Usuario] [Horas] [Razón] = <vp> Mutear a un jugador por un determinado tiempo <br>"
                    message += "<N>/unmute [Usuario] = <vp> Desmutear a un jugador<br>"
                    message += "<N>/hide = <vp> Ocultar tu nombre de la lista de jugadores (Para espiar a algún infractor sin que lo noten)<br>"
                    message += "<N>/unhide = <vp> Dejar de estar oculto<br>"
                    message += "<N>/staffes = <vp> Muestra todo el equipo administrativo<br>"
                    message += "<N>/re = <vp> Revivir<br>"
                    message += "<N>/mascota = <vp> Seleccionar una mascota<br>"
                    message += "<font color='#0B57C3'>MapCrews</font><br>"
                    message += "<N>/np [Codigo] = <vp> Cargar de inmediato un mapa <br>"
                    message += "<N>/npp [Codigo] = <vp> Cargar para la siguiente ronda <br>"
                    message += "<N>/p[Categoría] = <vp> Destinar el mapa actual hacia esa categoría<br>"
                    message += "<N>/lsp[Categoría] = <vp> Ver los mapas que están en dicha categoría<br>"
                    message += "<N>/join [Usuario] = <vp> Entrar en la sala del usuario<br>"
                    message += "<N>/mapc [Mensaje] = <vp> Envía un mensaje como MapCrew<br>"
                    message += "<font color='#FF8300'>Moderadores</font><br>"
                    message += "<N>/ban [Usuario] [Horas] [Razón] = <vp> Banear a un jugador por un determinado tiempo<br>"
                    message += "<N>/unban [Usuario] = <vp> Mutear a un jugador por un determinado tiempo<br>"
                    message += "<N>/lsc = <vp> Ver el número de jugadores en linea<br>"
                    message += "<N>/settime [TiempoEnSegundos] = <vp> Agregar tiempo al mapa actual<br>"
                    message += "<N>/ip [Usuario] = <vp> Ver la ip de un jugador<br>"
                    message += "<font color='#AE0DEA'>Coordinadores</font><br>"
                    message += "<N>/smn [Mensaje] = <vp> Enviar un mensaje general con tu nombre en color rosa<br>"
                    message += "<N>/ch [Usuario] = <vp> Seleccionar el siguiente chamán<br>"
                    message += "<N>/move [NombreDeSala] = <vp> Mover a todos los jugadores de una sala a otra<br>"
                    message += "<N>/clearban = <vp> Borra toda la lista de baneados<br>"
                    message += "<N>/maxplayer = <vp> Muestra el maximo de jugadores que hubo en la sala<br>"
                    message += "<N>/ipnom [IpDelUsuario] = <vp> Ver los usuarios que han usado esa ip<br>"
                    message += "<N>/give [Usuario] [Cosa] [Cantidad] = <vp> Dar a un usuario una cantidad de first, bc, etc<br>"
                    message += "<N>/ungive [Usuario] [Cosa] [Cantidad] = <vp> Quitar a un usuario una cantidad de first, bc, etc<br>"
                    message += "<N>/evento [Mensaje] = <vp> Enviar mensajes de evento<br>"
                    message += "<N>/mjoin [Usuario] = <vp> Ingresar a la sala del jugador<br>"
                    message += "<N>/moveplayer [Usuario] [Sala] = <vp> Mover a un usuario de una sala a otra<br>"
                    message += "<N>/mm [Mensaje] = <vp> Enviar un mensaje como [Moderación]<br>"
                    message += "<N>/ccm [Mensaje] = <vp> Hablar como Coordinador<br>"
                    message += "<font color='#FE11B2'>Administradores</font><br>"
                    message += "<N>/size [Usuario] [Tamaño 1 Al 5] = <vp> Cambiar el tamaño del ratón<br>"
                    message += "<N>/unbanip [IpDelUsuario] = <vp> Desbanear dicha ip<br>"
                    message += "<N>/playerid [Usuario] = <vp> Ver la ID de un usuario<br>"
                    message += "<N>/nieve = <vp> Comenzar a nevar, vuelve a usar para quitarla<br>"
                    message += "<N>/setvip [Usuario] [TiempoEnDías] = <vp> Dar vip a un jugador por una cantidad de dias<br>"
                    message += "<N>/admin [Mensaje] = <vp> Enviar un mensaje como administrador<br>"
                    message += "<font color='#28F404'>Generales</font><br>"
                    message += "<N>/mulodrome = <vp> Iniciar el mulodrome<br>"
                    message += "<N>/removevip [Usuario] = <vp> Quitar el vip al usuario<br>"
                    message += "<N>/general [Mensaje] = <vp> Enviar un mensaje como General<br>"
                    message += "<font color='#FFFF00'>Fundadores</font><br>"
                    message += "<N>/call [Mensaje] = <vp> Enviar un susurro a todo el servidor<br>"
                    message += "<N>/resetall = <vp> Reiniciar los records del servidor<br>"
                    message += "<N>/delaccount [Usuario] = <vp> Eliminar la cuenta del usuario<br>"
                    message += "<N>/clearreports = <vp> Borrar todos los reportes<br>"
                    message += "<N>/clearcache = <vp> Limpiar el caché del servidor<br>"
                    message += "<N>/cleariptempban [Mensaje] = <vp> Eliminar todas las ip baneadas<br>"
                    message += "<N>/contraseña [Usuario] [NuevaContraseña] = <vp> Cambiar la contraseña de un usuario<br>"
                    message += "<N>/lock [Usuario] = <vp> Bloquear a un usuario del servidor<br>"
                    message += "<N>/unlock [Usuario] = <vp> Desbloquear a un usuario del servidor<br>"
                    message += "<N>/giveforall [Cosa] [Cantidad] = <vp> Dar a todo el servidor una cantidad de cosas<br>"
                    message += "<N>/teleport = <vp> Activar teletransportación<br>"
                    message += "<N>/fly = <vp> Activar fly<br>"
                    message += "<N>/speed = <vp> Activar speed<br>"
                    message += "<N>/smc [Mensaje] = <vp> Enviar un mensaje con tu nombre y la comunidad en la que estas<br>"
                    message += "<N>/fundador [Mensaje] = <vp> Enviar mensaje como fundador<br>"
                    message += "<N>/mice [Mensaje] = <vp> Enviar mensaje con el nombre del servidor<br>"
                    message += "<N>/addblack [Mensaje o Link] = <vp> Añadir un texto a la blacklist<br>"
                    message += "<p align = \"center\"><font size = \"15\"><J>Información</font></p><p align=\"left\"><font size = \"13\">"
                    message += "<vp>Todos los comandos que se encuentran aqui son los que actualmente están funcionando en el servidor<br>"
                    message += "<vp>Pronto añadiremos más comandos para cada cargo<br>"
                    message += "<vp>Cabe mencionar que el mal uso de estos comandos será directamente motivo de suspensión del cargo<br>"
                    message += "<vp>Los comandos de rangos menores a otra, pueden ser usados en cargos más altos, por ejemplo: un moderador puede usar la mayoría de comandos de un helper<br>"
                    message += "<p align = \"center\"><font size = \"12\"><J>NiceMice 2020 <vp><b></b></vp></font></p>"
                    this.client.sendLogMessage(message.replace("&#", "&amp;#").replace("&lt;", "<"))



            elif command in ["mods", "mapcrews"]:
                if this.client.privLevel >= 1:
                    staff = {}
                    staffList = "$ModoPasEnLigne" if command == "mods" else "$MapcrewPasEnLigne"
                    for player in this.server.players.values():
                        if command == "mods" and player.privLevel >= 7 and not player.privLevel == 6 or command == "mapcrews" and player.privLevel == 6:
                            if staff.has_key(player.langue.lower()):
                                names = staff[player.langue.lower()]
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                            else:
                                names = []
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                    if len(staff) >= 1:
                        staffList = "$ModoEnLigne" if command == "mods" else "$MapcrewEnLigne"
                        for list in staff.items():
                            staffList += "<br><BV>[%s]<VI> %s" %(list[0], ("<BV>, <VI>").join(list[1]))
                    this.client.sendLangueMessage("", staffList)

            elif command in ["shahoraa"]:
                if this.client.privLevel >= 7:
                    if len(args) == 0:
                        this.client.isShaman = True
                        this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(this.client.playerCode).writeUnsignedByte(this.client.shamanType).writeUnsignedByte(this.client.shamanLevel).writeShort(this.client.server.getShamanBadge(this.client.playerCode)).toByteArray())

                    else:
                        this.requireArgs(1)
                        playerName = Utils.parsePlayerName(args[0])
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.isShaman = True
                            this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.shamanType).writeUnsignedByte(player.shamanLevel).writeShort(player.server.getShamanBadge(player.playerCode)).toByteArray())

                    
            elif command in ["aviso"]:
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    message = argsNotSplited.split(" ", 1)[1]
                    player = this.server.players.get(playerName)
                    if player == None:
                        this.client.sendMessage("Usuario no encontrado:  <V>%s<BL>." %(playerName))
                    else:
                        rank = {5:"MapCrew", 6:"Moderador", 7:"Coordinador", 8:"Administrador", 9:"General", 10:"Fundador", 11:"Programador"}[this.client.privLevel]
                        player.sendMessage("<ROSE>[<b>AVISO</b>]%s %s te envió una aletra, razón: %s</ROSE>" %(rank, this.client.playerName, message))
                        this.client.sendMessage("Si alerta fue enviada a  <V>%s</V>." %(playerName))
                        this.server.sendStaffMessage(7, "<V>%s</V> Envió una alerta a <V>%s</V>. Razón: <V>%s</V>" %(this.client.playerName, playerName, message))                   
                    
                    
                    
                    
                    
            elif command in ["resettotem"]:
                if this.client.room.isTotemEditor:
                    this.client.totem = [0 , ""]
                    this.client.tempTotem = [0 , ""]
                    this.client.resetTotem = True
                    this.client.isDead = True
                    this.client.sendPlayerDied()
                    this.client.room.checkChangeMap()

            elif command in ["ls"]:
                if this.client.privLevel >= 4:
                    if len(args) >= 1:
                        community = args[0].upper()
                        users, rooms, message = 0, [], ""
                        for player in this.server.players.values():
                            if player.langue.upper() == community:
                                users += 1

                        for room in this.server.rooms.values():
                            if room.community.upper() == community:
                                rooms.append(room.name)

                        message += "<bl>Jugadores/Salas (<R>%s</R>): </bl><N>%s</N><b>/</bl><n>%s</n>" % (community, users, len(rooms))
                        for room in rooms:
                            message += "\n"
                            message += "<bl>[</bl><N><b>%s</b></N><bl>]</bl>" % room
                        this.client.sendLogMessage(message)
                    else:
                        data = []
                        for room in this.server.rooms.values():
                            if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                                data.append(["Public", room.name, room.getPlayerCount()])
                            elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                                if room.name.startswith(("*" + chr(3))):
                                    data.append(["Tribe House", room.name, room.getPlayerCount()])
                                else:
                                    data.append(["Private", room.name, room.getPlayerCount()])
                            else:
                                data.append([room.community.upper(), room.roomName, room.getPlayerCount()])
                        result = ""
                        for roomInfo in data:
                            result += "<BL>Comunidad (<J>%s<BL>) - Sala (<V>%s<BL>) total: <J>%s</J>\n" %(roomInfo[0], roomInfo[1], roomInfo[2])
                        result += "<bl>Jugadores/Salas: </bl><bl><b><j>%s</b></bl><Bl>/</Bl><g><b><J>%s</b></g>" %(len(this.server.players), len(this.server.rooms))
                        this.client.sendLogMessage(result)

            elif command in ["call"]:
                if this.client.privLevel >= 9:
                    args = argsNotSplited.split(" ", 1)
                    if len(args) == 2:
                        CM, message = args
                        CM = CM.upper()
                        count = 0
                        if CM in Langues.getLangues():
                            for player in this.server.players.values():
                                if player.langue.upper() == CM:
                                    player.tribulle.sendPacket(66, ByteArray().writeUTF(this.client.playerName.lower()).writeInt(this.client.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())
                                    count += 1
                            this.client.sendMessage("Tu mensaje se ha enviado a <V>%i</V> %s." %(CM, count, "player" if count in [0, 1] else "players"))
                        else:
                            this.client.sendMessage("Invalid community.")
            
            elif command in ["ban"]:
                if this.client.privLevel >= 6:
                    playerName = Utils.parsePlayerName(args[0])
                    time = args[1] if (argsCount >= 2) else "360"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    silent = command == "iban"
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 1080 if (hours > 1080) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    if this.server.banPlayer(playerName, hours, reason, this.client.playerName, silent):
                         this.client.sendServerMessageAdmin("<V>%s<BL> ha baneado a <V>%s<BL> durante <V>%s <V>%s. <BL>Razón: <V>%s</V>" %(this.client.playerName, playerName, hours, "hora" if hours == 1 else "horas", reason))
                    else:
                         this.client.sendMessage("<V>%s <BL>no está conectado." % (playerName))
                else:
                    playerName = Utils.parsePlayerName(args[0])
                    this.server.voteBanPopulaire(playerName, this.client.playerName, this.client.ipAddress)
                    this.client.sendBanConsideration()

            elif command in ["mute"]:
                if this.client.privLevel >= 4:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    time = args[1] if (argsCount >= 2) else ""
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 500 if (hours > 500) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    this.server.mutePlayer(playerName, hours, reason, this.client.playerName)

            elif command in ["unmute"]:
                if this.client.privLevel >= 4:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    this.client.sendServerMessageAdmin("<V>%s<BL> ha desmuteado a <V>%s<BL>." %(this.client.playerName, playerName))
                    this.server.removeModMute(playerName)
                    this.client.isMute = False

            elif command in ["resetrecord"]:
                if this.client.privLevel >= 7:    
                    mapkod = args[0]
                    if mapkod.startswith("@"): 
                        mapkod = int(mapkod[1:])
                        this.client.room.CursorMaps.execute("update Maps set Time = ? and Player = ? and RecDate = ? where Code = ?", [0, "", 0, str(mapkod)])
                        this.client.sendServerMessageAdmin("Se ha eliminado el récord del mapa @%s." %(str(mapkod)))
                    else:
                        this.client.sendMessage("{} Este mapa aún no tiene récord.".format(str(mapkod)))
                else:
                    this.client.sendMessage("El código del mapa se encuentra en la parte superior.")

            elif command in ["deleterecords"]:
                if this.client.privLevel >= 8: 
                    isim = Utils.parsePlayerName(args[0])
                    t=this.server.fastRacingRekorlar
                    if t["kayitlar"].has_key(isim):
                        s = [isim,len(t["kayitlar"][isim])]
                        if s in t["siraliKayitlar"]:
                            index = t["siraliKayitlar"].index(s)
                            t["siraliKayitlar"].pop(index)
                            
                        for mapkod in t["kayitlar"][isim]:
                            if t["maplar"].has_key(mapkod):
                                del t["maplar"][mapkod]
                                
                        del t["kayitlar"][isim]
                        this.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ? where Player = ?", [0, "", 0, isim])
                        this.client.sendServerMessageAdmin("Se han eliminado todos los récords del jugador %s." %(isim))

            elif command in ["resetdef"]:
                if this.client.privLevel >= 10:
                    this.client.room.CursorMaps.execute("update Maps set BDTime = ?, BDTimeNick = ?", [0, ""])
                    this.client.sendServerMessageAdmin("<V>%s</V> ha reiniciado todos los récords de Defilante."%(this.client.playerName))            

            elif command in ["resetall"]:
                if this.client.privLevel >= 10:
                    this.client.room.CursorMaps.execute("update Maps set Time = ?, Player = ?, RecDate = ?", [0, "", 0])
                    this.server.fastRacingRekorlar = {"maplar":{},"siraliKayitlar":[],"kayitlar":{}}
                    this.client.sendServerMessageAdmin("<V>%s</V> ha reiniciado todos los récords."%(this.client.playerName))            
                
            elif command in ["mapname"]:
                if this.client.privLevel == 6 or this.client.privLevel >= 8:
                    playerName = Utils.parsePlayerName(args[0])
                    code = args[1]
                    if code.isdigit():
                        mapInfo = this.client.room.getMapInfo(int(code[1:]))
                        if mapInfo[0] == None:
                            this.client.sendLangueMessage("", "$CarteIntrouvable")
                        else:
                            this.client.room.CursorMaps.execute("update Maps set Name = ? where Code = ?", [playerName, code])
                            this.client.sendServerMessageAdmin("El mapa <J>@"+code+"</J> ahora le pertenece a <V>"+playerName+"</V>.")

            elif command in ["resetdeath"]:
                if this.client.privLevel >= 10:
                    this.Cursor.execute("update Users set deathCount = %s", [0])
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<V>%s</V> ha reiniciado los contadores de Deathmatch."%(this.client.playerName)).toByteArray())
                   
            elif command in ["changesize", "size"]:
                if (this.client.room.roomName == "*strm_" + this.client.playerName.lower()) or this.client.privLevel >= 8:
                        playerName = Utils.parsePlayerName(args[0])
                        this.client.playerSize = 1.0 if args[1] == "off" else (500.0 if float(args[1]) > 500.0 else float(args[1]))
                        if args[1] == "off":
                            this.server.sendStaffMessage(5, "All players now have their regular size.")
                            this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBoolean(False).toByteArray())

                        elif this.client.playerSize >= float(0.1) or this.client.playerSize <= float(5.0):
                            if playerName == "*":
                                for player in this.client.room.clients.values():
                                    this.server.sendStaffMessage(5, "All players now have the size " + str(this.client.playerSize) + ".")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())
                            else:
                                player = this.server.players.get(playerName)
                                if player != None:
                                    this.server.sendStaffMessage(5, "The following players now have the size " + str(this.client.playerSize) + ": <BV>" + str(player.playerName) + "</BV>")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())
                        else:
                            this.server.sendStaffMessage(5, "Invalid size.")
                else:
                    this.server.sendStaffMessage(5, "FunCorp commands work only when the room is in FunCorp mode.")

            elif command in ["cat"]:
                if this.client.privLevel >= 8:
                    this.client.room.sendAll([5, 43], ByteArray().writeInt(this.client.playerCode).writeByte(1).toByteArray())
					
            elif command in ["smn"]:
                if this.client.privLevel >= 7:
                    for player in this.server.players.values():
                        player.sendMessage("<ROSE>[%s] %s" % (this.client.playerName, argsNotSplited))
                        
            elif command in ["unban"]:
                if this.client.privLevel >= 6:
                    playerName = Utils.parsePlayerName(args[0])
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
                            this.Cursor.execute("insert into BanLog values (%s, %s, '', '', %s, 'Unban', '')", [playerName, this.client.playerName, int(str(time.time())[:9])])
                            this.server.sendStaffMessage(5, "<V>%s <BL>desbaneo a  <V>%s<BL>." %(this.client.playerName, playerName))

            elif command in ["unbanip"]:
                if this.client.privLevel >= 8:
                    ip = args[0]
                    if ip in this.server.IPPermaBanCache:
                        this.server.IPPermaBanCache.remove(ip)
                        this.Cursor.execute("delete from IPPermaBan where IP = %s", [ip])
                        this.server.sendStaffMessage(7, "<V>%s</V> ha desbaneado la ip <V>%s</V>." %(this.client.playerName, ip))
                    else:
                        this.client.sendMessage("IP no baneada.")

            elif command in ["delaccount"]:
                if this.client.privLevel >= 10: # RECOMIENDO NO USAR
                    playerName = Utils.parsePlayerName(args[0])
                    this.Cursor.execute("delete from Users where Username = %s", [playerName])
                    this.server.sendStaffMessage(7, "%s ha eliminado la cuenta de %s"%(playerName, this.client.playerName))
                else:
                    this.client.sendMessage("Account invalid.")

            elif command in ["playerid"]:
                if this.client.privLevel >= 8:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    playerID = this.server.getPlayerID(playerName)
                    this.client.sendMessage("Player ID: %s %s." % (playerName, str(playerID)), True)
                    
            elif command in ["ping"]:
                if this.client.privLevel >= 1:
                    if len(args) == 0:
                        player = this.server.players.get(str(this.client.playerName))
                        this.client.getPing(player.ipAddress, '')

                    elif len(args) == 1:
                        playerName = this.client.TFMUtils.parsePlayerName(args[0])
                        if this.server.checkConnectedAccount(playerName):
                            player = this.server.players.get(this.client.TFMUtils.parsePlayerName(args[0]))
                            this.client.getPing(player.ipAddress, playerName)
                        else:
                            this.client.sendMessage("%s no existe." % (playerName))

                else:
                    this.client.sendMessage("<R>Error, inténtalo de nuevo.")

            elif command in ["cargo", "rango", "rank"]:
                if this.client.privLevel >= 10 or this.client.playerName in ["Fabri", "Omar", "Jeikob", "Baited"]:
                    this.requireArgs(2)
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendClientMessage("No fue posible encontrar al usuario: <V>"+playerName+"<BL>.")
                    else:
                        privLevel = 11 if rank.startswith("prog") else 10 if rank.startswith("fundador") else 9 if rank.startswith("general") else 8 if rank.startswith("admin") else 7 if rank.startswith("coord") or rank.startswith("ccm") else 6 if rank.startswith("mod") else 5 if rank.startswith("map") or rank.startswith("mpc") else 4 if rank.startswith("helper") else 3 if rank.startswith("svip") else 2 if rank.startswith("vip") else 1
                        rankName = "Programador" if rank.startswith("prog") else "Fundador" if rank.startswith("fundador") else "General" if rank.startswith("general") else "Administrador" if rank.startswith("admin") else "Coordinador" if rank.startswith("coord") or rank.startswith("ccm") else "Moderador" if rank.startswith("mod") else "MapCrew" if rank.startswith("map") or rank.startswith("mpc") else "Helper" if rank.startswith("helper") else "Súper Vip" if rank.startswith("svip") else "Vip" if rank.startswith("vip") else "Jugador"
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = privLevel
                            player.TitleNumber = 0
                        this.Cursor.execute("update Users set PrivLevel = %s, TitleNumber = 0, UnRanked = %s where Username = %s", [privLevel, 1 if privLevel > 5 else 0, playerName])
                        this.server.sendStaffMessage(5, "<V>"+this.client.playerName+"<BL> ha dado rango de <V>"+rankName+"<BL> a <V>"+playerName+"")
                elif this.client.privLevel == 9:
                    this.requireArgs(2)
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendClientMessage("No fue posible encontrar al usuario: <V>"+playerName+"<BL>.")
                    else:
                        privLevel = 8 if rank.startswith("admin") else 7 if rank.startswith("coord") or rank.startswith("ccm") else 6 if rank.startswith("mod") else 5 if rank.startswith("map") or rank.startswith("mpc") else 4 if rank.startswith("helper") else 2 if rank.startswith("vip") else 1
                        rankName = "Administrador" if rank.startswith("admin") else "Coordinador" if rank.startswith("coord") or rank.startswith("ccm") else "Moderador" if rank.startswith("mod") else "MapCrew" if rank.startswith("map") or rank.startswith("mpc") else "Helper" if rank.startswith("helper") else "Vip" if rank.startswith("vip") else "Jugador"
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = privLevel
                            player.TitleNumber = 0
                        this.Cursor.execute("update Users set PrivLevel = %s, TitleNumber = 0, UnRanked = %s where Username = %s", [privLevel, 1 if privLevel > 5 else 0, playerName])
                        this.server.sendStaffMessage(5, "<V>"+this.client.playerName+"<BL> ha dado rango de <V>"+rankName+"<BL> a <V>"+playerName+"")
                elif this.client.privLevel == 8:
                    this.requireArgs(2)
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendClientMessage("No fue posible encontrar al usuario: <V>"+playerName+"<BL>.")
                    else:
                        privLevel = 7 if rank.startswith("coord") or rank.startswith("ccm") else 5 if rank.startswith("map") or rank.startswith("mpc") else 4 if rank.startswith("helper") else 6 if rank.startswith("mod") else 2 if rank.startswith("vip") else 1
                        rankName = "Coordinador" if rank.startswith("coord") or rank.startswith("ccm") else "Moderador" if rank.startswith("mod") else "MapCrew" if rank.startswith("map") or rank.startswith("mpc") else "Helper" if rank.startswith("helper") else "Vip" if rank.startswith("vip") else "Jugador"
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = privLevel
                            player.TitleNumber = 0
                        this.Cursor.execute("update Users set PrivLevel = %s, TitleNumber = 0, UnRanked = %s where Username = %s", [privLevel, 1 if privLevel > 5 else 0, playerName])
                        this.server.sendStaffMessage(5, "<V>"+this.client.playerName+"<BL> ha dado rango de <V>"+rankName+"<BL> a <V>"+playerName+"")
                else:
                    this.client.sendMessage("<ROSE>• <N>No tienes permitido usar este Comando")	

            elif command in ["np", "npp"]:
                if this.client.privLevel >= 5:
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
                                        this.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

                            elif code.isdigit():
                                this.client.room.forceNextMap = code
                                if command == "np":
                                    if this.client.room.changeMapTimer != None:
                                        this.client.room.changeMapTimer.cancel()
                                    this.client.room.mapChange()
                                else:
                                    this.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

            elif command in ["colornick"]:
				if argsCount == 0:
					this.client.sendMessage("<font color='#FFFFFF'>Escribe</font> <font color='#FFFF00'><b>/colornick piel</b></font><font color='#FFFFFF'> y selecciona un color de piel</font>")
					this.client.sendMessage("<font color='#FFFFFF'>Escribe</font> <font color='#FFFF00'><b>/colornick chat</b></font><font color='#FFFFFF'> y selecciona un color de chat</font>")
				if argsCount == 2:
					variable = values[1].lower()
					colorelegido = values[2].lower()
					if variable == "piel":
						xxxs = int(colorelegido)
						color = hex(xxxs).replace("0x", "")
						this.client.mouseColor = str(color)
						this.client.sendMessage("<font color='#"+str(color)+"'>Este es el color de tu ratón</font>")
						this.client.Cursor.execute("update users set MouseColor = %s where Username = %s", [color, this.client.playerName])
					if variable == "chat":
						if this.client.privLevel >= 1:
							xxxs = int(colorelegido)
							color = hex(xxxs).replace("0x", "")
							this.client.chatColor = "#"+str(color)
							this.client.sendMessage("<font color='"+str(this.client.chatColor)+"'>Este es tu nuevo color de chat</font>")
							this.client.Cursor.execute("update users set colorchat = %s where Username = %s", [this.client.chatColor, this.client.playerName])
							this.client.sendMessage("<font color='"+str(this.client.chatColor)+"'>SI USAS COLORES QUE CUESTEN LEER O DAÑEN LA VISTA SERÁS SANCIONADO.</font>")
					if not variable == "piel" and not variable == "chat":
						this.client.sendMessage("<font color='#FFFFFF'>Escribe</font> <font color='#FFFF00'><b>/colornick piel</b></font><font color='#FFFFFF'> y selecciona un color de piel</font>")
						this.client.sendMessage("<font color='#FFFFFF'>Escribe</font> <font color='#FFFF00'><b>/colornick chat</b></font><font color='#FFFFFF'> y selecciona un color de chat</font>")         

            elif command in ["nickcolor"]:
                if this.client.privLevel >= 1:
					try:	
						if len(args) == 0: this.client.room.showColorPicker(10002, this.client.playerName, this.client.nickColor if this.client.nickColor == "" else 0xc2c2da, "Selecciona un color")
						x = args[0]
						if not x.startswith("#"): this.client.sendMessage("Utiliza el código Hexadecimal. (#000000)")
						else:this.client.nickColor = x[1:7] ; this.client.sendMessage("<font color='%s'>%s</font>" % (x, "Se ha cambiado el color del nombre en el chat al color seleccionado.")) 						
					except:pass

            elif command in ["lsc"]:
                if this.client.privLevel >= 6:
                    result = {}
                    for room in this.server.rooms.values():
                        if result.has_key(room.community):
                            result[room.community] = result[room.community] + room.getPlayerCount()
                        else:
                            result[room.community] = room.getPlayerCount()

                    message = "\n"
                    for community in result.items():
                        message += "<BL>%s<BL> : <J>%s\n" %(community[0].upper(), community[1])
                    message += "<BL>ALL<BL> : <J>%s" %(sum(result.values()))
                    this.client.sendLogMessage(message)

            elif command in ["skip"]:
                if this.client.privLevel >= 1 and this.client.canSkipMusic and this.client.room.isMusic and this.client.room.isPlayingMusic:
                    this.client.room.musicSkipVotes += 1
                    this.client.checkMusicSkip()
                    this.client.sendBanConsideration()

            elif command in ["pw"]:
                if this.client.privLevel >= 1:
                    if this.client.room.roomName.startswith("*") or this.client.room.roomName.startswith(this.client.playerName):
                        if len(args) == 0:
                            this.client.room.roomPassword = ""
                            this.client.sendLangueMessage("", "$MDP_Desactive")
                        else:
                            password = args[0]
                            this.client.room.roomPassword = password
                            this.client.sendLangueMessage("", "$Mot_De_Passe : %s" %(password))
                            
            elif command in ["hide"]:
                if this.client.privLevel >= 4:
                    this.client.isHidden = True
                    this.client.sendPlayerDisconnect()
                    this.client.sendMessage("Ahora eres invisible.")

            elif command in ["unhide"]:
                if this.client.privLevel >= 4:
                    if this.client.isHidden:
                        this.client.isHidden = False
                        this.client.enterRoom(this.client.room.name)
                        this.client.sendMessage("Ya no eres invisible.")

            elif command in ["reboot"]:
                if this.client.playerName in ["Fabri", "Omar", "Baited", "Jeikob"]:
                    this.server.sendServerRestart(0, 0)
                    
            elif command in ["shutdown"]:
                if this.client.playerName in ["Fabri", "Omar", "Baited", "Jeikob"]:
                    this.server.closeServer()

            elif command in ["updatesql", "guardar"]:
                if this.client.playerName in ["Fabri", "Omar", "Baited", "Jeikob", "Sebita"]:
                    for player in this.server.players.values():
                        player.updateDatabase()
                    this.server.sendStaffMessage(5, "%s ha guardado la Base de Datos." %(this.client.playerName))

            elif command in ["kill", "suicide", "mort", "die"]:
                if not this.client.isDead:
                    this.client.isDead = True
                    if not this.client.room.noAutoScore: this.client.playerScore += 1
                    this.client.sendPlayerDied()
                    this.client.room.checkChangeMap()

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
                            if titleStars > 1:
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
                            this.client.titleNumber = int(titleID)
                            for title in this.client.titleList:
                                if str(title).split(".")[0] == titleID:
                                    this.client.titleStars = int(str(title).split(".")[1])
                            this.client.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(this.client.gender).writeShort(titleID).toByteArray())

            elif command in ["sy?"]:
                if this.client.privLevel >= 5:
                    this.client.sendLangueMessage("", "$SyncEnCours : [%s]" %(this.client.room.currentSyncName))

            elif command in ["sy"]:
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.isSync = True
                        this.client.room.currentSyncCode = player.playerCode
                        this.client.room.currentSyncName = player.playerName
                        if this.client.mapCode != -1 or this.client.room.EMapCode != 0:
                            this.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode, ""])
                        else:
                            this.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode])

                        this.client.sendLangueMessage("", "$NouveauSync <V> %s" %(playerName))

            elif command in ["defrecs"]:
                if this.client.room.isBigdefilante:
                    if this.client.privLevel != 0:
                        mapList = ""
                        records = 0
                        this.client.room.CursorMaps.execute("select * from Maps where BDTimeNick = ?", [this.client.playerName])
                        for rs in this.client.room.CursorMaps.fetchall():
                            #this.client.sendLogMessage("<R>Records\n\n%s" %(mapList))
                            bestTime = rs["BDTime"]
                            records += 1
                            rec = bestTime * 0.01
                            mapList += "\n<font color='#F272A5'>%s</font> - <font color='#9a9a9a'>@%s</font> - <font color='#F272A5'>%s</font><font color='#9a9a9a'>%s</font>" %(rs["BDTimeNick"], rs["Code"], rec, "s")
                        try: this.client.sendLogMessage("<p align='center'><font color='#F272A5'>Records</font><BV>:</BV> <font color='#9a9a9a'>%s</font>\n%s</p>" %(records, mapList))
                        except: this.client.sendLogMessage("<R>So much records.</R>")
                        
            elif command in ["lb"]:
                if this.client.room.isSpeedRace:
                    this.client.sendLeaderBoard()

            elif command in ["ds"]:
                if this.client.room.isDeathmatch:
                    this.client.sendDeathBoard()
                            
            elif command in ["ch"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        if this.client.room.forceNextShaman == player:
                            this.client.sendLangueMessage("", "$PasProchaineChamane", player.playerName)
                            this.client.room.forceNextShaman = -1
                        else:
                            this.client.sendLangueMessage("", "$ProchaineChamane", player.playerName)
                            this.client.room.forceNextShaman = player

            elif re.match("p\\d+(\\.\\d+)?", command):
                if this.client.privLevel >= 5:
                    mapCode = this.client.room.mapCode
                    mapName = this.client.room.mapName
                    currentCategory = this.client.room.mapPerma
                    if mapCode != -1:
                        category = int(command[1:])
                        if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44, 45]:
                            this.server.sendStaffMessage(5, "<VP>[%s] (@%s): validate map <J>P%s</J> => <J>P%s</J>" %(this.client.playerName, mapCode, currentCategory, category))
                            this.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

            elif re.match("lsp\\d+(\\.\\d+)?", command):
                if this.client.privLevel >= 5:
                    category = int(command[3:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44]:
                        mapList = ""
                        mapCount = 0
                        this.client.room.CursorMaps.execute("select * from Maps where Perma = ?", [category])
                        for rs in this.client.room.CursorMaps.fetchall():
                            mapCount += 1
                            yesVotes = rs["YesVotes"]
                            noVotes = rs["NoVotes"]
                            totalVotes = yesVotes + noVotes
                            if totalVotes < 1: totalVotes = 1
                            rating = (1.0 * yesVotes / totalVotes) * 100
                            mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])
                            
                        try: this.client.sendLogMessage("<font size=\"12\"><N>Há</N> <BV>%s</BV> <N>maps</N> <V>P%s %s</V></font>" %(mapCount, category, mapList))
                        except: this.client.sendMessage("<R>There are too many maps and it can not be opened.</R>")

            elif command in ["lsmap", "mymaps", "mismapas"]:
                if this.client.privLevel >= (1 if len(args) == 0 else 5):
                    playerName = this.client.playerName if len(args) == 0 else Utils.parsePlayerName(args[0])
                    mapList = ""
                    mapCount = 0

                    this.client.room.CursorMaps.execute("select * from Maps where Name = ?", [playerName])
                    for rs in this.client.room.CursorMaps.fetchall():
                        mapCount += 1
                        yesVotes = rs["YesVotes"]
                        noVotes = rs["NoVotes"]
                        totalVotes = yesVotes + noVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * yesVotes / totalVotes) * 100
                        mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

                    try: this.client.sendLogMessage("<font size= \"12\"><V>%s<N>'s maps: <BV>%s %s</font>" %(playerName, mapCount, mapList))
                    except: this.client.sendMessage("<R>There are too many maps and it can not be opened.</R>")

            elif command in ["monedas"]:
                this.client.sendMessage("<font color='#FFFFFF'>¡Tienes</font> <font color='#6EDA84'><b>"+str(this.client.nowCoins)+"</b></font> <font color='#FFFFFF'>monedas!</font>")					

            elif command in ["stand"]:
                this.client.sendMessage("<font color='#FFFFFF'>Utiliza el siguiente link para descargar nuestro standalone:</font> <font color='#FFFF00'>http://nicemice.site/Standalone.rar</font>")

            elif command in ["help", "comandos", "ayuda"]:
                if this.client.privLevel >= 1:
                    message = "<p align = \"center\"><font size = \"15\"><J>Lista de comandos</font></p><p align=\"left\"><font size = \"13\">"
                    message += "<vp>Cambia el color de tu nombre en el chat escribe <N>/nickcolor<br>"
                    message += "<vp>Cambia tu color de ratón escribe <N>/colornick piel<br>"
                    message += "<vp>Cambia el color de tu letra en el chat escribe <N>/colornick chat<br>"
                    message += "<vp>Añade una mascota escribe <N>/mascotas info<br>"
                    message += "<vp>Ranking de récords <j>(solo disponible en sala #fastracing)</j> escribe <N>!lb<br>"
                    message += "<vp>Personalizar estado en el perfil escribe <N>/estado<br>"
                    message += "<vp>Ver tus monedas escribe <N>/monedas<br><br>"
                    message += "<p align = \"center\"><font size = \"15\"><J>Información</font></p><p align=\"left\"><font size = \"13\">"
                    message += "<vp>First a partir de <N>3 jugadores en sala<br>"
                    message += "<vp>Standalone ingresa en <N>http://nicemice.site/Standalone.rar<br>"
                    message += "<vp>Ranking first ingresa en <N>http://nicemice.site/ranking-firsts.php<br>"
                    message += "<vp>Tienda de títulos ingresa en <N>http://nicemice.site/tienda-titulos.php<br>"
                    message += "<vp>Tienda de títulos ingresa en <N>http://nicemice.site/tienda-titulos.php<br><br>"
                    message += "<p align = \"center\"><font size = \"11\"><J>NiceMice from <vp><b>Mundo Siuny</b></vp></font></p>"
                    message += "</font></p>"

                    this.client.sendLogMessage(message.replace("&#", "&amp;#").replace("&lt;", "<"))

            elif command in ["mapinfo"]:
                if this.client.privLevel >= 4:
                    if this.client.room.mapCode != -1:
                        totalVotes = this.client.room.mapYesVotes + this.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        Rating = (1.0 * this.client.room.mapYesVotes / totalVotes) * 100
                        rate = str(Rating).split(".")[0]
                        if rate == "Nan": rate = "0"
                        this.client.sendMessage("<V>"+str(this.client.room.mapName)+"<BL> - <V>@"+str(this.client.room.mapCode)+"<BL> - <V>"+str(totalVotes)+"<BL> - <V>"+str(rate)+"%<BL> - <V>P"+str(this.client.room.mapPerma)+"<BL>.")

            elif command in ["re", "respawn"]:
                if len(args) == 0:
                    if this.client.privLevel >= 2:
                        if not this.client.canRespawn:
                            this.client.room.respawnSpecific(this.client.playerName)
                            this.client.canRespawn = True
                            this.client.sendMessage("<vp>Recuerda que solo puedes revivir una vez.</vp>")
                else:
                    if this.client.privLevel >= 7:
                        playerName = Utils.parsePlayerName(args[0])
                        if this.client.room.clients.has_key(playerName):
                            this.client.room.respawnSpecific(playerName)

            elif command in ["staff", "equipo"]:
                if this.client.privLevel >= 1:
                    lists = ["<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>"]
                    this.Cursor.execute("select Username, PrivLevel from Users where PrivLevel > 4 AND (PrivLevel = 5 or PrivLevel = 6 or PrivLevel = 7 or PrivLevel = 8 or PrivLevel = 9 or PrivLevel = 10)")
                    r = this.Cursor.fetchall()
                    for rs in r:
                        playerName = rs[0]
                        privLevel = int(rs[1])
                        lists[{10:0, 9:1, 8:2, 7:3, 6:4, 5:5}[privLevel]] += "\n" + ("<VP> •<N> " if this.server.checkConnectedAccount(playerName) else "<R> • ") + " <N>" + playerName + "<V> - <N>[" + {10: "<font color='#FFFF00'>Fundador", 9: "<font color='#28F404'>General", 8: "<font color='#FE11B2'>Administrador", 7:"<font color='#AE0DEA'>Coordinador", 6:"<font color='#FF8300'>Moderador", 5:"<font color='#0B57C3'>MapCrew"}[privLevel] + "<N>] \n"
                this.client.sendLogMessage("<p align='center'></b></b></b></b></p><br><p align = \"center\"><font size = \"12\"><VP>• <N>Conectado<br><R>• <N>Desconectado</p>" + "".join(lists) + "</p>""<br><br>")
            
            elif command in ["staffes"]:
                if this.client.privLevel >= 4:
                    lists = ["<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>"]
                    this.Cursor.execute("select Username, PrivLevel from Users where PrivLevel > 3 AND (PrivLevel = 4 or PrivLevel = 5 or PrivLevel = 6 or PrivLevel = 7 or PrivLevel = 8 or PrivLevel = 9 or PrivLevel = 10 or PrivLevel = 11)")
                    r = this.Cursor.fetchall()
                    for rs in r:
                        playerName = rs[0]
                        privLevel = int(rs[1])
                        lists[{11:0, 10:1, 9:2, 8:3, 7:4, 6:5, 5:6, 4:7}[privLevel]] += "\n" + ("<VP> •<N> " if this.server.checkConnectedAccount(playerName) else "<R> • ") + " <N>" + playerName + "<V> - <N>[" + {10: "<font color='#FFFF00'>Fundador", 11: "<font color='#FFFFFF'>Programador", 9: "<font color='#28F404'>General", 8: "<font color='#FE11B2'>Administrador", 7:"<font color='#AE0DEA'>Coordinador", 6:"<font color='#FF8300'>Moderador", 5:"<font color='#0B57C3'>MapCrew", 4:"<font color='#0EE5FA'>Helper"}[privLevel] + "<N>] \n"
                this.client.sendLogMessage("<p align='center'></b></b></b></b></p><br><p align = \"center\"><font size = \"12\"><VP>• <N>Conectado<br><R>• <N>Desconectado</p>" + "".join(lists) + "</p>""<br><br>")
            
            elif command in ["startsnow", "stopsnow", "nieve", "snow"]:
                if this.client.privLevel >= 8 or this.requireTribe(True):
                    this.client.room.startSnow(1000, 60, not this.client.room.isSnowing)

            elif command in ["music"]:
                if this.client.privLevel >= 8 or this.requireTribe(True):
                    if len(args) == 0:
                        this.client.room.sendAll(Identifiers.old.send.Music, [])
                    else:
                        this.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

            elif command in ["estado"]:
                if this.client.privLevel >= 1:
				    try:
						estado = argsNotSplited
						if "www" in estado or "http" in estado and not this.client.privLevel <= 3:
							this.client.sendMessage("<font color='#FFFFFF'>Su estado no puede contener links</font>")
							this.server.sendStaffMessage(6, "<VP>"+str(this.client.playerName)+"<BL> intentó poner un link en su estado")
						if not estado == "" and len(estado) < 100:
							this.client.estado = str(estado)
							this.Cursor.execute('UPDATE users set estado = %s where Username = %s'%(estado, this.client.playerName))				
						if len(estado) > 100:
							this.client.sendMessage("<font color='#FFFFFF'>Su estado no puede tener más de 100 carácteres</font>")
				    except:
					    this.client.sendMessage("<font color='#FFFFFF'>Este es tu nuevo estado:</font> <font color='#6EDA84'>"+this.client.estado+"</font>")

            elif command in ["clearreports", "limpiarreportes"]:
                if this.client.privLevel >= 10:
                    this.server.reports = {}
                    this.server.sendStaffMessage(7, "<V>%s</V> deleted all ModoPwet reports." %(this.client.playerName))

            elif command in ["clearcache", "limpiarcache"]:
                if this.client.privLevel >= 10:
                    this.server.IPPermaBanCache = []
                    this.server.sendStaffMessage(7, "<V>%s</V> clear the cache of the server." %(this.client.playerName))

            elif command in ["cleariptempban"]:
                if this.client.privLevel >= 10:
                    this.server.IPTempBanCache = []
                    this.server.sendStaffMessage(8, "<V>%s</V> removed all IP bans." %(this.client.playerName))

            elif command in ["casier", "log"]:
                if this.client.privLevel >= 5:
                    if argsCount > 0:
                        playerName = Utils.parsePlayerName(args[0])
                        this.requireNoSouris(playerName)
                        yazi = "<p align='center'><N>Sanction Logs</N>\n</p><p align='left'>Currently running sanctions: (<V>"+playerName+"</V>)</p>"
                        this.Cursor.execute("select * from bmlog where Name = %s order by Timestamp desc limit 0, 200", [playerName])
                        for rs in this.Cursor.fetchall():
                            isim,durum,timestamp,bannedby,time,reason = rs[0],rs[1],rs[2],rs[3],rs[4],rs[5]
                            baslangicsure = str(datetime.fromtimestamp(float(int(timestamp))))
                            bitis = (int(time)*60*60)
                            bitissure = str(datetime.fromtimestamp(float(int(timestamp)+bitis)))
                            yazi = yazi+"<font size='12'><p align='left'> - <b><V>"+durum+" "+time+"h</V></b> by "+bannedby+" : <BL>"+reason+"</BL>\n"
                            yazi = yazi+"<p align='left'><font size='9'><N2>    "+baslangicsure+" --> "+bitissure+" </N2>\n\n"
                        this.client.sendLogMessage(yazi)    
                    else:
                        yazi = "<p align='center'>Sanction Logs\n\n"
                        this.Cursor.execute("select * from bmlog order by Timestamp desc limit 0, 200")
                        for rs in this.Cursor.fetchall():
                            isim,durum,timestamp,bannedby,time,reason = rs[0],rs[1],rs[2],rs[3],rs[4],rs[5]
                            baslangicsure = str(datetime.fromtimestamp(float(int(timestamp))))
                            bitis = (int(time)*60*60)
                            bitissure = str(datetime.fromtimestamp(float(int(timestamp)+bitis)))
                            yazi = yazi+"<font size='12'><p align='left'><J>"+isim+"</J> <b><V>"+durum+" "+time+"h</V></b> by "+bannedby+" : <BL>"+reason+"</BL>\n"
                            yazi = yazi+"<p align='left'><font size='9'><N2>    "+baslangicsure+" --> "+bitissure+" </N2>\n\n"
                        this.client.sendLogMessage(yazi)

            elif command in ["snowboard"]:
                try:
                    if len(args) > 0:
                        if this.client.room.roomName == "*strm_" + this.client.playerName.lower():
                            if this.client.room.isFunCorp:
								player = this.server.players.get(Utils.parsePlayerName(args[0]))
								player.room.sendAll([100, 69], ByteArray().writeInt(player.playerCode).writeUTF("$Snowboard").writeShort(0).writeShort(15).toByteArray()) ; player.sendMessage("%s sana snowboard verdi!" % (this.client.playerName)) ; this.client.sendMessage("Snowboard gönderildi!")
                        else:
                            this.client.sendMessage("FunCorp must be opened for execute this command.")
                    else:
                        this.client.room.sendAll([100, 69], ByteArray().writeInt(this.client.playerCode).writeUTF("$Snowboard").writeShort(0).writeShort(15).toByteArray()) ; this.client.sendMessage("Snowboard zamanı!")
                except Exception as e: this.client.sendMessage("Snowboard error: %s" % (e))

            elif command in ["move"]:
                if this.client.privLevel >= 7:
                    for player in this.client.room.clients.values():
                        player.enterRoom(argsNotSplited)

##            elif command in ["clearcasier", "clearlog"]: # RECOMIENDO NO USAR PLOX
##                if this.client.privLevel == 11:
##                    this.Cursor.execute("DELETE FROM banlog")
##                    this.Cursor.execute("DELETE FROM userpermaban")
##                    this.Cursor.execute("DELETE FROM usertempban")
##                    this.Cursor.execute("DELETE FROM ippermaban")
##                    this.Cursor.execute("DELETE FROM bmlog")
##                    this.client.sendServerMessageAdmin("%s borró los logs." %(this.client.playerName))
                
            elif command in ["settime"]:
                if this.client.privLevel >= 6:
                    time = args[0]
                    if time.isdigit():
                        iTime = int(time)
                        iTime = 5 if iTime < 5 else (32767 if iTime > 32767 else iTime)
                        for player in this.client.room.clients.values():
                            player.sendRoundTime(iTime)
                        this.client.room.changeMapTimers(iTime)

            elif command in ["contraseña"]:
                if this.client.privLevel >= 9:
                    this.requireArgs(2)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    password = args[1]
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Player invalid:  <V>%s</V>." %(playerName))
                    else:
                        this.Cursor.execute("update Users set Password = %s where Username = %s", [base64.b64encode(hashlib.sha256(hashlib.sha256(password).hexdigest() + "\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0").digest()), playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> ha cambiado la contraseña de <V>%s</V> ." %(this.client.playerName, playerName))

                        player = this.server.players.get(playerName)
                        if player != None:
                            player.sendLangueMessage("", "$Changement_MDP_ok")
                                                 
            elif command in ["playersql"]:
                if this.client.privLevel == 11:
                    playerName = Utils.parsePlayerName(args[0])
                    paramter = args[1]
                    value = args[2]
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.transport.loseConnection()

                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Player invalid:  <V>%s</V>." %(playerName))
                    else:
                        try:
                            this.Cursor.execute("update Users set %s = %s where Username = %s" %(paramter), [value, playerName])
                            this.server.sendStaffMessage(7, "%s <V>%s</V> updated player with SQL information. <T>%s</T> -> <T>%s</T>." %(this.client.playerName, playerName, paramter, value))
                        except:
                            this.client.sendMessage("Invalid arguments")

            elif command in ["clearban"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.voteBan = []
                        this.server.sendStaffMessage(7, "<V>%s</V> <V>%s</V> all the bans of the player are deleted." %(this.client.playerName, playerName))

##            elif command in ["bootcamp", "vanilla", "survivor", "racing", "defilante", "tutorial"]:
##                this.client.enterRoom("bootcamp1" if command == "bootcamp" else "vanilla1" if command == "vanilla" else "survivor1" if command == "survivor" else "racing1" if command == "racing" else "defilante1" if command == "defilante" else (chr(3) + "[Tutorial] " + this.client.playerName) if command == "tutorial" else "Sourimenta" + this.client.playerName)

            elif command in ["inv"]:
                if this.client.privLevel >= 1:
                    if argsCount >= 1:
                        if this.client.room.isTribeHouse:
                            playerName = Utils.parsePlayerName(args[0])
                            if this.server.checkConnectedAccount(playerName) and not playerName in this.client.tribulle.getTribeMembers(this.client.tribeCode):
                                player = this.server.players.get(playerName)
                                player.invitedTribeHouses.append(this.client.tribeName)
                                player.sendPacket(Identifiers.send.Tribe_Invite, ByteArray().writeUTF(this.client.playerName).writeUTF(this.client.tribeName).toByteArray())
                                this.client.sendLangueMessage("", "$InvTribu_InvitationEnvoyee", "<V>" + player.playerName + "</V>")

            elif command in ["invkick"]:
                if this.client.privLevel >= 1:
                    if argsCount >= 1:
                        if this.client.room.isTribeHouse:
                            playerName = Utils.parsePlayerName(args[0])
                            if this.server.checkConnectedAccount(playerName) and not playerName in this.client.tribulle.getTribeMembers(this.client.tribeCode):
                                player = this.server.players.get(playerName)
                                if this.client.tribeName in player.invitedTribeHouses:
                                    player.invitedTribeHouses.remove(this.client.tribeName)
                                    this.client.sendLangueMessage("", "$InvTribu_AnnulationEnvoyee", "<V>" + player.playerName + "</V>")
                                    player.sendLangueMessage("", "$InvTribu_AnnulationRecue", "<V>" + this.client.playerName + "</V>")
                                    if player.roomName == "*" + chr(3) + this.client.tribeName:
                                        player.enterRoom(this.server.recommendRoom(this.client.langue))

            elif command in ["ip"]:
               if this.client.privLevel >= 6:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        this.client.sendMessage("<V>%s</V> : <V>%s</V>." %(playerName, player.ipAddress))

            elif command in ["kick"]:
                if this.client.privLevel >= 4:
                    playerName = Utils.parsePlayerName(args[0])
                    if playerName in ["Omar", "Fabri", "Jeikob", "Baited"]:
                        this.server.sendStaffMessage(4, "<V>%s<BL> intentó kickear a <V>"+playerName+"<BL>." %(this.client.playerName))
                    else:
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.room.removeClient(player)
                            player.transport.loseConnection()
                            this.server.sendStaffMessage(6, "<V>%s</V> ha kickeado a <V>%s</V>."%(this.client.playerName, playerName))
                        else:
                            this.client.sendMessage("<V>%s</V> no está conectado." %(playerName))

            elif command in ["find"]:
                if this.client.privLevel >= 4:
                    playerName = Utils.parsePlayerName(args[0])
                    result = ""
                    for player in this.server.players.values():
                        if playerName in player.playerName:
                            result += "\n<V>%s</V> -> <V>%s</V>" %(player.playerName, player.room.name)
                    this.client.sendMessage(result)

            elif command in ["join"]:
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    for player in this.server.players.values():
                        if playerName in player.playerName:
                            room = player.room.name
                            this.client.enterRoom(room)

            elif command in ["clearchat"]:
                if this.client.privLevel >= 5:
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 300).toByteArray())
            
            elif command in ["vamp"]:
                if this.client.privLevel >= 7:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 10:
                                this.client.sendVampireMode(False)
                    else:
                        if this.client.privLevel == 10:
                            playerName = this.Utils.parsePlayerName(args[0])
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendVampireMode(False)

            elif command in ["meep"]:
                if this.client.privLevel >= 7 and this.client.isFuncorp:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendPacket(Identifiers.send.Can_Meep, 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in this.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Meep, 1)
                        else:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Meep, 1)

            elif command in ["pink"]:
                if this.client.privLevel >= 3:
                    this.client.room.sendAll(Identifiers.send.Player_Damanged, ByteArray().writeInt(this.client.playerCode).toByteArray())

            elif command in ["transformation"]:
                if this.client.privLevel >= 8:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 7:
                                this.client.sendPacket(Identifiers.send.Can_Transformation, 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in this.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Transformation, 1)
                        else:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Transformation, 1)

            elif command in ["maxplayer"]:
                if this.client.privLevel >= 7 or this.client.isFuncorp:
                    maxPlayers = int(args[0])
                    if maxPlayers < 1: maxPlayers = 1
                    this.client.room.maxPlayers = maxPlayers
                    this.client.sendMessage("Máximo número de jugadores en esta sala: <V>" +str(maxPlayers))        

            elif command in ["shaman"]:
                if this.client.privLevel >= 7:
                    if len(args) == 0:
                        this.client.isShaman = True
                        this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(this.client.playerCode).writeUnsignedByte(this.client.shamanType).writeUnsignedByte(this.client.shamanLevel).writeShort(this.client.server.getShamanBadge(this.client.playerCode)).toByteArray())

                    else:
                        this.requireArgs(1)
                        playerName = Utils.parsePlayerName(args[0])
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.isShaman = True
                            this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.shamanType).writeUnsignedByte(player.shamanLevel).writeShort(player.server.getShamanBadge(player.playerCode)).toByteArray())

            elif command in ["lock"]:
                if this.client.privLevel >= 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Player invalid:  <V>"+playerName+"<BL>.")
                    else:
                        if this.server.getPlayerPrivlevel(playerName) < 4:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.room.removeClient(player)
                                player.transport.loseConnection()
                            this.Cursor.execute("update Users set PrivLevel = -1 where Username = %s", [playerName])
                            this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> fue bloqueado por <V>"+this.client.playerName)

            elif command in ["unlock"]:
                if this.client.privLevel >= 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Player invalid:  <V>"+playerName+"<BL>.")
                    else:
                        if this.server.getPlayerPrivlevel(playerName) == -1:
                            this.Cursor.execute("update Users set PrivLevel = 1 where Username = %s", [playerName])
                        this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> fue desbloqueado por <V>"+this.client.playerName)

## RECOMIENDO NO USAR 

            elif command in ["clearlog"]:
                if this.client.privLevel == 11:
                    this.Cursor.execute("DELETE FROM loginlog")
                    this.client.sendServerMessageAdmin("[CLEAR] %s Loginlog database cleared" %(this.client.playerName))

            elif command in ["clearcafe"]:
                if this.client.privLevel >= 10:
                    this.server.CursorCafe.execute("DELETE FROM cafetopics")
                    this.server.CursorCafe.execute("DELETE FROM cafeposts")
                    this.client.sendServerMessageAdmin("[CLEAR] %s Cafe database cleared" %(this.client.playerName))

            elif command in ["don", "regalo"]:
                if this.client.privLevel == 3 or this.client.privLevel >= 10:
                    this.client.room.sendAll([8, 43], ByteArray().writeInt(this.client.playerCode).toByteArray())

            elif command == "mascota" or command == "mascotas":
                mascota = args[0]
                if this.client.privLevel >= 2:
                    if "dragon" in mascota or "Dragon" in mascota:
                        this.client.mascota = 1
                    if "angel" in mascota or "Angel" in mascota:
                        this.client.mascota = 2
                    if "reno" in mascota or "Reno" in mascota:
                        this.client.mascota = 3
                    if "pez" in mascota or "Pez" in mascota:
                        this.client.mascota = 4
                    if "rana" in mascota or "Rana" in mascota:
                        this.client.mascota = 5
                    if "pajaro" in mascota or "Pajaro" in mascota:
                        this.client.mascota = 6
                    if "cosarara" in mascota or "Cosarara" in mascota:
                        this.client.mascota = 7
                    if "fantasma" in mascota or "Fantasma" in mascota:
                        this.client.mascota = 8
                    if "nada" in mascota:
                        this.client.mascota = 0
                    if not "dragon" in mascota and not "angel" in mascota and not "pez" in mascota and not "rana" in mascota and not "reno" in mascota and not "pajaro" in mascota and not "cosarara" in mascota and not "fantasma" in mascota and not "nada" in mascota:
                        this.client.sendMessage("<font color='#FFFFFF'>Escribe</font> <font color='#6EDA84'><b>/mascota tipo</b></font>")
                        this.client.sendMessage("<font color='#FFFFFF'>Tipos:</font> <font color='#6EDA84'><b>dragon, angel, reno, pez, rana, pajaro, cosarara, fantasma, nada</b></font>") 
                    else:
                        this.client.sendMessage("<font color='#FFFFFF'>La mascota aparecerá al comienzo de cada ronda :3</font>")
                    if this.client.mascota == 0:
                        this.client.sendMessage("<font color='#FFFFFF'>Escribe</font> <font color='#6EDA84'><b>/mascota tipo</b></font>")
                        this.client.sendMessage("<font color='#FFFFFF'>Tipos:</font> <font color='#6EDA84'><b>dragon, angel, reno, pez, rana, pajaro, cosarara, fantasma, nada</b></font>")
                else:
                    this.client.sendMessage("<font color='#FFFFFF'>MASCOTAS solo para VIPS o equipo administrativo</font>")		

            elif command in ["loginlog"]:
                if this.client.privLevel >= 7:
                    playerName = this.client.playerName if len(args) is 0 else "" if "." in args[0] else Utils.parsePlayerName(args[0])
                    ip = args[0] if len(args) != 0 and "." in args[0] else ""
                    if playerName != "":
                        this.Cursor.execute("select IP, Time, Country from LoginLogs where Username = %s", [playerName])
                        r = this.Cursor.fetchall()
                        message = "<p align='center'>Connection logs for player: <V>"+playerName+"</V>\n</p>"
                        for rs in r:
                            message += "<p align='left'><V>[%s]</V> %s ( <FC>%s</FC> - <VI>%s</VI> )<br>" % (playerName, str(rs[1]), str(rs[0]), rs[2])
                        this.client.sendLogMessage(message)

                    elif ip != "":
                        this.Cursor.execute("select Username, Time, Country from LoginLogs where IP = %s", [ip])
                        r = this.Cursor.fetchall()
                        message = "<p align='center'>Connection logs for ip: <V>"+ip+"</V>\n</p>"
                        for rs in r:
                            message += "<p align='left'><V>[%s]</V> %s ( <FC>%s</FC> - <VI>%s</VI> ) - %s<br>" % (str(rs[0]), str(rs[1]), ip, rs[2], this.server.miceName)
                        this.client.sendLogMessage(message)

            elif command in ["ipnom"]:
                if this.client.privLevel >= 7:
                    ip = args[0]
                    nameList = "Lista de usuarios de IP: "+ip
                    historyList = "Historia de IP :"
                    for player in this.server.players.values():
                        if player.ipAddress == ip:
                            nameList += "<br>" + player.playerName

                    this.Cursor.execute("select Username from loginlogs where IP = %s", [ip])
                    r = this.Cursor.fetchall()
                    for rs in r:
                        historyList += "<br>" + rs[0]

                    this.client.sendMessage(nameList)
                    this.client.sendMessage(historyList)
                    this.server.sendStaffMessage(9, "<V>"+this.client.playerName+"<BL> ha visto el historial de la IP: <V>"+ip+"<BL>.")

            elif command in ["giveforall"]:
                if this.client.privLevel >= 9:
                    this.requireArgs(2)
                    type = args[0].lower()
                    count = int(args[1]) if args[1].isdigit() else 0
                    type = "quesos" if type.startswith("quesos") else "fresas" if type.startswith("fresas") else "conss" if type.startswith("cons") or type.startswith("consss") else "bootcamps" if type.startswith("bootcamps") else "firsts" if type.startswith("firsts") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "monedas" if type.startswith("monedas") else "fichas" if type.startswith("fichas") else "title" if type.startswith("title") else "badge" if type.startswith("badge") else "consumables" if type.startswith("consumables") else ""
                    if count > 0 and not type == "":
                        this.server.sendStaffMessage(7, "<V>%s</V> entregó <V>%s %s</V> a los usuarios conectados." %(this.client.playerName, count, type))
                        for player in this.server.players.values():
                            if type in ["quesos", "fresas"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "quesos" else 0).writeInt(count if type == "çilek" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "quesos" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("<BL>Recibiste <V>%s %s<BL>." %(count, type))
                            if type == "quesos":
                                player.shopCheeses += count
                            elif type == "fresas":
                                player.shopFraises += count
                            elif type == "bootcamps":
                                player.bootcampCount += count
                            elif type == "firsts":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif type == "profile":
                                player.cheeseCount += count
                            elif type == "monedas":
                                player.nowCoins += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count
                            elif type == "fichas":
                                player.nowTokens += count
                            elif type == "title":
                                player.EventTitleKazan(count)
                            elif type == "badge":
                                player.winBadgeEvent(count)
                            elif type == "consumables":
                                player.sendGiveConsumables(count)
                            elif type == "cons" :
                                player.winHediye(count)

            elif command in ["give"]:
                if this.client.privLevel >= 7:
                    this.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    count = 10000 if count > 10000 else count
                    type = "quesos" if type.startswith("quesos") else "fresas" if type.startswith("fresas") else "bootcamps" if type.startswith("bootcamps") else "firsts" if type.startswith("firsts") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "monedas" if type.startswith("monedas") else "fichas" if type.startswith("fichas") else "title" if type.startswith("title") else "badge" if type.startswith("badge") else "consumables" if type.startswith("consumables") else ""
                    if count > 0 and not type == "":
                        player = this.server.players.get(playerName)
                        if player != None:
                            this.server.sendStaffMessage(7, "<V>%s le ha entregado a %s</V>: <V>%s %s</V>." %(this.client.playerName, playerName, count, type))
                            if type in ["quesos", "fresas"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "quesos" else 0).writeInt(count if type == "çilek" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "fresas" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("<BL>Recibiste <V>%s %s<BL>." %(count, type))
                            if type == "quesos":
                                player.shopCheeses += count
                            elif type == "fresas":
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
                            elif type == "hardsaves":
                                player.hardModeSaves += count
                            elif type == "divinesaves":
                                player.divineModeSaves += count
                            elif type == "monedas":
                                player.nowCoins += count
                            elif type == "fichas":
                                player.nowTokens += count
                            elif type == "badge":
                                player.winBadgeEvent(count)
                            elif type == "consumables":
                                player.giveConsumables(count)
            
            elif command in ["dar"]:
                if this.client.privLevel >= 10:
                    this.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    count = 10000 if count > 10000 else count
                    type = "quesos" if type.startswith("quesos") else "fresas" if type.startswith("fresas") else "bootcamps" if type.startswith("bootcamps") else "firsts" if type.startswith("firsts") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "monedas" if type.startswith("monedas") else "fichas" if type.startswith("fichas") else "title" if type.startswith("title") else "badge" if type.startswith("badge") else "consumables" if type.startswith("consumables") else ""
                    if count > 0 and not type == "":
                        player = this.server.players.get(playerName)
                        if player != None:
                            if type in ["quesos", "fresas"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "quesos" else 0).writeInt(count if type == "çilek" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "fresas" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("<BL>Recibiste <V>%s %s<BL>." %(count, type))
                            if type == "quesos":
                                player.shopCheeses += count
                            elif type == "fresas":
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
                            elif type == "hardsaves":
                                player.hardModeSaves += count
                            elif type == "divinesaves":
                                player.divineModeSaves += count
                            elif type == "monedas":
                                player.nowCoins += count
                            elif type == "fichas":
                                player.nowTokens += count
                            elif type == "title":
                                player.EventTitleKazan(count)
                            elif type == "badge":
                                player.winBadgeEvent(count)
                            elif type == "consumables":
                                player.giveConsumables(count)

            elif command in ["ungive"]:
                if this.client.privLevel >= 7:
                    this.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    type = "quesos" if type.startswith("quesos") else "fresas" if type.startswith("fresas") else "bootcamps" if type.startswith("bootcamps") else "firsts" if type.startswith("firsts") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "monedas" if type.startswith("monedas") or type.startswith("coins") else "fichas" if type.startswith("fichas") else "cheese1" if type.startswith("cheese1") else ""
                    yeah = False
                    if count > 0 and not type == "":
                        player = this.server.players.get(playerName)
                        if player != None:
                            this.server.sendStaffMessage(7, "<V>%s</V> by <V>%s %s</V> rolled back <V>%s</V> named player." %(this.client.playerName, count, type, playerName))
                            if type == "quesos":
                                if not count > player.shopCheeses:
                                    player.shopCheeses -= count
                                    yeah = True
                            if type == "fresas":
                                if not count > player.shopFraises:
                                    player.shopFraises -= count
                                    yeah = True
                            if type == "bootcamps":
                                if not count > player.bootcampCount:
                                    player.bootcampCount -= count
                                    yeah = True
                            if type == "firsts":
                                if not count > player.firstCount:
                                    player.cheeseCount -= count
                                    player.firstCount -= count
                                    yeah = True
                            if type == "cheese1":
                                if not count > player.cheeseCount:
                                    player.cheeseCount -= count
                                    yeah = True
                            if type == "saves":
                                if not count > player.shamanSaves:
                                    player.shamanSaves -= count
                                    yeah = True
                            if type == "hardSaves":
                                if not count > player.hardModeSaves:
                                    player.hardModeSaves -= count
                                    yeah = True
                            if type == "divineSaves":
                                if not count > player.divineModeSaves:
                                    player.divineModeSaves -= count
                                    yeah = True
                            if type == "monedas":
                                if not count > player.nowCoins:
                                    player.nowCoins -= count
                                    yeah = True
                            if type == "fichas":
                                if not count > player.nowTokens:
                                    player.nowTokens -= count
                                    yeah = True
                            if yeah:
                                player.sendMessage("<V>%s %s</V> lost." %(count, type))
                            else:
                                this.sendMessage("The player does not have that much %s already." %(type))

            elif command in ["dartitulo"]:
                if this.client.playerName in ["Omar", "Fabri", "Jeikob", "Baited", "Sebita"]:
                    if argsCount == 2:
                        playerName = Utils.parsePlayerName(args[0])
                        player = this.server.players.get(playerName)
                        if player == None:
                            this.client.sendLangueMessage("", "$erreur.tribulle2.joueurNonConnecte", playerName)
                        else:
                            titleID = str(args[1])
                            if titleID.isdigit():
                                found = False
                                for title in player.titleList:
                                    titleInfo = str(title).split(".")
                                    titleNumber = str(titleInfo[0])
                                    if titleNumber == titleID:
                                        found = True
                                        break
                                if not found:
                                    titleID = float(titleID)+0.1
                                    player.specialTitleList.append(titleID);
                                    player.sendUnlockedTitle(str(int(titleID)), "")
                                    player.sendCompleteTitleList()
                                    player.sendTitleList()
                                else:
                                    this.client.sendMessage("El usuario ya tiene el título: "+str(titleID))
                else:
                    this.client.sendMessage("Formato Incorrecto\n/"+str(command)+" user title")

            elif command in ["unranked"]:
                if this.client.privLevel == 11:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Player invalid:  <V>%s</V>." %(playerName))
                    else:
                        this.Cursor.execute("update Users set UnRanked = %s where Username = %s", [1 if command == "unranked" else 0, playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> foi %s ranking by <V>%s</V>." %(playerName, "removed do" if command == "unranked" else "colocado novamente no", this.client.playerName))

            elif command in ["changepoke", "changeanime", "poke"]:
                    if (this.client.room.roomName == "*strm_" + this.client.playerName.lower()) or this.client.privLevel in [5, 10, 11] or this.client.isFuncorp or not this.client.privLevel in [6, 7, 8, 9]:
                            playerName = Utils.parsePlayerName(args[0])
                            player = this.server.players.get(playerName)
                            skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                            number = float(args[1])
                            if args[1] == "off":
                                this.client.sendMessage("All players back to normal size.")
                                skin = skins[int(number)]
                                p = ByteArray()
                                p.writeInt(0)
                                p.writeUTF(skin)
                                p.writeByte(3)
                                p.writeInt(player.playerCode)
                                p.writeShort(-30)
                                p.writeShort(-35)
                                this.client.room.sendAll([29, 19], p.toByteArray())
                                this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBoolean(False).toByteArray())

                            elif number >= 0:
                                if playerName == "*":
                                    for player in this.client.room.clients.values():
                                        skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                                        number = args[1]
                                        
                                        if int(number) in skins:
                                            #this.client.useAnime += 1
                                            skin = skins[int(number)]
                                            p = ByteArray()
                                            p.writeInt(0)
                                            p.writeUTF(skin)
                                            p.writeByte(3)
                                            p.writeInt(player.playerCode)
                                            p.writeShort(-30)
                                            p.writeShort(-35)
                                            this.client.room.sendAll([29, 19], p.toByteArray())
##                                        this.client.sendMessage("All players skin: " + str(skin) + ".")
                                        #this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())
                                else:
                                    player = this.server.players.get(playerName)
                                    if player != None:
                                        skins = {0: '1534bfe985e.png', 1: '1507b2e4abb.png', 2: '1507bca2275.png', 3: '1507be4b53c.png', 4: '157f845d5fa.png', 5: '1507bc62345.png', 6: '1507bc98358.png', 7: '157edce286a.png', 8: '157f844c999.png', 9: '157de248597.png', 10: '1507b944d89.png', 11: '1507bcaf32c.png', 12: '1507be41e49.png', 13: '1507bbe8fe3.png', 14: '1507b8952d3.png', 15: '1507b9e3cb6.png', 16: '1507bcb5d04.png', 17: '1507c03fdcf.png', 18: '1507bee9b88.png', 19: '1507b31213d.png', 20: '1507b4f8b8f.png', 21: '1507bf9015d.png', 22: '1507bbf43bc.png', 23: '1507ba020d2.png', 24: '1507b540b04.png', 25: '157d3be98bd.png', 26: '1507b75279e.png', 27: '1507b921391.png', 28: '1507ba14321.png', 29: '1507b8eb323.png', 30: '1507bf3b131.png', 31: '1507ba11258.png', 32: '1507b8c6e2e.png', 33: '1507b9ea1b4.png', 34: '1507ba08166.png', 35: '1507b9bb220.png', 36: '1507b2f1946.png', 37: '1507b31ae1f.png', 38: '1507b8ab799.png', 39: '1507b92a559.png', 40: '1507b846ea8.png', 41: '1507bd2cd60.png', 42: '1507bd7871c.png', 43: '1507c04e123.png', 44: '1507b83316b.png', 45: '1507b593a84.png', 46: '1507becc898.png', 47: '1507befa39f.png', 48: '1507b93ea3d.png', 49: '1507bd14e17.png', 50: '1507bec1bd2.png'}
                                        number = args[1]
                                        if int(number) in skins:
                                            #this.client.useAnime += 1
                                            skin = skins[int(number)]
                                            p = ByteArray()
                                            p.writeInt(0)
                                            p.writeUTF(skin)
                                            p.writeByte(3)
                                            p.writeInt(player.playerCode)
                                            p.writeShort(-30)
                                            p.writeShort(-35)
                                            this.client.room.sendAll([29, 19], p.toByteArray())
                                        #this.client.sendMessage("New size: " + str(this.client.playerSize) + " for : <BV>" + str(player.playerName) + "</BV>")
                                        #this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())

            elif command in ["teleport"]:
                if this.client.privLevel >= 10:
                    this.client.isTeleport = not this.client.isTeleport
                    this.client.room.bindMouse(this.client.playerName, this.client.isTeleport)
                    this.client.sendMessage("Teleport Hack: " + ("<VP>On" if this.client.isTeleport else "<R>Off") + " !")

            elif command in ["fly"]:
                if this.client.privLevel >= 10:
                    this.client.isFly = not this.client.isFly
                    this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.isFly)
                    this.client.sendMessage("Fly Hack: " + ("<VP>On" if this.client.isFly else "<R>Off") + " !")

            elif command in ["speed"]:
                if this.client.privLevel >= 10:
                    this.client.isSpeed = not this.client.isSpeed
                    this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.isSpeed)
                    this.client.sendMessage("Speed Hack: " + ("<VP>On" if this.client.isSpeed else "<R>Off") + " !")				

            elif command in ["smc"]:
                if this.client.privLevel >= 10:
                    for player in this.server.players.values():
                        player.sendMessage("<VP>[%s] [%s] %s" % (this.client.langue, this.client.playerName, argsNotSplited))

            elif command in ["special"]:
                if this.client.privLevel >= 10:
                    message = "<ROSE>"+argsNotSplited
                    for player in this.client.room.clients.values():
                        player.sendLangueMessage("", message)

            elif command in ["mjj"]:
                roomName = args[0]
                if roomName.startswith("#"):
                    if roomName.startswith("#utility"):
                        this.client.enterRoom(roomName)
                    else:
                        this.client.enterRoom(roomName + "1")
                else:
                    this.client.enterRoom(({0:"", 1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[this.client.lastGameMode]) + roomName)

            elif command == "prog":
                if this.client.privLevel >= 10:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF("<N>• <font color='#FFFFFF'>[Programador "+this.client.playerName+"]</font> <N>» "+message+"").toByteArray())

            elif command == "fundador":
                if this.client.privLevel >= 10:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF("<N>• <font color='#FFFF00'>[Fundador "+this.client.playerName+"]</font> <N>» "+message+"").toByteArray())
            
            elif command == "general":
                if this.client.privLevel == 9 or this.client.privLevel >= 10:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF( "<N>• <font color='#2AE64F'>[General "+this.client.playerName+"]</font> <N>» "+message+"").toByteArray())
            
            elif command == "admin":
                if this.client.privLevel == 8 or this.client.privLevel >= 10:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF("<N>• <ROSE>[Administrador "+this.client.playerName+"]</font> <N>» "+message+"").toByteArray())

            elif command == "ccm" or command == "coord":
                if this.client.privLevel == 7 or this.client.privLevel >= 10:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF("<N>• <font color='#FFFF00'>[Coordinador "+this.client.playerName+"]</font> <N>» <font color='#0EE5FA'>"+message+"</font>").toByteArray())
                    
                    
            elif command == "mmod" or command == "modd":
                if this.client.privLevel == 6 or this.client.privLevel >= 9:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF("<N>• <font color='#FF8300'>[Moderador "+this.client.playerName+"]</font> <N>» <font color='#D0D0D0'>"+message+"</font>").toByteArray())        
                    

            elif command in ["mpc", "mapc", "mapcrew"]:
                if this.client.privLevel == 5 or this.client.privLevel >= 10:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF("<N>• <font color='#0B57C3'>[Mapcrew "+this.client.playerName+"]</font> <N>» "+message+"").toByteArray())

            elif command == "mice":
                if this.client.privLevel >= 9:
                    message = argsNotSplited
                    this.server.sendWholeServer(Identifiers.send.Message, ByteArray().writeUTF("<ROSE>• [NiceMice]</font> » <N>"+message+"").toByteArray())

            elif command == "evento":
                if this.client.privLevel >= 7:
                    message = argsNotSplited
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<ROSE>• [<N>Evento<ROSE>]</font> » <N>"+message+"").toByteArray())

            elif command == "vip":
                if this.client.privLevel == 2 or this.client.privLevel >= 9:
                    message = argsNotSplited
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#FFD700'>VIP <font color='#ffffff'>"+this.client.playerName+"</font><N>]</font> » <N>"+message).toByteArray())
            
            elif command == "svip":
                if this.client.privLevel == 3 or this.client.privLevel >= 9:
                    message = argsNotSplited
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#0EE5FA'>Super VIP <font color='#ffffff'>"+this.client.playerName+"</font><N>]</font> » <N>"+message).toByteArray())
            
            elif command == "text1":
                if this.client.privLevel == 3 or this.client.privLevel >= 9:
                    if this.client.gender in [2, 0]:     
                        message = argsNotSplited
                        this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#FFFF00'>Dios <font color='#ffffff'>"+this.client.playerName+"</font><N>]</font> <N>"+message).toByteArray())
                    else:
                        message = argsNotSplited
                        this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#FBA9FD'>Diosa <font color='#ffffff'>"+this.client.playerName+"</font><N>]</font> <N>"+message).toByteArray())

            elif command == "text2":
                if this.client.privLevel == 3 or this.client.privLevel >= 9:
                    if this.client.gender in [2, 0]:     
                        message = argsNotSplited
                        this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#ffffff'>"+this.client.playerName+"</font><font color='#0EE5FA'> Hermoso</font><N>]</font> <N>"+message).toByteArray())
                    else:
                        message = argsNotSplited
                        this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#ffffff'>"+this.client.playerName+"</font><font color='#FBA9FD'> Hermosa</font><N>]</font> <N>"+message).toByteArray())
            
            elif command == "text3":
                if this.client.privLevel == 3 or this.client.privLevel >= 9:
                    if this.client.gender in [2, 0]:     
                        message = argsNotSplited
                        this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#FFFF00'>Leyenda <font color='#ffffff'>"+this.client.playerName+"</font><N>]</font> <N>"+message).toByteArray())
                    else:
                        message = argsNotSplited
                        this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<N>[<font color='#FBA9FD'>Leyenda <font color='#ffffff'>"+this.client.playerName+"</font><N>]</font> <N>"+message).toByteArray())

            elif command in ["mulodrome"]:
                if this.client.privLevel >= 9 or this.client.room.roomName.startswith(this.client.playerName) and not this.client.room.isMulodrome:
                    for player in this.client.room.clients.values():
                        player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == this.client.playerName else 0)

            elif command in ["follow", "mjoin"]:
                if this.client.privLevel >= 7:
                    this.requireArgs(1)
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        this.client.enterRoom(player.roomName)

            elif command in ["moveplayer"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    roomName = argsNotSplited.split(" ", 1)[1]
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.enterRoom(roomName)

            elif command == "setvip" or command == "darvip":
                if this.client.privLevel >= 8:
                    this.requireArgs(2)
                    playerName = this.client.TFMUtils.parsePlayerName(args[0])
                    days = args[1]
                    this.requireNoSouris(playerName)
					
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendClientMessage("<V>"+playerName+"<BL> no existe.")
                    else:
                        this.server.setVip(playerName, int(days) if days.isdigit() else 1)
                        this.server.sendStaffMessage(7, "<V>"+this.client.playerName+"<BL> le ha dado VIP a <V>"+playerName+"<BL>.")	

            elif command in ["removevip"]:
                if this.client.privLevel >= 9:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("<V>"+playerName+"<BL> no existe.")
                    else:
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = 1
                            if player.titleNumber == 1100:
                                player.titleNumber = 0

                            player.sendMessage("<vp>Ya no eres VIP")
                            this.Cursor.execute("update Users set viptime = 0 where Username = %s", [playerName])
                        else:
                            this.Cursor.execute("update Users set PrivLevel = 1, viptime = 0, TitleNumber = 0 where Username = %s", [playerName])

                        this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> ya no es VIP")


            elif command in ["cc"]:
                if this.client.privLevel >= 7:
                    if len(args) == 1:
                        cm = args[0].upper()
                        this.client.langue = cm
                        this.client.langueID = Langues.getLangues().index(cm)
                        this.client.startBulle(this.server.recommendRoom(this.client.langue))
                    elif len(args) >= 2:
                        player, cm = this.server.players.get(args[0].capitalize()), args[1].upper()
                        player.langue = cm
                        player.langueID = Langues.getLangues().index(cm)
                        player.startBulle(player.server.recommendRoom(player.langue))

            elif command in ["mm"]:
                if this.client.privLevel >= 6:
                    this.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())

            elif command in ["addblack"]:
                if this.client.privLevel >= 10:
                    link = argsNotSplited		
                    this.Cursor.execute("insert into blacklist values (%s)", [link])	
                    this.server.sendStaffMessage(7, "<V>"+this.client.playerName+"<BL> ha agregado a la BlackList: <V>"+str(link)+"</V>.")
                   
            elif command in ["appendblack", "removeblack"]:
                if this.client.privLevel >= 7:
                    name = args[0].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                    if command == "appendblack":
                        if name in this.server.serverList:
                            this.client.sendMessage("[<R>%s</R>] já listado." %(name))
                        else:
                            this.server.serverList.append(name)
                            this.server.updateBlackList()
                            this.client.sendMessage("[<J>%s</J>] adicionado à lista" %(name))
                    else:
                        if not name in this.server.serverList:
                            this.client.sendMessage("[<R>%s</R>] Nenhuma lista." %(name))
                        else:
                            this.server.serverList.remove(name)
                            this.server.updateBlackList()
                            this.client.sendMessage("[<J>%s</J>] Removido da lista" %(name))

            elif command in ["blacklist"]:
                if this.client.privLevel >= 7:
                    blacklist = "<BL>BlackList actual:</BL>"
                    this.Cursor.execute("select links from blacklist")
                    r = this.Cursor.fetchall()
                    for rs in r:
                        blacklist += "<br>" + rs[0]

                    this.client.sendLogMessage(blacklist.replace("&#", "&amp;#").replace("&lt;", "<"))

            else:
                this.client.sendMessage("<N>Comando no encontrado.")

        except Exception as ERROR:
            import time, traceback
            c = open("./logs/BugCommands.log", "a")
            c.write("\n" + "=" * 60 + "\n- Hora: %s\n- Usuario: %s\n- Error: \n" %(time.strftime("%d/%m/%Y - %H:%M:%S"), this.client.playerName))
            traceback.print_exc(file=c)
            c.close()            
