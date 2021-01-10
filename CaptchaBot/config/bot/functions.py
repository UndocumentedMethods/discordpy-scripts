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

def DumpData(data):
    with open("database\\guildsettings.json", "w") as f:
        json.dump(data, f, indent=4)
###########################################################################################

# CAPTCHA FUNCTIONS:
###########################################################################################
def LoadJSON():
    with open("database\\guildsettings.json", "r") as f:
        settings = json.load(f)

    return settings


def SetSettingsValue(guild, setting, value):
    settings = LoadJSON()
    guild = str(guild)

    if guild in settings:
        settings[guild][setting] = value
    else:
        settings[guild] = {}
        settings[guild][setting] = value

    with open("database\\guildsettings.json", "w") as f:
        json.dump(settings, f, indent=4)


def GetSettingsValue(guild, setting):
    settings = LoadJSON()
    guild = str(guild)

    if guild in settings:
        try:
            return settings[guild][setting]
        except:
            settings[guild][setting] = "unknown"
            DumpData(settings)
            return settings[guild][setting]
    else:
        settings[guild] = {}
        settings[guild][setting] = "unknown"
        DumpData(settings)
        return settings[guild][setting]

###########################################################################################