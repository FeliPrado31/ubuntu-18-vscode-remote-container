# -*- coding: cp1252 -*-
# Embedded file name: E:\George\Workspaces\Compiler\Output\BlindSource\Transformice\Package\Content\BotGuardian.py
#modulos tornado & mysql
from datetime import datetime
import random
import time
import re
import logging
import json
import sqlite3
import os
import urllib2
import xml.etree.ElementTree
import xml.parsers.expat
import sys, string, os, traceback
import struct
import math
import smtplib
import thread, threading
import time as thetime
#from requests import get
import ast
import ByteArray
import exceptions
import psutil
import string
import fnmatch
#modulos tornado & mysql
#from DBUtils.PooledDB import PooledDB
#import MySQLdb
#import mysql.connector
import thread, threading
import urllib

class Feli:

    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

    def checkproxy(this, usuario):
        if this.client.playerName.startswith("*"):
            return 0
        else:
            this.Cursor.execute('select proxy from ips where ip = %s', [this.client.ipAddress])
            rrf = this.Cursor.fetchone()
            if rrf is None:
                return 3
            else:
                return rrf[0]

    def checkIP(this, address):
        this.client.proxy = this.checkproxy(address)
        if this.client.privLevel >= 4:
            this.client.proxy == 0
            this.client.sendMessage("<font color='#FFFFFF'>Eres staff y ya puedes acceder con VPN</font>")
        else:
            if this.client.proxy == 3:
                data = urllib.urlopen('http://www.ipqualityscore.com/api/json/ip/zamA1itYGyw1n8DHaTmyg91BxRMwNQIR/'+address+'').read()
                d = json.loads(data)
                vpn = d.get('vpn')
                proxy = d.get('proxy')
                tor = d.get('tor')
                if vpn == True or proxy == True or tor == True:
                    this.client.proxy = 1
                    this.server.sendStaffMessage(7, "<V>Feli<BL> ha expulsado a <v>"+str(this.client.playerName)+"<BL> por VPN <V>"+str(address)+"")
                    this.Cursor.execute('insert into ips (ip, proxy) values (%s,%s)', [address, 1])
                    this.server.banPlayer(this.client.playerName, 0, "Uso de VPN ("+str(address)+")", "Feli", True)
                    this.client.removeClient(this.client.playerName)
                    this.client.transport.loseConnection()
                    print ("Proxy = Y")
                else:
                    this.Cursor.execute('insert into ips (ip, proxy) values (%s,%s)', [address, 0])
                    print ("Proxy = N")
            if this.client.proxy == 1:
                this.server.sendStaffMessage(7, "<V>Feli<BL> ha expulsado a <v>"+str(this.client.playerName)+"<BL> por VPN <V>"+str(address)+"")
                this.server.banPlayer(this.client.playerName, 0, "Uso de VPN ("+str(address)+")", "Feli", True)
                this.client.removeClient(this.client.playerName)
                this.client.transport.loseConnection()
                print ("proxy = 1")
            else:
                print ("No usa proxy")