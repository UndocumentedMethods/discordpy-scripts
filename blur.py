# discord.py
import discord
from discord.ext import commands
# pillow
from PIL import Image, ImageFilter
# typing
import typing
# io
from io import BytesIO
# random
from random import randint

@client.command(aliases=["bulanıklaştırma", "bulanıklaştır"])
async def blur(ctx, member: typing.Optional[discord.Member], value: typing.Optional[int]):
    if member == None:
        member = ctx.author

    if value == None:
        value = 3

    avatarurl = member.avatar_url_as(format="png",size=128)
    data = BytesIO(await avatarurl.read())
    profil = Image.open(data)
    profil = profil.resize((128, 128))

    profil_lokasyon = "./blur_{0}_{1}.png".format(randint(1, 100000), member.id)

    profil.filter(ImageFilter.GaussianBlur(value)).save(pfp_conf)
    await ctx.send(f"İşte, Bulanıklaştırılmış Resmin Burada:", file=discord.File(profil_lokasyon))
    os.remove(profil_lokasyon)
