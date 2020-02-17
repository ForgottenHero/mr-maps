from discord.ext import commands
import discord
import functions
from os.path import expanduser
embedColour = 0x50bdfe
import math
import urllib.request
import io
from PIL import Image
headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            'Accept-Encoding': 'none',
                            'Accept-Language': 'en-US,en;q=0.8',
                            'Connection': 'keep-alive' }
smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

async def ImageCluster(ctx, lat_deg, lon_deg, zoom):
    #lat_deg = float(lat_deg)
    #lon_deg = float(lon_deg)
    zoom=int(zoom)
    delta_long = 0.00421*math.pow(2,19-int(zoom))
    delta_lat = 0.0012*math.pow(2,19-int(zoom))
    lat_deg = float(lat_deg)-(delta_lat/2)
    lon_deg = float(lon_deg)-(delta_long/2)
    await ctx.send(f'Getting map') #for {lat_deg} lat, {lon_deg} log, with a delta of {delta_lat} lat, and {delta_long} log, and with a zoom of {zoom}')
    i=0
    j=0
    xmin, ymax =deg2num(lat_deg, lon_deg, zoom)
    xmax, ymin =deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)
    Cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) )
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin, ymax+1):
            try:
                imgurl=smurl.format(zoom, xtile, ytile)
                imgstr = urllib.request.urlopen(urllib.request.Request(imgurl, None, headers))
                tile = Image.open(io.BytesIO(imgstr.read()))
                Cluster.paste(tile, box=((xtile-xmin)*256 ,  (ytile-ymin)*255))
                i=i+1
            except Exception as e:
                print(e)
        j=j+1
    Cluster.save(expanduser('~/osm/cluster.png'))
    await ctx.send(file=discord.File(expanduser('~/osm/cluster.png')))

class osm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def showMap(self,ctx,*argv):
        """Prints cluster of maptiles"""
        if(len(argv)==3):
            zoom = int(argv[0])
            lat_deg = float(argv[1])
            lon_deg = float(argv[2])
        elif(len(argv)==1):
            zll = argv[0][argv[0].find("map=")+4:]
            zoom=int(zll[:zll.find('/')])
            ll = zll[zll.find('/')+1:]
            lat_deg = float(ll[:ll.find('/')])
            lon_deg = float(ll[ll.find('/')+1:])
            #print(f'{zoom},{lat_deg},{lon_deg}')
        else:
            await ctx.send(f"Either enter the zoom, latitude and longditude, or url, like this: `€showMap 15 60.3912 5.3242`")
            return
        if(zoom>19):
            zoom=19
        await ImageCluster(ctx, lat_deg, lon_deg, zoom)

def setup(bot):
    n = osm(bot)
    bot.add_cog(n)
