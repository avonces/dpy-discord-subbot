# imports
import os
import logging
import discord
from discord.ext import commands
import sqlite3


# logging
"""create logger by inheriting configuration from root logger"""
logger = logging.getLogger(__name__)


# extension
class OnMessageListener(commands.Cog, name='On Message Listener', description='contains on_message listener'):
    """cog for on_message event"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        """"custom on_ready event"""
        """empty template"""

        # do not process the following for messages sent by the bot itself
        if message.author == self.client.user:
            return


# cog related functions
def setup(client):
    """load extensions"""
    logger.info(f'loading extension: {os.path.basename(__file__)}')
    client.add_cog(OnMessageListener(client))


def teardown(client):
    """send information when extension is being unloaded"""
    logger.info(f'unloading extension: {os.path.basename(__file__)}')
