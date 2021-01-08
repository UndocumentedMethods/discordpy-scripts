# discord.py
import discord
from discord.ext import commands
# events.py
from config.bot.events import *
# fucntions.py
from config.bot.functions import *
# classes.py
from config.bot.classes import *
# typing
import typing
# random
import random

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild = True)
async def start(ctx, channel: typing.Optional[discord.TextChannel], language: typing.Optional[str]):
    if channel == None:
        channel = ctx.channel

    langs = [
        "turkish",
        "english"
    ]

    if language == None:
        language = "turkish"

    language = language.lower()

    if not language in langs:
        embed = discord.Embed(title="", description=f"{EMOTES.REDOK} Lütfen Geçerli Bir Dil Giriniz.\n\n**Diller**: `turkish`, `english`", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=10)
        return

    if not GetWordGameData(ctx.guild.id, "started") == "unknown":
        embed = discord.Embed(title="", description=f"{EMOTES.REDOK} Görünüşe Göre Bu Sunucuda Zaten <#{GetWordGameData(ctx.guild.id, 'game-channel')}> Adlı Kanala Ayarlamışsın.", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=10)
        return

    SetWordGameData(ctx.guild.id, "started", "true")
    SetWordGameData(ctx.guild.id, "game-channel", channel.id)
    SetWordGameData(ctx.guild.id, "language", language)

    with open("database\\db.json", "r") as r:
        all_words_data__ = json.load(r)
        words = all_words_data__[language]

    words = list(words)
    random_word = random.choice(words)

    if random_word[-1:] == "ğ":
        random_word = "araba"

    SetWordGameList(ctx.guild.id, random_word)
    SetWordGameListAuthor(ctx.guild.id, client.user.id)
    SetWordGameHistory(ctx.guild.id, random_word)

    language = language.capitalize()

    embed = discord.Embed(title="", description=f"{EMOTES.BLUEOK} **Oyun Başladı!**\n\n**`Detaylar`**:\n**Dil**: {language}\n**Kelime**: {random_word.capitalize()}", color=COLORS.LEET)
    await channel.send(embed=embed)


@start.error
async def start_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.REDOK + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingPermissions):
        desc = EMOTES.REDOK + " Bu Komutu Kullanmak İçin `SUNUCUYU_YÖNET` Yetkilerine Sahip Olmalısın!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.BadArgument):
        desc = EMOTES.REDOK + " Hatalı Argüman(lar)!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error


##############################################################################################################################################


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild = True)
async def finish(ctx):
    if GetWordGameData(ctx.guild.id, "started") == "unknown":
        embed = discord.Embed(title="", description=f"{EMOTES.REDOK} Görünüşe Göre Bu Sunucuda Oyun Başlamamış", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=10)
        return

    SetWordGameData(ctx.guild.id, "started", "unknown")

    with open("database\\wordchannels.json", "r") as f:
        all_data = json.load(f)
        j_guild_d = all_data[str(ctx.guild.id)]
        words = j_guild_d["history"]
        lan_dil = j_guild_d["language"]

    lan_dil = lan_dil.capitalize()
    words = list(words)
    words_len = len(words)

    del j_guild_d["history"]
    del j_guild_d["language"]
    del j_guild_d["last-used"]

    with open("database\\wordchannels.json", "w") as f:
        json.dump(all_data, f, indent=4)

    embed = discord.Embed(title="", description=f"{EMOTES.BLUEOK} **Oyun Bitti!**\n\n**`Detaylar`**:\n**Dil**: {lan_dil}\n**Toplam Kelimeler**: {words_len}", color=COLORS.LEET)
    await ctx.send(embed=embed)


@finish.error
async def finish_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.REDOK + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingPermissions):
        desc = EMOTES.REDOK + " Bu Komutu Kullanmak İçin `SUNUCUYU_YÖNET` Yetkilerine Sahip Olmalısın!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.BadArgument):
        desc = EMOTES.REDOK + " Hatalı Argüman(lar)!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error