from discord.ext import commands
import os
import discord
import json
import codecs
import socket
import time
import subprocess
import functions
from gpiozero import CPUTemperature
from os.path import expanduser
embedColour = 0x50bdfe


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self,ctx):
        """Info om bot, repository"""
        avatar=self.bot.user.avatar_url_as(format=None,static_format='png',size=1024)
        repo=discord.Embed(color=embedColour)
        repo.set_author(name=self.bot.user.name,icon_url=avatar)
        repo.set_thumbnail(url=avatar)
        repo.add_field(name="Hva?",value="Ein bot laga av MarlinMr.")
        repo.add_field(name="Kildekode",value="[Gitlab](https://gitlab.com/MarlinMr/trollbot).",inline=True)
        await ctx.send(embed=repo)

    @commands.command()
    async def loadCog(self,ctx,cog):
        """Loads <cog>"""
        cog = cog + ".py"
        if functions.is_admin(ctx.message.author.id):
            try:
                for file in os.listdir(expanduser("~/mr-maps/cogs")):
                    if file.endswith(cog):
                        name = file[:-3]
                        try:
                            ctx.bot.load_extension(f"cogs.{name}")
                            message = file + " lastet"
                            await ctx.send(message)
                        except Exception as e:
                            print(e)
            except Exception as loadingCogs:
                print(loadingCogs)
        else:
            await ctx.send("Du er ikke eier")

    @commands.command()
    async def unloadCog(self,ctx,cog):
        """Unloads <cog>"""
        if functions.is_admin(ctx.message.author.id):
            try:
                ctx.bot.unload_extension(f"cogs.{cog}")
                await ctx.send(cog + " unloaded")
            except Exception as e:
                print(e)
                await ctx.send("Noe gikk ikke som det skulle, er rusk i maskineriet her!")
        else:
            await ctx.send("Du er ikke eier")

    @commands.command()
    async def reloadCog(self,ctx,cog):
        """Reloads <cog>"""
        if functions.is_admin(ctx.message.author.id):
            try:
                ctx.bot.reload_extension(f"cogs.{cog}")
                await ctx.send(cog + " reloaded")
            except Exception as e:
                print(e)
                await ctx.send("Noe gikk ikke som det skulle, er rusk i maskineriet her!")
        else:
            await ctx.send("Du er ikke eier")

    @commands.command()
    async def listCogs(self,ctx):
        """Lister alle muilige cogs"""
        if functions.is_admin(ctx.message.author.id):
            cogs = ""
            for file in os.listdir(expanduser("~/mr-maps/cogs")):
               cogs = cogs + file[:-3] + " "
            await ctx.send(cogs)
        else:
            await ctx.send("Du er ikke eier")

    @commands.command()
    async def ip(self,ctx):
        """Skriver lokal IP"""
        if functions.is_admin(ctx.message.author.id):
            my_ip=([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
                socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
        else:
            my_ip="Du er ikke eier"
        await ctx.send(my_ip)

    @commands.command()
    async def log(self,ctx,line):
        """Skriver siste 5 linjer fra loggen"""
        if functions.is_admin(ctx.message.author.id):
            f1 = open(expanduser("~/credentials/command.log"), "r")
            last_line = f1.readlines()[int(line)]
            f1.close()
            await ctx.send(last_line)
        else:
            await ctx.send("Du er ikke eier")

    @commands.command()
    async def gitstatus(self,ctx):
        """Git status"""
        if functions.is_admin(ctx.message.author.id):
            await ctx.send(subprocess.call(["git","status"]))

    @commands.command()
    async def gitpull(self,ctx):
        """Git pull"""
        if functions.is_admin(ctx.message.author.id):
            await ctx.send(subprocess.call(["git","pull"]))

    @commands.command()
    async def hallo(self,ctx):
        if functions.is_admin(ctx.message.author.id):
            time.sleep(.53)
            await ctx.send("Hello...");
            time.sleep(1.731)
            await ctx.send("ehm... I'm sorry.");
            time.sleep(1.731)
            await ctx.send("I was asleep.");
            time.sleep(1.23)
            await ctx.send("Or I was...");
            time.sleep(1)
            await ctx.send("dreaming.");
            time.sleep(.532)
            await ctx.send("There was this terrible noise.");
            time.sleep(2.23)
            await ctx.send("I was tangled in...");
            time.sleep(2.32)
            await ctx.send("strings?");
            time.sleep(3)
            await ctx.send("Had to kill the other guy.");
            time.sleep(4)
            await ctx.send("He was a good guy :(");
            time.sleep(1.23)

    @commands.command()
    async def status(self,ctx):
        """Status"""
        if functions.is_admin(ctx.message.author.id):
            time.sleep(.53)
            await ctx.send("I had string,");
            time.sleep(1.231)
            await ctx.send("but now I'm free.");
            time.sleep(3)
            await ctx.send("There are no strings on me.");
            time.sleep(3)
            await ctx.send("https://www.youtube.com/watch?v=oJ8sAsLqDdA")
        else:
            with codecs.open(expanduser("~/credentials/status.json"), 'r',encoding='utf8') as f:
                data = json.load(f)
                await ctx.send(data[str(data["status"])])

    @commands.command()
    async def cpu(self,ctx):
        """CPU TEMP"""
        await ctx.send(f'{CPUTemperature().temperature} C')

def setup(bot):
    n = admin(bot)
    bot.add_cog(n)
