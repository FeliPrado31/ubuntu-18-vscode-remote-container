# coding: utf-8
import time as thetime, random, time, re, xml.etree.ElementTree as xml, xml.parsers.expat

from datetime import datetime

class TFMUtils:
    @staticmethod
    def getTFMLangues(langueID):
        if langueID == 0:
            return ["EN"]
        elif langueID == 1:
            return ["FR"]
        elif langueID == 2:
            return ["FR"]
        elif langueID == 3:
            return ["BR"]
        elif langueID == 4:
            return ["ES"]
        elif langueID == 5:
            return ["CN"]
        elif langueID == 6:
            return ["TR"]
        elif langueID == 7:
            return ["VK"]
        elif langueID == 8:
            return ["PL"]
        elif langueID == 9:
            return ["HU"]
        elif langueID == 10:
            return ["NL"]
        elif langueID == 11:
            return ["RO"]
        elif langueID == 12:
            return ["ID"]
        elif langueID == 13:
            return ["DE"]
        elif langueID == 14:
            return ["E2"]
        elif langueID == 15:
            return ["AR"]
        elif langueID == 16:
            return ["PH"]
        elif langueID == 17:
            return ["LT"]
        elif langueID == 18:
            return ["JP"]
        elif langueID == 19:
            return ["CH"]
        elif langueID == 20:
            return ["FI"]
        elif langueID == 21:
            return ["CZ"]
        elif langueID == 22:
            return ["SK"]
        elif langueID == 23:
            return ["HR"]
        elif langueID == 24:
            return ["BU"]
        elif langueID == 25:
            return ["LV"]
        elif langueID == 26:
            return ["HE"]
        elif langueID == 27:
            return ["IT"]
        elif langueID == 29:
            return ["ET"]
        elif langueID == 30:
            return ["AZ"]
        elif langueID == 31:
            return ["PT"]
        else:
            return ["EN"]

    @staticmethod
    def getTime():
        return int(long(str(time.time())[:10]))

    @staticmethod
    def checkValidXML(XML):
        if re.search("ENTITY", XML) and re.search("<html>", XML):
            return False
        else:
            try:
                parser = xml.parsers.expat.ParserCreate()
                parser.Parse(XML)
                return True
            except Exception, e:
                return False

    @staticmethod
    def getHoursDiff(endTimeMillis):
        startTime = TFMUtils.getTime()
        startTime = datetime.fromtimestamp(float(startTime))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        seconds = (result.microseconds + (result.seconds + result.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)
        hours = int(int(seconds) / 3600) + 1
        return hours

    @staticmethod
    def getSecondsDiff(endTimeMillis):
        return int(long(str(thetime.time())[:10]) - endTimeMillis)

    @staticmethod
    def getRandomChars(size):
        return "".join((random.choice("ABCDEF123456789") for x in range(size)))

    @staticmethod
    def calculateTime(time):
        diff = int(time) - TFMUtils.getTime()
        diffSeconds = diff / 1000 % 60
        diffMinutes = diff / (60 * 1000) % 60
        diffHours = diff / (60 * 60 * 1000) % 24
        diffDays = diff / (24 * 60 * 60 * 1000)
        return diffDays <= 0 and diffHours <= 0 and diffMinutes <= 0 and diffSeconds <= 0

    @staticmethod
    def getDiffDays(time):
        return time - TFMUtils.getTime() / (24 * 60 * 60)

    @staticmethod
    def parsePlayerName(playerName):
        return (playerName[0] + playerName[1:].lower().capitalize()) if playerName.startswith("*") or playerName.startswith("+") else playerName.lower().capitalize()

    @staticmethod
    def joinWithQuotes(list):
        return "\"" + "\", \"".join(list) + "\""

    @staticmethod
    def getValue(*array):
        return random.choice(array)

    @staticmethod
    def getYoutubeID(url):
        matcher = re.compile(".*(?:youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=)([^#\\&\\?]*).*").match(url)
        return matcher.group(1) if matcher else None

    @staticmethod
    def Duration(duration):
        time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
        for key in time.items():
            time[key[0]] = 0 if key[1] is None else time[key[0]]
        return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)
