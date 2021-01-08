import json
import os

os.chdir("") # bura config dosyasının lokasyonu
###########################################################################################



# MAIN FUNCTIONS:
###########################################################################################
def GetBotPrefix(): # Prefix
    with open("bot\\settings.json", "r") as f:
        settings = json.load(f)
        prefix = settings["prefix"]

    return prefix

def GetBotToken(): # Secret Token SSHH
    with open("bot\\settings.json", "r") as f:
        settings = json.load(f)
        token = settings["token"]

    return token
###########################################################################################


# GET, SET, RESET GAME SETTINGS:
###########################################################################################
def LoggingJSON():
    with open("database\\wordchannels.json", "r") as f:
        data = json.load(f)

    return data

def GetWordGameData(guild, type):
    data = LoggingJSON()
    guild = str(guild)
    type = str(type)

    if guild in data:
        try:
            return data[guild][type]
        except:
            data[str(guild)][type] = "unknown"
            return data[guild][type]
    else:
        data[str(guild)] = {}
        data[str(guild)][type] = "unknown"

        with open("database\\wordchannels.json", "w") as f:
            json.dump(data, f, indent=4)

        return data[guild][type]

def SetWordGameData(guild, type, channel):
    data = LoggingJSON()
    guild = str(guild)

    if guild in data:
        data[guild][type] = channel
    else:
        data[guild] = {}
        data[guild][type] = channel

    with open("database\\wordchannels.json", "w") as f:
        json.dump(data, f, indent=4)


def GetWordGameList(guild):
    data = LoggingJSON()
    guild = str(guild)

    if guild in data:
        try:
            return data[guild]["last-used"]
        except:
            data[str(guild)]["last-used"] = {}
            return data[guild]["last-used"]
    else:
        data[str(guild)] = {}
        data[str(guild)]["last-used"] = {}

        with open("database\\wordchannels.json", "w") as f:
            json.dump(data, f, indent=4)

        return data[guild]["last-used"]

def SetWordGameList(guild, word):
    data = LoggingJSON()
    guild = str(guild)
    word = str(word)

    if guild in data:
        try:
            data[guild]["last-used"]["word"] = word
        except:
            data[guild]["last-used"] = {}
            data[guild]["last-used"]["word"] = word
    else:
        data[str(guild)] = {}
        data[str(guild)]["last-used"] = {}
        data[guild]["last-used"]["word"] = word

    with open("database\\wordchannels.json", "w") as f:
        json.dump(data, f, indent=4)

def SetWordGameListAuthor(guild, id):
    data = LoggingJSON()
    guild = str(guild)
    id = int(id)

    if guild in data:
        try:
            data[guild]["last-used"]["author"] = id
        except:
            data[guild]["last-used"] = {}
            data[guild]["last-used"]["author"] = id
    else:
        data[str(guild)] = {}
        data[str(guild)]["last-used"] = {}
        data[guild]["last-used"]["author"] = id

    with open("database\\wordchannels.json", "w") as f:
        json.dump(data, f, indent=4)

def SetWordGameHistory(guild, word):
    data = LoggingJSON()
    guild = str(guild)
    word = str(word)

    if guild in data:
        try:
            data[guild]["history"][word] = word
        except:
            data[guild]["history"] = {}
            data[guild]["history"][word] = word
    else:
        data[str(guild)] = {}
        data[str(guild)]["history"] = {}
        data[guild]["history"][word] = word

    with open("database\\wordchannels.json", "w") as f:
        json.dump(data, f, indent=4)
###########################################################################################

# POINT SYSTEM:
###########################################################################################
def PointJSON():
    with open("database\\points.json", "r") as f:
        data = json.load(f)

    return data

def GetGuildUserPoint(guild, id):
    data = PointJSON()
    guild = str(guild)
    id = str(id)

    if guild in data:
        try:
            return data[guild][id]["point"]
        except:
            data[guild][id] = {}
            data[guild][id]["point"] = 0
            return data[guild][id]["point"]
    else:
        data[guild] = {}
        data[guild][id] = {}
        data[guild][id]["point"] = 0

        with open("database\\points.json", "w") as f:
            json.dump(data, f, indent=4)

        return data[guild][id]["point"]

def SetGuildUserPoint(guild, id, point):
    data = PointJSON()
    guild = str(guild)
    id = str(id)

    if guild in data:
        try:
            new_point = data[guild][id]["point"] + point
            data[guild][id]["point"] = new_point
            data[guild][id]["user"] = id
        except:
            data[guild][id] = {}
            data[guild][id]["point"] = point
            data[guild][id]["user"] = id
    else:
        data[guild] = {}
        data[guild][id] = {}
        data[guild][id]["point"] = 0

    with open("database\\points.json", "w") as f:
        json.dump(data, f, indent=4)

def ResetGuildPoints(guild):
    data = PointJSON()
    guild = str(guild)

    if guild in data:
        try:
            del data[guild]
        except:
            return False
    else:
        return False

    with open("database\\points.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return True
###########################################################################################