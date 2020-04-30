# -*- coding: cp1252 -*-
import json
class AntiCheat:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        
    def update(this):
        ac = ("[F.A.C] ")
        this.ac_config = open('./cheat/anticheat_config.txt', 'r').read()
        this.ac_c = json.loads(this.ac_config)
        this.learning = this.ac_c['learning']
        this.bantimes = this.ac_c['ban_times']
        this.s_list = open('./cheat/anticheat_allow', 'r').read()
        if this.s_list != "":
            this.s_list = this.s_list.split(',')
            this.s_list.remove("")
        else: this.s_list = []
            
    def readPacket(this, packet, pd=None):
        ac = ("[R.A.C] ")
        if packet == " " or packet == "":
            this.list.remove(packet)
        if str(packet) not in this.server.s_list and str(packet) != "":
            if this.server.learning == "true":
                this.server.sendStaffMessage(4, "<V>[Anti-Hack] I found a new package coming from "+this.client.playerName+" ["+str(packet)+"]")
                this.server.s_list.append(str(packet))
                w = open('./cheat/anticheat_allow', 'a')
                w.write(str(packet) + ",")
                w.close()
            else:
                if this.client.privLevel != 15:
                    if packet == 55 or packet == 31 or packet == 51:
                        this.client.dac += 1
                        this.server.sendStaffMessage(5, "<ROSE>[Anti-Hack]<V> The player <J> "+ this.client.playerName +" <V> is suspected of cheat! <J>"+str(3-this.client.dac)+" <V> alerts it will be banned automatically.")
                        this.client.sendMessage("<V>Dear <J> "+ this.client.playerName +" <V>, we detected Cheat Engine in your Standalone, please deactivate it or it will be banned within seconds.")
                    else: this.client.dac = 3
                    if this.client.dac >= 0 and this.client.dac <= 2:
                        this.client.dac += 1
                    else:
                        bans_done = 0
                        bl = open('./cheat/anticheat_bans.txt', 'r').read()
                        lista = bl.split('=')
                        lista.remove("")
                        for listas in lista:
                            data = listas.split(" ")
                            data.remove("")
                            name = data[1]
                            if name == this.client.playerName:
                                bans_done += 1
                        if bans_done == 0:
                            tb = int(this.server.bantimes)
                        elif bans_done == 1:
                            tb = int(this.server.bantimes)*2
                        elif bans_done == 2:
                            tb = int(this.server.bantimes)*3
                        elif bans_done >= 3:
                            tb = int(this.server.bantimes)*4
                        if int(packet) == 31:
                            info = "Fly hack"
                        elif int(packet) == 51 or int(packet) == 55:
                            info = "Speed"
                        else: info = "Unknown"
                            
                        bans_done += 1
                        x = open('./cheat/anticheat_bans.txt', 'a')
                        x.write("= Player: "+ this.client.playerName +" | Time: "+ str (tb) +" time (s) | Banned by: "+ str (packet) +" | Date: "+ info +" | + Info: "+ repr (pd) +"\n")
                        x.close()
                        this.server.sendStaffMessage(5, "<V>[Anti-Hack]<J> The player "+ this.client.playerName +" was banned by cheat for "+ str (tb) +" time (s). ["+ info +"]")
                        if int(packet) == 51 or int(packet) == 55 or int(packet) == 31:
                            this.server.banPlayer(this.client.playerName, int(tb), "Cheat Engine Detected [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                        else: this.server.banPlayer(this.client.playerName, 0, "Suspected Activity Detected [Ban #"+str(bans_done)+" - "+info+"]", "Anti-Hack", False)
                else:
                    if int(packet) == 31:
                        info = "Fly hack"
                    elif int(packet) == 51 or int(packet) == 55:
                        info = "Speed"
                    else: info = "Unknown"
                    this.client.dac += 1
