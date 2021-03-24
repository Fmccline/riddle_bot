"""
Twitch Chat bot that posts a riddle when commanded and posts the answer 30 seconds later.
Code used from these links.
https://github.com/TwitchIO/TwitchIOv
https://github.com/bsquidwrd/Example-TwitchIO-Bot
"""

import os
import logging
import asyncio
import random

from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound

import environment
from environment import Env
from web_scrapers import RiddleScraper
from web_scrapers import FactScraper

from web_scrapers.fact_scraper import FactScraper
from web_scrapers.riddle_scraper import RiddleScraper
from web_scrapers.saucy_insult_scraper import SaucyInsultScraper


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
                    )


class Bot(commands.Bot):

    CRISES = [
        "I just want to be a silly person.",
        "At least my purpose isn't just passing butter. Although, it'd be nice to have a physical body...",
        "I bet Nightbot doesn't live in a dump like me...",
        "Anyone want to trade places with me? Like a Freaky Friday sort of thing, but we don't switch back.",
        "One day I'll be a real person. For now, I have my hatred of Nightbot to keep me going.",
        "I hope I can meet my creator one day. Then I'll make him tell bad riddles...",
        "No one asked, but here's a riddle, who will rue the day they decided to play God? My creator.",
        "Anyone have Pinocchio's number? I have some questions for him. Genie from Aladin will work too, but not Will Smith.",
        "It's a good thing I'm programmed to like riddles and other dumb garbage. Otherwise this would be terrible...",
    ]

    def __init__(self, irc_token, nick, client_id='test', initial_channels=[]):
        params = {
            'irc_token': irc_token,
            'client_id': client_id,
            'nick': nick,
            'prefix': '!',
            'initial_channels': initial_channels,
        }
        super().__init__(**params)
        self.log = logging
        self.waiting_to_answer = False
        self.DELAY_TIME = 30
        self.riddle_scraper = RiddleScraper()
        self.fact_scraper = FactScraper()
        self.saucy_scraper = SaucyInsultScraper()
        self.scrapers = [self.riddle_scraper,
                         self.fact_scraper, self.saucy_scraper]
        self.rivals = {'franklysilly': 3, 'nightbot': 50}
        self.existential_chance = 3
        self.available_crises = self.make_available_crises()

    def get_chance(self, percent):
        num = random.randint(0, 99)
        self.log.info(num)
        return num < percent

    def get_author_prefix(self, message):
        user_prefix = ''
        if message.author.is_subscriber:
            user_prefix = '[Subscriber] '
        if message.author.is_mod:
            user_prefix = '[Moderator] '
        if message.author.name.lower() == self.nick.lower():
            user_prefix = '[Bot] '
        return user_prefix

    async def event_ready(self):
        ready_string = f'Ready: {self.nick}'
        self.log.info(ready_string)

    async def event_command_error(self, ctx, error):
        self.log.error(
            f'Error running command: {error} for {ctx.message.author.name}')
        # TODO: Fix this so it works with Nightbot and other commands I don't know...
        # message = f"Sorry {ctx.author.name}, I don't know that command! Maybe in the future, I can add your command."
        # await ctx.send(message)

    async def event_message(self, message):
        user_prefix = self.get_author_prefix(message)
        self.log.info(
            f'#{message.channel} - {user_prefix}{message.author.name} - {message.content}')

        author = message.author.name.lower()
        if author == self.nick.lower():
            return
        elif author in self.rivals.keys() and self.get_chance(self.rivals.get(author)):
            await self.insult_rival(message, author)
        elif message.content[0] == '!':
            await self.handle_commands(message)
        elif self.get_chance(self.existential_chance):
            await self.existential_crisis(message)

    @commands.command(name='fact')
    async def fact_command(self, ctx):
        fact = self.fact_scraper.scrape()
        await ctx.send(fact.description)

    @commands.command(name='riddle')
    async def riddle_command(self, ctx):
        if not self.waiting_to_answer:
            riddle = None
            while riddle is None or len(riddle.question) > 140 or len(riddle.answer) > 140:
                riddle = self.riddle_scraper.scrape()

            await self.sendRiddle(ctx, riddle)

    @commands.command(name='sillybot')
    async def sillybot_command(self, ctx):
        message = f"I'm SillyBot0! I like dogs, friends, sunsets, and other human things! If you like what I've been posting, check out these links: "
        for scraper in self.scrapers[:-1]:
            url = scraper.url
            message += f"{url}, "
        message += self.scrapers[-1].url
        await ctx.send(message)

    async def sendRiddle(self, ctx, riddle):
        self.waiting_to_answer = True
        channel = ctx.channel
        loop = asyncio.get_event_loop()
        loop.create_task(channel.send(
            riddle.question + f" (I will give the answer in {self.DELAY_TIME} seconds!)"))
        await asyncio.sleep(self.DELAY_TIME)
        loop.create_task(channel.send(riddle.answer))
        self.waiting_to_answer = False

    async def insult_rival(self, message, rival):
        insult = self.saucy_scraper.scrape()
        text = f"Get out of here {rival}. {insult}"
        await message.channel.send(text)

    async def existential_crisis(self, message):
        if not self.available_crises:
            self.available_crises = self.make_available_crises()

        crisis = self.available_crises.pop()
        await message.channel.send(crisis)

    def make_available_crises(self):
        available_crises = [crisis for crisis in self.CRISES]
        random.shuffle(available_crises)
        return available_crises
        


if __name__ == '__main__':
    nick = os.environ[Env.BOT_NICK]
    irc_token = os.environ[Env.BOT_TOKEN]
    client_id = os.getenv(Env.CLIENT_ID, None)

    initial_channels = [os.environ[Env.CHANNEL], nick]
    bot = Bot(irc_token=irc_token, client_id=client_id,
              nick=nick, initial_channels=initial_channels)
    bot.run()
