# discord.py
import discord
from discord.ext import commands
# for hours
from itertools import product
# typing
import typing

@client.command()
@commands.has_permissions(manage_channels = True)
async def slowmode(ctx, channel: typing.Optional[discord.TextChannel], amount: typing.Optional[int]):
    if amount == None:
        amount = 1

    if amount > 21600:
        embed = discord.Embed(title="", description=f":x: Slowmode Komutu İçin Maksimum Sayı `21600`.", color=0xff0000)
        await ctx.send(embed=embed, delete_after=5)
        return

    if amount < 0:
        embed = discord.Embed(title="", description=f":x: Sayı Pozitif Yönde Olmalıdır.", color=0xff0000)
        await ctx.send(embed=embed, delete_after=5)
        return

    if channel == None:
        channel = ctx.channel

    hhmmss = []
    for (h, m, s) in product(range(24), range(60), range(60)):
        hhmmss.append("%02d Saat, %02d Dakika, %02d Saniye" % (h, m, s))

    try:
        await channel.edit(slowmode_delay=amount)
        if amount == 0:
            embed = discord.Embed(title="", description=f":white_check_mark: <#{channel.id}> Kanalında Slowmode Artık **Kapatıldı**!", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=f":white_check_mark: <#{channel.id}> Kanalında Slowmode Artık `{hhmmss[amount]}` Olarak Ayarlandı!", color=0x00ff00)
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="", description=f":x: Kanalda Yavaşlama Modunu Ayarlamak İçin Gereken Yetkiye Sahip Değilim.", color=0xff0000)
        await ctx.send(embed=embed, delete_after=5)

@slowmode.error
async def slowmode_error(ctx, error):
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="", description=":x: Bu Komutu Kullanabilmek İçin `KANALLARI_YÖNET` Yetkisine Sahip Olman Gerek.", color=0xff0000)
        await ctx.send(embed=embed, delete_after=5)
