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
# regex
import re

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_guild = True)
async def settings(ctx, setting: typing.Optional[str], value = None):
    if not GetSettingsValue(ctx.guild.id, "enabled") == True:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Ayarları Yapmadan Önce Captcha Sistemini Açın!`", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return

    if not setting:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Doğru Bir Ayar Giriniz.\n\n**Liste:** `length`, `forecolor`, `bordercolor`, `rights`", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return


    settings_list = [
        "length",
        "forecolor",
        "bordercolor",
        "rights"
    ]

    setting = setting.lower()

    if not setting in settings_list:
        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Doğru Bir Ayar Giriniz.\n\n**Liste:** `length`, `forecolor`, `bordercolor`, `rights`", color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
        return

    if setting == settings_list[0]: # length
        if value == None:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Doğru Bir Değer Giriniz.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        value = int(value)

        if value < 3:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__eğer En Az 3 Olabilir.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        if value > 8:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__eğer En Fazla 8 Olabilir.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        SetSettingsValue(ctx.guild.id, "length", value)
        embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __B__aşarıyla Uzunluk `{value}` Olarak Ayarlandı!", color=COLORS.PASTEL_GREEN)
        await ctx.send(embed=embed)
        return

    if setting == settings_list[1]: # forecolor
        if value == None:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Doğru Bir Değer Giriniz.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        check_value = re.search("^#(?:[0-9a-fA-F]{1,2}){3}$", value)

        if not check_value:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__eğer Hex Türünde Olmalı.\n\n**Örnek**: `#7289da`", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        SetSettingsValue(ctx.guild.id, "forecolor", value)
        embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __B__aşarıyla Renk `{value}` Olarak Ayarlandı!", color=COLORS.PASTEL_GREEN)
        await ctx.send(embed=embed)
        return

    if setting == settings_list[2]: # bordercolor
        if value == None:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Doğru Bir Değer Giriniz.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        check_value = re.search("^#(?:[0-9a-fA-F]{1,2}){3}$", value)

        if not check_value:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__eğer Hex Türünde Olmalı.\n\n**Örnek**: `#7289da`", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        SetSettingsValue(ctx.guild.id, "bordercolor", value)
        embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __B__aşarıyla Yan Renk `{value}` Olarak Ayarlandı!", color=COLORS.PASTEL_GREEN)
        await ctx.send(embed=embed)
        return

    if setting == settings_list[3]: # rights
        if value == None:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __L__ütfen Doğru Bir Değer Giriniz.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        value = int(value)

        if value < 1:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__eğer En Az 1 Olabilir.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        if value > 5:
            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__eğer En Fazla 5 Olabilir.", color=COLORS.PASTEL_RED)
            await ctx.send(embed=embed, delete_after=5)
            return

        SetSettingsValue(ctx.guild.id, "rights", value)
        embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __B__aşarıyla Deneme Hakkı Sayısı `{value}` Olarak Ayarlandı!", color=COLORS.PASTEL_GREEN)
        await ctx.send(embed=embed)
        return



@settings.error
async def settings_error(ctx, error):
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