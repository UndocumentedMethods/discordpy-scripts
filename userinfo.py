# discord.py
import discord
from discord.ext import commands
# typing
import typing

@client.command()
async def userinfo(ctx, member: typing.Optional[discord.Member]):
    if member == None:
        member = ctx.author

    if member.bot:
        kullanıcı_botmu = "Evet"
    else:
        kullanıcı_botmu = "Hayır"

    kullanıcı_id = member.id

    kullanici_rolleri_list = [r.mention for r in member.roles if r != ctx.guild.default_role]
    kullanici_butun_roller_fix = ", ".join(kullanici_rolleri_list)

    kullanici_sunucuya_giris_obj = str(member.joined_at)
    kullanici_bolunmus_sunucuya_giris = kullanici_sunucuya_giris_obj.split(".")
    kullanici_sunucuya_giris = kullanici_bolunmus_sunucuya_giris[0]

    kullanici_hesap_tarihi_obj = str(member.created_at)
    kullanici_bolunmus_hesap_tarihi = kullanici_hesap_tarihi_obj.split(".")
    kullanici_hesap_tarihi = kullanici_bolunmus_hesap_tarihi[0]

    embed = discord.Embed(title=f"{member.mention} Kişinin Detayları", description=f"**Kullanıcı ID:**\n{kullanıcı_id}\n\n**Bot mu?**\n{kullanıcı_botmu}\n\n**Roller ({len(kullanici_rolleri_list)}):**\n{kullanici_butun_roller_fix}\n\n**Sunucuya Giriş Tarihi (ABD):**\n{kullanici_sunucuya_giris}\n\n**Hesap Oluşturma Tarihi (ABD):**\n{kullanici_hesap_tarihi}", color=0xff00ff)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)
