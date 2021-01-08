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
async def point(ctx, member: typing.Optional[discord.Member]):
    if member == None:
        member = ctx.author

    member_point = GetGuildUserPoint(ctx.guild.id, member.id)
    member_mention = member.mention

    embed = discord.Embed(title="", description=f"{EMOTES.BLUEOK} **İşte Veri Geldi!**\n\n**`Detaylar`**:\n**Kullanıcı**: {member_mention}\n**Puanı**: {member_point}", color=COLORS.LEET)
    embed.set_footer(text=f"Komutu Kullanan: {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)


@point.error
async def point_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.REDOK + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.BadArgument):
        desc = EMOTES.REDOK + " Hatalı Argüman(lar)!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error


##############################################################################################################################################

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def leaderboard(ctx):
    with open("database\\points.json", "r") as f:
        json_data____ = json.load(f)
        guild_data = json_data____[str(ctx.guild.id)]

    guild_point_listed = []

    for users in guild_data:
        guild_point_listed.append(guild_data[users]["point"])

    guild_point_listed = sorted(guild_point_listed, reverse=True)

    guild_member_listed = []
    index_data = 0
    for points in guild_point_listed:
        for users in guild_data:
            if guild_data[users]["point"] == points:
                guild_member_listed.append(guild_data[users]["user"])
                index_data += 1
            else:
                continue

    desc = ""
    index = 0
    for indexed in guild_point_listed:
        user_name = client.get_user(int(guild_member_listed[index])).mention

        desc += "**{0}.** {1} | **Puan:** {2}\n".format(index + 1, user_name, guild_point_listed[index])
        index += 1

        if index == 9:
            break

    embed = discord.Embed(title="", description=f"{EMOTES.BLUEOK} **{ctx.guild}** Sunucusu İçin Leaderboard!\n\n{desc}", color=COLORS.LEET)
    embed.set_footer(text=f"Komutu Kullanan: {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)


@leaderboard.error
async def leaderboard_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        desc = EMOTES.REDOK + " Bu Komut **Yavaşlama** Modunda, Lütfen `{:.2f}` Saniye Sonra Deneyin.".format(error.retry_after)
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=error.retry_after)
    elif isinstance(error, commands.BadArgument):
        desc = EMOTES.REDOK + " Hatalı Argüman(lar)!"
        embed = discord.Embed(title="", description=desc, color=COLORS.PASTEL_RED)
        await ctx.send(embed=embed, delete_after=5)
    else:
        raise error