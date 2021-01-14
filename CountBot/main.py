import discord
from discord.ext import commands
import json


def GetDatabaseValue(guild, data):
    with open("./database.json", "r") as f:
        json_data = json.load(f)
        
    guild = str(guild)
    if guild in json_data:
        try:
            return json_data[guild][data]
        except:
            json_data[guild][data] = "none"
            
            with open("./database.json", "w") as f:
                json.dump(json_data, f, indent=4)
                
            return json_data[guild][data]
    else:
        json_data[guild] = {}
        json_data[guild][data] = "none"

        with open("./database.json", "w") as f:
            json.dump(json_data, f, indent=4)
                
        return json_data[guild][data]
    

def SetDatabaseValue(guild, data, value):
    with open("./database.json", "r") as f:
        json_data = json.load(f)
        
    guild = str(guild)
    if guild in json_data:
        json_data[guild][data] = value
    else:
        json_data[guild] = {}
        json_data[guild][data] = value

    with open("./database.json", "w") as f:
        json.dump(json_data, f, indent=4)
                
    return True


with open("./settings.json", "r") as f:
    data = json.load(f)
    token = data["token"]
    prefix = data["prefix"]


client = commands.Bot(command_prefix = prefix, intent=discord.Intents.all())


@client.event
async def on_ready():
    print("Bot Hazır!")
    
@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.channel.id == GetDatabaseValue(message.guild.id, "channel") and GetDatabaseValue(message.guild.id, "started") == True:
        content = message.content
        number = GetDatabaseValue(message.guild.id, "number") + 1
        last_author = GetDatabaseValue(message.guild.id, "author")
        
        if content.startswith("."):
            return
        
        if message.author.id == last_author:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Zaten En Son Sen Yazdın!", delete_after=5)
            return
        
        if not content == str(number):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Lütfen Sırayı Bozmayı Deneme.", delete_after=5)
            return
        
        SetDatabaseValue(message.guild.id, "number", int(content))
        SetDatabaseValue(message.guild.id, "author", message.author.id)
        
        if GetDatabaseValue(message.guild.id, "number") == GetDatabaseValue(message.guild.id, "max-value"):
            SetDatabaseValue(message.guild.id, "started", False)
            await message.channel.send("Oyun Bitti!")
            return
    else:
        await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_guild=True)
async def start(ctx, channel: discord.TextChannel = None, max_value: int = None):
    if GetDatabaseValue(ctx.guild.id, "started") == True:
        return await ctx.send("Zaten Oyun Başlamış!")
    
    if not channel:
        channel = ctx.channel
    
    if not max_value:
        return await ctx.send("Bir Oyun Bitiş Değeri Girmeniz Gerek!")
    
    if max_value > 100000:
        return await ctx.send("Değer 100,000'den Fazla Olamaz!")
    
    if max_value < 10:
        return await ctx.send("Değer 100'den Az Olamaz!")
    
    SetDatabaseValue(ctx.guild.id, "started", True)
    SetDatabaseValue(ctx.guild.id, "channel", channel.id)
    SetDatabaseValue(ctx.guild.id, "max-value", max_value)
    SetDatabaseValue(ctx.guild.id, "number", 0)
    SetDatabaseValue(ctx.guild.id, "author", client.user.id)
    
    await ctx.send(f"Oyun <#{channel.id}> Adlı Kanalda Başladı!")
    

@client.command()
@commands.has_permissions(manage_guild=True)
async def finish(ctx):
    if not GetDatabaseValue(ctx.guild.id, "started") == True:
        return await ctx.send("Oyun Zaten Bitmiş!")
    
    SetDatabaseValue(ctx.guild.id, "started", False)
    await ctx.send("Oyun Bitti.")

client.run(token)