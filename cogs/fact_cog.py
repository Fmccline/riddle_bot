from twitchio.ext import commands
from web_scrapers import FactScraper
import time

# # Deco changes the class to AutoCog
# @commands.cog()
class FactCog(commands.Cog):

    # AutoCogs only can accept bot as an init argument which is passed automatically
    def __init__(self, bot):
        self.bot = bot
        self.fact_scraper = FactScraper()
        self.last_fact = None
        self.fact_delay = 3
    
    @commands.command(name='fact')
    async def fact_command(self, ctx):
        now = time.time()
        if self.last_fact is None or now - self.last_fact > self.fact_delay:
            self.last_fact = now
            fact = self.fact_scraper.scrape()
            await ctx.send(fact.description)
