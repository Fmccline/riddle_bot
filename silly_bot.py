"""
Twitch Chat bot that posts a riddle when commanded and posts the answer 30 seconds later.
Code used from these links.
https://github.com/TwitchIO/TwitchIOv
https://github.com/bsquidwrd/Example-TwitchIO-Bot
"""

import os
import logging
import asyncio

from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound

import environment
from environment import Env
from web_scrapers import RiddleScraper
from web_scrapers import FactScraper

from web_scrapers.fact_scraper import FactScraper
from web_scrapers.riddle_scraper import RiddleScraper


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
                    )


class Bot(commands.Bot):
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

    async def event_message(self, message):
        user_prefix = self.get_author_prefix(message)
        self.log.info(
            f'#{message.channel} - {user_prefix}{message.author.name} - {message.content}')

        if message.author.name.lower() != self.nick.lower():
            await self.handle_commands(message)

    @commands.command(name='fact')
    async def test_command(self, ctx):
        fact = self.fact_scraper.scrape()
        await ctx.send(fact.description)

    @commands.command(name='riddle')
    async def riddle_command(self, ctx):
        if not self.waiting_to_answer:
            riddle = None
            while riddle is None or len(riddle.question) > 140 or len(riddle.answer) > 140:
                riddle = self.riddle_scraper.scrape()

            await self.sendRiddle(ctx, riddle)

    async def sendRiddle(self, ctx, riddle):
        self.waiting_to_answer = True
        channel = ctx.channel
        loop = asyncio.get_event_loop()
        loop.create_task(channel.send(
            riddle.question + f" (I will give the answer in {self.DELAY_TIME} seconds!)"))
        await asyncio.sleep(self.DELAY_TIME)
        loop.create_task(channel.send(riddle.answer))
        self.waiting_to_answer = False


if __name__ == '__main__':
    nick = os.environ[Env.BOT_NICK]
    irc_token = os.environ[Env.BOT_TOKEN]
    client_id = os.getenv(Env.CLIENT_ID, None)

    initial_channels = [os.environ[Env.CHANNEL], nick]
    bot = Bot(irc_token=irc_token, client_id=client_id,
              nick=nick, initial_channels=initial_channels)
    bot.run()
