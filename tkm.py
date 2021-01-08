# discord.py
import discord
from discord.ext import commands
# random
import random

@client.command(aliases=["tkm"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def rsp(ctx, *, tkm="Taş"):
    secenekler = ["Taş", "Kağıt", "Makas"]

    if not tkm.capitalize() in secenekler:
        embed = discord.Embed(title="", description=f":x: Lütfen `Taş`, `Kağıt` veya `Makas` Arasından Birini Seçiniz.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    bot_secimi = random.choice(secenekler)
    durum_message = "\n\n**`Detaylar`**:\n**Bot**: {0} \n**{1}**: {2}".format(bot_secimi.lower(), str(ctx.author), str(tkm.lower()))

    if bot_secimi.lower() == "taş":
        if tkm.lower() == "taş":
            embed = discord.Embed(title="", description=f"**Durum**: Beraberlik.{durum_message}", color=0x000000)
            await ctx.send(embed=embed)
        elif tkm.lower() == "kağıt":
            embed = discord.Embed(title="", description=f"**Durum**: Kazandın!{durum_message}", color=0x00ff00)
            await ctx.send(embed=embed)
        elif tkm.lower() == "makas":
            embed = discord.Embed(title="", description=f"**Durum**: Kaybettin.{durum_message}", color=0xff0000)
            await ctx.send(embed=embed)
    elif bot_secimi.lower() == "kağıt":
        if tkm.lower() == "taş":
            embed = discord.Embed(title="", description=f"**Durum**: Kaybettin.{durum_message}", color=0xff0000)
            await ctx.send(embed=embed)
        elif "kağıt":
            embed = discord.Embed(title="", description=f"**Durum**: Beraberlik.{durum_message}", color=0x000000)
            await ctx.send(embed=embed)
        elif "makas":
            embed = discord.Embed(title="", description=f"**Durum**: Kazandın!{durum_message}", color=0x00ff00)
            await ctx.send(embed=embed)
    elif bot_secimi.lower() == "makas":
        if tkm.lower() == "taş":
            embed = discord.Embed(title="", description=f"**Durum**: Kazandın!{durum_message}", color=0x00ff00)
            await ctx.send(embed=embed)
        elif tkm.lower() == "kağıt":
            embed = discord.Embed(title="", description=f"**Durum**: Kaybettin.{durum_message}", color=0xff0000)
            await ctx.send(embed=embed)
        elif tkm.lower() == "makas":
            embed = discord.Embed(title="", description=f"**Durum**: Beraberlik.{durum_message}", color=0x000000)
            await ctx.send(embed=embed)
