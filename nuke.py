# discord.py
import discord
from discord.ext import commands
# typing
import typing
# asyncio
import asyncio

@client.command()
@commands.has_permissions(manage_channels = True)
async def nuke(ctx, channel: typing.Optional[discord.TextChannel]):
    if channel == None:
        channel = ctx.channel

    embed = discord.Embed(title="", description=f":eyes: <#{channel.id}> Adlı Kanalı Sıfırlamak İstediğine Emin misin? Eğer Eminsen 💯 Tepkisine Bas!\n\nEğer İptal Etmek İstiyorsan Sadece 10 Saniye Bekle. Otomatik İptal Olucaktır.", color=0xffffff)
    nuke_check_msg = await ctx.send(embed=embed)
    await nuke_check_msg.add_reaction("💯")

    def collectorDogrula(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "💯"

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=collectorDogrula)
    except asyncio.TimeoutError:
        await nuke_check_msg.delete()
        embed = discord.Embed(title="", description=f":x: İşlem İptal Edildi.", color=0xff0000)
        await ctx.send(embed=embed, delete_after=5)
        return
    else:
        await nuke_check_msg.delete()

        channel_position = channel.position
        nuked_channel = await channel.clone()
        await channel.delete()
        await nuked_channel.edit(position=channel_position)

        nuked_embed = discord.Embed(title="", description=f"💯 Kanal Başarıyla Sıfırlandı!", color=0x00ff00)
        await nuked_channel.send(embed=nuked_embed)
