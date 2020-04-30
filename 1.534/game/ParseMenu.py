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
        if this.client.privLevel >= 11:
            text = "<a href='event:openPanel'><img src=''></a>"
            this.client.sendAddPopupText(11001, 785, 24, 70, 50, '0000', '0000', 100, str(text))
