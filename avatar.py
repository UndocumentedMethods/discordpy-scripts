# discord.py
import discord
from discord.ext import commands
# typing
import typing

@client.command()
async def avatar(ctx, member: typing.Optional[discord.Member]):
    if member == None:
        member = ctx.author

    formatlar = "[png](https://cdn.discordapp.com/avatars/{str(member.id)}/{member.avatar}.png) | [jpg](https://cdn.discordapp.com/avatars/{str(member.id)}/{member.avatar}.jpg) | [webp](https://cdn.discordapp.com/avatars/{str(member.id)}/{member.avatar}.webp)"

    embed = discord.Embed(title=f"{member.mention} Kişinin Avatarı", description=f"**Bütün Formatlar:**\n\n{formatlar}", color=0xff00ff)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)
