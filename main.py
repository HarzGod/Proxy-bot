import requests
import discord
from discord import Embed, Option
from discord import File

bot = discord.Bot()
token = ("token")

@bot.event
async def on_ready():
    print("Online.")

@bot.slash_command()
async def proxy(ctx, 
protocol: Option(str, "Proxy Protocol (If you don't choose, auto choose to Http)", choices = ["Http", "Socks4", "Socks5", "ALL"], required=False), 
country: Option(str, "Proxy Country (If you don't choose, auto choose to ALL)", choices = ["ALL", "AR", "CA", "DE", "FR", "HK", "JP", "KR", "RU", "TR", "UA", "US"], required=False), 
timeout: Option(int, "Proxy Timeout (If you don't choose, auto choose to 5000ms)", min_value=1, max_value=10000, required=False), 
):

    if protocol==None:
        protocol="HTTP"

    elif not protocol==None:
        pass

    if timeout==None:
        timeout="5000"
        
    elif not timeout==None:
        pass

    if country==None:
        country="ALL"
    
    elif not timeout==None:
        pass

    proxyinfo = requests.get(f'https://api.proxyscrape.com/v2/?request=proxyinfo&protocol={protocol}').json()
    updated = proxyinfo.get('last_updated', None)
    amount = proxyinfo.get('proxy_count', None)
    embed = Embed(title="proxy scrape proxylist", color=0x3464e0)
    embed.add_field(name="Proxy type", value=f"{protocol}")
    embed.add_field(name="Proxy country", value=f"{country}")
    embed.add_field(name="Proxy timeout", value=f"{timeout}")
    embed.add_field(name="Proxy amount", value=f"{amount}")
    embed.add_field(name="Proxy last updated", value=f"{updated}")
    await ctx.respond(embed=embed)

    f = open("Data/proxies.txt", "a+")
    f.truncate(0)
    r = requests.get(f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout={timeout}&country={country}&ssl=all&anonymity=all')
    proxies = []
    for proxy in r.text.split('\n'):
        proxy = proxy.strip()
        if proxy:
            proxies.append(proxy)
    for p in proxies:
        f.write((p)+"\n")
    await ctx.send(file=File("proxies.txt"))
    return

bot.run(token)
