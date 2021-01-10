# discord.py
import discord
from discord.ext import commands
# functions.py
from config.bot.functions import *
# classes.py
from config.bot.classes import *
# window.py
from config.visual.window import *
# random
import random
# string
import string
# asyncio
import asyncio

client = commands.AutoShardedBot(command_prefix = GetBotPrefix(), intents = discord.Intents.all())

@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="Captcha") 
    await client.change_presence(status=discord.Status.idle, activity=activity)
    printc(f">>> Game Setted Up to: {activity.name}", "green")
    printc(f">>> Shards: {client.shards}", "yellow")
    printc(">>> Bot is Ready!", "green")

@client.event
async def on_guild_channel_delete(channel):
    if GetSettingsValue(channel.guild.id, "logging") == channel.id:
        SetSettingsValue(channel.guild.id, "logging", "unknown")

@client.event
async def on_member_join(member):
    if GetSettingsValue(member.guild.id, "enabled"):
        if not GetSettingsValue(member.guild.id, "logging") == "unknown":
            log_channel = client.get_channel(GetSettingsValue(member.guild.id, "logging"))
            embed = discord.Embed(title="", description=f"{EMOTES.NOTIFICATION} **Yeni Birisi Geldi! Captcha Uygulanıyor...**\n> **Gelen**: {member.mention}",  color=COLORS.PASTEL_PURPLE)
            await log_channel.send(embed=embed)

        if GetSettingsValue(member.guild.id, "rights") == "unknown":
            deneme_hakki = 3
        else:
            deneme_hakki = GetSettingsValue(member.guild.id, "rights")

        if GetSettingsValue(member.guild.id, "forecolor") == "unknown":
            on_renk = "#7289da"
        else:
            on_renk = GetSettingsValue(member.guild.id, "forecolor")

        on_renk = on_renk.split("#")[1]

        if GetSettingsValue(member.guild.id, "bordercolor") == "unknown":
            yan_renk = "#000000"
        else:
            yan_renk = GetSettingsValue(member.guild.id, "bordercolor")

        yan_renk = yan_renk.split("#")[1]

        if GetSettingsValue(member.guild.id, "length") == "unknown":
            uzunluk = 4
        else:
            uzunluk = GetSettingsValue(member.guild.id, "length")

        kalan_deneme_hakki = deneme_hakki

        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        captcha = "".join(random.sample(chars, uzunluk))

        url = "http://chart.apis.google.com/chart?chst=d_text_outline&chld={0}|128|h|{1}|_|{2}".format(on_renk, yan_renk, captcha)

        try:
            embed = discord.Embed(title="Doğrulama", description=f"Bu Sunucuda Captcha Bulunuyor! Sunucuya Giriş Yapmak İçin Aşağıdaki Kodu Buraya Yaz.\n\n> **Kalan Deneme Hakkın**: {kalan_deneme_hakki}", color=COLORS.MUTED)
            embed.set_image(url=url)
            await member.send(embed=embed)
        except:
            if not GetSettingsValue(member.guild.id, "logging") == "unknown":
                log_channel = client.get_channel(GetSettingsValue(member.guild.id, "logging"))
                embed = discord.Embed(title="", description=f"{EMOTES.ERROR} {member.mention} Adlı Kişinin __Ö__zel Mesajları Kapalı. Bu Yüzden Doğrulama Yapamıyorum.",  color=COLORS.PASTEL_RED)
                await log_channel.send(embed=embed)

            return

        for deneme in range(deneme_hakki):
            try: 
                def dogrula(m):
                    return m.author == member

                yazmayi_bekle = await client.wait_for('message', check=dogrula, timeout=300.0)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__oğrulama Zaman Aşımına Uğradığı İçin Kapatıldı. Lütfen Sunucuya Gir-Çık Yaparak Tekrar Deneyin.",  color=COLORS.PASTEL_RED)

                try:
                    await member.send(embed=embed)
                except:
                    pass

                if not GetSettingsValue(member.guild.id, "logging") == "unknown":
                    log_channel = client.get_channel(GetSettingsValue(member.guild.id, "logging"))
                    embed = discord.Embed(title="", description=f"{EMOTES.ERROR} {member.mention} Adlı Kişi __D__oğrulama Süresini Doldurdu.",  color=COLORS.PASTEL_RED)
                    await log_channel.send(embed=embed)

                return
            else:
                if yazmayi_bekle.content == captcha:
                    embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} __D__oğrulama Başarılı, Sunucuya Hoşgeldiniz!",  color=COLORS.PASTEL_GREEN)

                    try:
                        await member.send(embed=embed)
                    except:
                        pass

                    if not GetSettingsValue(member.guild.id, "logging") == "unknown":
                        log_channel = client.get_channel(GetSettingsValue(member.guild.id, "logging"))
                        embed = discord.Embed(title="", description=f"{EMOTES.SUCCESS} {member.mention} Adlı Kişi Başarıyla Doğrulandı!",  color=COLORS.PASTEL_GREEN)
                        await log_channel.send(embed=embed)
                
                    captcha_role = discord.utils.get(member.guild.roles, id=GetSettingsValue(member.guild.id, "role"))
                    await member.add_roles(captcha_role)
                    return

                else:
                    kalan_deneme_hakki -= 1

                    if kalan_deneme_hakki == 0:
                        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __B__ütün Haklarınızı Bitirdiniz. Lütfen Sunucudan Çıkıp-Girerek Tekrar Deneyin.",  color=COLORS.PASTEL_RED)

                        try:
                            await member.send(embed=embed)
                        except:
                            pass

                        if not GetSettingsValue(member.guild.id, "logging") == "unknown":
                            log_channel = client.get_channel(GetSettingsValue(member.guild.id, "logging"))
                            embed = discord.Embed(title="", description=f"{EMOTES.ERROR} {member.mention} Adlı Kişinin __T__üm Hakları Doldu.",  color=COLORS.PASTEL_RED)
                            await log_channel.send(embed=embed)

                        return

                    embed = discord.Embed(title="", description=f"{EMOTES.ERROR} __D__oğrulama Başarısız Oldu. Kalan Hakkınız: {kalan_deneme_hakki}",  color=COLORS.PASTEL_RED)
                    try:
                        await member.send(embed=embed)
                    except:
                        pass

                    if not GetSettingsValue(member.guild.id, "logging") == "unknown":
                        log_channel = client.get_channel(GetSettingsValue(member.guild.id, "logging"))
                        embed = discord.Embed(title="", description=f"{EMOTES.ERROR} {member.mention} Adlı Kişi Doğrulamada Başarısız Oldu.\n\n> **Kalan Deneme Hakkı**: {kalan_deneme_hakki}\n > **Yazması Gereken**: {captcha}\n > **Yazdığı**: {yazmayi_bekle.content}",  color=COLORS.PASTEL_RED)
                        await log_channel.send(embed=embed)

                    continue