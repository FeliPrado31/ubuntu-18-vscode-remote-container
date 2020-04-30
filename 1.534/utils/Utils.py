# coding: utf-8
import re, time, random, string, time as thetime

# Library
from datetime import datetime

class Utils:

    @staticmethod
    def getTFMLangues(langueID):
        return {0:"ES", 1:"ES", 2:"ES", 3:"ES", 4:"ES", 5:"ES", 6:"ES", 7:"ES", 8:"ES", 9:"ES", 10:"ES", 11:"ES", 12:"ES", 13:"ES", 14:"ES", 15:"ES", 16:"ES", 17:"ES", 18:"ES", 19:"ES", 20:"ES", 21:"ES", 22:"ES", 23:"ES", 24:"ES", 25:"ES", 26:"ES", 27:"ES", 29:"ES", 30:"ES", 31:"ES"}[langueID]

    @staticmethod
    def getLangues():
        return {0:"ES", 1:"ES", 2:"ES", 3:"ES", 4:"ES", 5:"ES", 6:"ES", 7:"ES", 8:"ES", 9:"ES", 10:"ES", 11:"ES", 12:"ES", 13:"ES", 14:"ES", 15:"ES", 16:"ES", 17:"ES", 18:"ES", 19:"ES", 20:"ES", 21:"ES", 22:"ES", 23:"ES", 24:"ES", 25:"ES", 26:"ES", 27:"ES", 29:"ES", 30:"ES", 31:"ES"}[langueID]

    @staticmethod
    def getTime():
        return int(long(str(time.time())[:10]))

    @staticmethod
    def getValue(*array):
        return random.choice(array)

    @staticmethod
    def getDate():
        return str(datetime.now()).replace("-", "/").split(".")[0].replace(" ", " - ")

    @staticmethod
    def getHoursDiff(endTimeMillis):
        startTime = Utils.getTime()
        startTime = datetime.fromtimestamp(float(startTime))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        seconds = (result.microseconds + (result.seconds + result.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)
        hours = int(int(seconds) / 3600) + 1
        return hours
    
    @staticmethod
    def getDiffDays(time):
        diff = time - Utils.getTime()
        return diff / (24 * 60 * 60)

    @staticmethod
    def getSecondsDiff(endTimeMillis):
        return int(long(str(thetime.time())[:10]) - endTimeMillis)

    @staticmethod
    def getRandomChars(size):
        return "".join(random.choice(string.digits + string.ascii_uppercase + string.ascii_lowercase) for x in range(size))

    @staticmethod
    def getDaysDiff(endTimeMillis):
        startTime = datetime.fromtimestamp(float(Utils.getTime()))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        return result.days + 1

    @staticmethod
    def parsePlayerName(playerName):
        return (playerName[0] + playerName[1:].lower().capitalize()) if playerName.startswith("*") or playerName.startswith("+") else playerName.lower().capitalize()

    @staticmethod
    def joinWithQuotes(list):
        return "\"" + "\", \"".join(list) + "\""

    @staticmethod
    def getYoutubeID(url):
        matcher = re.compile(".*(?:youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=)([^#\\&\\?]*).*").match(url)
        return matcher.group(1) if matcher else None

    @staticmethod
    def Duration(duration):
        time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
        for key, count in time.items():
            time[key] = 0 if count is None else time[key]
        return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)

    @staticmethod
    def getUptime(time):
        text = ""
        time = str(time).split(".")[0].split(":")
        hours = time[0]
        minutes = time[1]
        seconds = time[2]

        minutes = minutes.replace("00", "0") if minutes == "00" else minutes.replace("0", "") if len("0") == 1 and not minutes in ["10", "20", "30", "40", "50", "60"] else minutes
        seconds = seconds.replace("00", "0") if seconds == "00" else seconds.replace("0", "") if len("0") == 1 and not seconds in ["10", "20", "30", "40", "50", "60"] else seconds
        if hours > "0": text += hours + (" hours " if hours > "1" else " hour ")
        if minutes > "0": text += minutes + (" minutes " if minutes > "1" else " minute ")
        if seconds > "0": text += seconds + (" seconds " if seconds > "1" else " second ")
        return text
