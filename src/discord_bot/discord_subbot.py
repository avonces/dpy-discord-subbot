# imports
import os
import datetime
import logging
from logging import config
import dotenv
import discord
from discord.ext import commands
from custom_help_command import CustomHelpCommand


# logging
"""configure .log file name"""
logFileName = f'logs/log_-_{datetime.datetime.now().isoformat().replace(":", "-")}.log'

"""configure root logger; set up basic logger"""
logging.config.fileConfig('../logging.conf', defaults={'logfilename': logFileName})
logger = logging.getLogger(__name__)


# dotenv
"""import secrets and vars from .env file because of security and configuration reasons"""
dotenv.load_dotenv()
discordToken = os.getenv('DISCORD_TOKEN')


# create subbot
"""create the client (bot)"""
intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or(*['sb1']),
                      strip_after_prefix=True,
                      case_insensitive=True,
                      intents=intents,
                      help_command=CustomHelpCommand())


# define main function for running bot
def main():
    """runs the code and starts the client"""
    logger.info('loading extensions...')
    """load all the available extensions from "ext" folder"""
    # initialize dictionary for saving path.to.files: [filenames]
    dir_name_filenames_dict = {}

    # get all files from directories and subdirectories
    for (dir_path, dir_name, file_names) in os.walk('./ext'):
        dotted_dir_path = dir_path.replace('./', '').replace('\\', '.')
        dir_name_filenames_dict[dotted_dir_path] = file_names

    # try loading all the files that end on .py
    for dotted_dir_path in dir_name_filenames_dict.keys():
        for file_name in dir_name_filenames_dict[dotted_dir_path]:
            if file_name.endswith('.py'):
                try:
                    if not file_name == 'discord_subbot.py':
                        client.load_extension(f"{dotted_dir_path}.{file_name[:-3]}")
                        logger.info(f'successfully loaded extension {dotted_dir_path}.{file_name[:-3]}')
                except Exception as error:
                    logger.critical(f'failed loading extension {dotted_dir_path}.{file_name[:-3]}')
                    logger.error(f'error: "{error}"')

    # run
    logger.info('executing...')
    """run the code and start the client"""
    client.run(discordToken)


if __name__ == '__main__':
    main()
