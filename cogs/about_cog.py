from twitchio.ext import commands
from web_scrapers import FactScraper, RiddleScraper, SaucyInsultScraper

class AboutCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.scrapers = [FactScraper(), RiddleScraper(), SaucyInsultScraper()]

    @commands.command(name='sillybot')
    async def sillybot_command(self, ctx):
        message = f"I'm SillyBot0! I like dogs, friends, sunsets, and other human things! If you like what I've been posting, check out these links: "
        for scraper in self.scrapers[:-1]:
            url = scraper.url
            message += f"{url}, "
        message += self.scrapers[-1].url
        await ctx.send(message)

