# discord.py
import discord
from discord.ext import commands
# functions.py
from config.bot.functions import *
# classes.py
from config.bot.classes import *
# window.py
from config.visual.window import *
# random
import random

client = commands.AutoShardedBot(command_prefix = GetBotPrefix(), intents = discord.Intents.all(), help_command=None)

@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="WordBot") 
    await client.change_presence(status=discord.Status.idle, activity=activity)
    printc(f">>> Game Setted Up to: {activity.name}", "green")
    printc(f">>> Shards: {client.shards}", "yellow")
    printc(">>> Bot is Ready!", "green")    

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if GetWordGameData(message.guild.id, "started") == "true" and GetWordGameData(message.guild.id, "game-channel") == message.channel.id:
        if message.content.startswith(":") or message.content.startswith("'") or message.content.startswith("//") or message.content.startswith("."):
            return

        typed_word = message.content.lower()

        with open("database\\wordchannels.json", "r") as f:
            all_data_1 = json.load(f)
            json_guild_1 = all_data_1[str(message.guild.id)]
            get_lan = json_guild_1["language"]
            history = json_guild_1["history"]
            words = json_guild_1["last-used"]

        with open("database\\db.json", "r") as r:
            all_words_data = json.load(r)
            all_words = all_words_data[get_lan]

        all_words = list(all_words)
        history = list(history)
        should_end_with = words["word"][-1:]
        cant_play = words["author"]

        if cant_play == message.author.id:
            await message.delete()
            embed = discord.Embed(title="", description=f"{EMOTES.REDOK} {message.author.mention} Son Kelimeyi Zaten Sen Yazdın!", color=COLORS.PASTEL_RED)
            await message.channel.send(embed=embed, delete_after=5)
            return

        if not typed_word.startswith(should_end_with):
            await message.delete()
            embed = discord.Embed(title="", description=f"{EMOTES.REDOK} {message.author.mention} Kelime \"{should_end_with}\" Harfi İle Başlamalı!", color=COLORS.PASTEL_RED)
            await message.channel.send(embed=embed, delete_after=5)
            return

        if not typed_word in all_words:
            await message.delete()
            embed = discord.Embed(title="", description=f"{EMOTES.REDOK} {message.author.mention} Kelime Database İçinde Bulunamadı.", color=COLORS.PASTEL_RED)
            await message.channel.send(embed=embed, delete_after=5)
            return

        if typed_word in history:
            await message.delete()
            embed = discord.Embed(title="", description=f"{EMOTES.REDOK} {message.author.mention} Kelime Önceden Yazıldı!", color=COLORS.PASTEL_RED)
            await message.channel.send(embed=embed, delete_after=5)
            return

        if message.content.endswith("ğ"):
            SetGuildUserPoint(message.guild.id, message.author.id, len(typed_word))
            SetWordGameList(message.guild.id, typed_word)
            SetWordGameListAuthor(message.guild.id, message.author.id)
            SetWordGameHistory(message.guild.id, typed_word)
            await message.add_reaction(EMOTES.NOTIFICATION)

            yeni_kelime = random.choice(all_words)
            while yeni_kelime in history:
                yeni_kelime = random.choice(all_words)

            SetWordGameList(message.guild.id, yeni_kelime)
            SetWordGameListAuthor(message.guild.id, client.user.id)
            SetWordGameHistory(message.guild.id, yeni_kelime)

            embed = discord.Embed(title="", description=f"{EMOTES.BLUEOK} **Bildiri!**\nKelime \"Ğ\" ile Bittiği İçin Yeniden Bir Kelime Seçildi.\n\n**Yeni Kelime**: {yeni_kelime.capitalize()}", color=COLORS.LEET)
            await message.channel.send(embed=embed)
            return

        SetGuildUserPoint(message.guild.id, message.author.id, len(typed_word))
        SetWordGameList(message.guild.id, typed_word)
        SetWordGameListAuthor(message.guild.id, message.author.id)
        SetWordGameHistory(message.guild.id, typed_word)
        await message.add_reaction(EMOTES.NOTIFICATION)
    else:
        await client.process_commands(message)

        
@client.event
async def on_guild_channel_delete(channel):
    if channel.id == GetWordGameData(channel.guild.id, "game-channel"):
        SetWordGameData(channel.guild.id, "started", "unknown")

        with open("database\\wordchannels.json", "r") as f:
            all_data = json.load(f)
            json_guild = all_data[str(channel.guild.id)]

        del json_guild["history"]
        del json_guild["language"]
        del json_guild["last-used"]

        with open("database\\wordchannels.json", "w") as f:
            json.dump(all_data, f, indent=4)