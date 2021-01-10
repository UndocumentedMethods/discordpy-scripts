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

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild = True)
async def log(ctx, channel: typing.Optional[discord.TextChannel]):
    if not GetSettingsValue(ctx.guild.id, "enabled") == True:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Log Ayarlamadan Önce Captcha Sistemini Açın!", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return 
    
    if not channel:
        channel = ctx.channel

    SetSettingsValue(ctx.guild.id, "logging", channel.id)
    embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __B__aşarıyla Log Kanalı <#{channel.id}> Olarak Ayarlandı!", color=COLORS.PASTEL_GREEN)
    await ctx.send(embed=embed)


@log.error
async def log_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.ERROR + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingPermissions):
        desc = EMOTES.ERROR + " Bu Komutu Kullanmak İçin `SUNUCUYU_YÖNET` Yetkilerine Sahip Olmalısın!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.BadArgument):
        desc = EMOTES.ERROR + " Hatalı Argüman(lar)!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error

#####################################################################################################################################################################

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild = True)
async def logoff(ctx):
    if GetSettingsValue(ctx.guild.id, "logging") == "unknown":
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ogging Zaten Kapatılmış Durumda.", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return 

    if not GetSettingsValue(ctx.guild.id, "enabled") == True:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Log Kapatmadan Önce Captcha Sistemini Açın!", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return 

    SetSettingsValue(ctx.guild.id, "logging", "unknown")
    embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __B__aşarıyla Logging Kapatıldı!", color=COLORS.PASTEL_GREEN)
    await ctx.send(embed=embed)


@logoff.error
async def logoff_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.ERROR + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingPermissions):
        desc = EMOTES.ERROR + " Bu Komutu Kullanmak İçin `SUNUCUYU_YÖNET` Yetkilerine Sahip Olmalısın!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.BadArgument):
        desc = EMOTES.ERROR + " Hatalı Argüman(lar)!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error