from twitchio.ext import commands
from web_scrapers import FactScraper

# Deco changes the class to AutoCog
@commands.cog()
class FactCog:

    # AutoCogs only can accept bot as an init argument which is passed automatically
    def __init__(self, bot):
        self.bot = bot
        self.fact_scraper = FactScraper()
    
    @commands.command(name='fact')
    async def fact_command(self, ctx):
        fact = self.fact_scraper.scrape()
        await ctx.send(fact.description)
