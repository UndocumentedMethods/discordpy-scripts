# discord.py
import discord
from discord.ext import commands
# events.py
from config.bot.events import *
# fucntions.py
from config.bot.functions import *
# classes.py
from config.bot.classes import *

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild = True)
async def enable(ctx, role: discord.Role = None):
    if not role:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __C__aptcha İçin Lütfen Bir Rol Belirleyin.", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return

    id = ctx.guild.id

    if GetSettingsValue(id, "enabled") == True:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __C__aptcha Zaten Açık!", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return

    SetSettingsValue(id, "enabled", True)
    SetSettingsValue(id, "role", role.id)
    embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __C__aptcha Başarıyla Açıldı!", color=COLORS.PASTEL_GREEN)
    await ctx.send(embed=embed)


@enable.error
async def enable_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.ERROR + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingPermissions):
        desc = EMOTES.ERROR + " Bu Komutu Kullanmak İçin `SUNUCUYU_YÖNET` Yetkilerine Sahip Olmalısın!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error

###############################################################################################################################################################

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild = True)
async def disable(ctx):
    id = ctx.guild.id

    if not GetSettingsValue(id, "enabled") == True:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __C__aptcha Zaten Kapalı!", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return

    SetSettingsValue(id, "enabled", False)
    embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __C__aptcha Başarıyla Kapatıldı!", color=COLORS.PASTEL_GREEN)
    await ctx.send(embed=embed)


@disable.error
async def disable_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.ERROR + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingPermissions):
        desc = EMOTES.ERROR + " Bu Komutu Kullanmak İçin `SUNUCUYU_YÖNET` Yetkilerine Sahip Olmalısın!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error